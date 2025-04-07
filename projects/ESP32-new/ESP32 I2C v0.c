#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2c.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include <math.h> // For isnan()

// 7-bit I2C address (ADDO = GND)
#define TMP102_ADDR 0b1001000
#define ALERT_PIN 4  // Use int
#define I2C_MASTER_SCL_IO 22 // Use int
#define I2C_MASTER_SDA_IO 21 // Use int
#define I2C_MASTER_NUM I2C_NUM_0
#define I2C_MASTER_FREQ_HZ 400000
#define I2C_MASTER_TX_BUF_DISABLE 0
#define I2C_MASTER_RX_BUF_DISABLE 0

// Register addresses
#define POINTER_TEMP      0x00
#define POINTER_CONFIG    0x01
#define POINTER_TLOW      0x02
#define POINTER_THIGH     0x03

static const char *TAG = "tmp102";
static volatile bool alert_triggered = false;

static void IRAM_ATTR gpio_isr_handler(void* arg) {
    alert_triggered = true;
}

esp_err_t i2c_master_write_reg(uint8_t reg_addr, uint16_t data) {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (TMP102_ADDR << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write_byte(cmd, reg_addr, true);
    i2c_master_write_byte(cmd, (data >> 8) & 0xFF, true);
    i2c_master_write_byte(cmd, data & 0xFF, true);
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(I2C_MASTER_NUM, cmd, 1000 / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);
    return ret;
}

esp_err_t i2c_master_read_reg(uint8_t reg_addr, int16_t *data) {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (TMP102_ADDR << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write_byte(cmd, reg_addr, true);
    i2c_master_start(cmd); // Repeated START
    i2c_master_write_byte(cmd, (TMP102_ADDR << 1) | I2C_MASTER_READ, true);
    uint8_t high_byte, low_byte;
    i2c_master_read_byte(cmd, &high_byte, I2C_MASTER_ACK);
    i2c_master_read_byte(cmd, &low_byte, I2C_MASTER_NACK);
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(I2C_MASTER_NUM, cmd, 1000 / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);

    if (ret == ESP_OK) {
        *data = (int16_t)((high_byte << 8) | low_byte); // Combine bytes and cast
    }
    return ret;
}

// Function to read and convert temperature to Celsius
float readTemperature_esp() {
    int16_t rawTemp;
    if (i2c_master_read_reg(POINTER_TEMP, &rawTemp) != ESP_OK) {
        ESP_LOGE(TAG, "Failed to read temperature.");
        return NAN; // Return Not-a-Number if read fails.
    }

    // Convert the raw 12-bit value to Celsius
    if (rawTemp & 0x8000) {
        rawTemp = -((~rawTemp) + 1);
    }
    return (float)rawTemp * 0.0625;
}


void app_main() {
    // Configure I2C using a compound literal with designated initializers
    i2c_config_t conf = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = I2C_MASTER_SDA_IO,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_io_num = I2C_MASTER_SCL_IO,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master = {.clk_speed = I2C_MASTER_FREQ_HZ}, // Designated initializer for master
    };
    ESP_ERROR_CHECK(i2c_param_config(I2C_MASTER_NUM, &conf));
    ESP_ERROR_CHECK(i2c_driver_install(I2C_MASTER_NUM, conf.mode, I2C_MASTER_RX_BUF_DISABLE, I2C_MASTER_TX_BUF_DISABLE, 0));

    // Configure ALERT pin
    gpio_config_t io_conf = {
        .intr_type = GPIO_INTR_NEGEDGE,
        .pin_bit_mask = (1ULL << ALERT_PIN),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
    };
    ESP_ERROR_CHECK(gpio_config(&io_conf));
    ESP_ERROR_CHECK(gpio_install_isr_service(0));
    ESP_ERROR_CHECK(gpio_isr_handler_add(ALERT_PIN, gpio_isr_handler, NULL));

    // Set THIGH register (120°C = 0x0780)
    ESP_ERROR_CHECK(i2c_master_write_reg(POINTER_THIGH, 0x0780));

    // Set TLOW register (90°C = 0x05A0)
    ESP_ERROR_CHECK(i2c_master_write_reg(POINTER_TLOW, 0x05A0));

    // Set Configuration Register:  TM=1, other bits default.
    uint16_t configValue = 0x60A0; //default
    configValue |= 0x0200; //setting TM bit
    ESP_ERROR_CHECK(i2c_master_write_reg(POINTER_CONFIG, configValue));


    while (1) {
        if (alert_triggered) {
            ESP_LOGI(TAG, "Temperature exceeded 100°C!");
            alert_triggered = false;

            // Read and discard the temperature register (to clear alert).
            int16_t temp; // Dummy variable.
            i2c_master_read_reg(POINTER_TEMP, &temp);
        }

        // Read and print the temperature.
        float temperature = readTemperature_esp();
        if (!isnan(temperature)) {
            ESP_LOGI(TAG, "Temperature: %.2f °C", temperature);
        }

        vTaskDelay(500 / portTICK_PERIOD_MS);
    }
}
