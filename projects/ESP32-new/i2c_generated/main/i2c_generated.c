/*
 * SPDX-FileCopyrightText: 2024 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Unlicense OR CC0-1.0
 */
/* i2c - Complete Example for TMP102 Temperature Sensor

   Initializes I2C master, configures the TMP102 sensor,
   and continuously reads temperature data using standard ESP-IDF functions,
   correctly handling the TMP102's register pointer mechanism.
*/
#include <stdint.h>
#include <stdio.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_attr.h" // Required for IRAM_ATTR
#include "driver/i2c_master.h"
#include "driver/i2c_types.h"
#include "driver/gpio.h"

#include "esp_check.h" // For ESP_RETURN_ON_ERROR macro if desired

// --- Configuration ---
// Ensure these are set via menuconfig (idf.py menuconfig -> Component config -> ESP System -> I2C)
#define I2C_MASTER_SCL_IO           CONFIG_I2C_MASTER_SCL       /*!< GPIO number used for I2C master clock */
#define I2C_MASTER_SDA_IO           CONFIG_I2C_MASTER_SDA       /*!< GPIO number used for I2C master data  */
#define I2C_MASTER_NUM              I2C_NUM_0                   /*!< I2C port number for master dev (can be I2C_NUM_1) */
#define I2C_MASTER_FREQ_HZ          CONFIG_I2C_MASTER_FREQUENCY /*!< I2C master clock frequency */
#define I2C_TIMEOUT_MS              400                         /*!< I2C operation timeout ms */

// --- TMP102 Specific Defines ---
#define TMP102_I2C_ADDR             0x48 // 7-bit I2C address (0b1001000, ADDR0 pin to GND)
// --- Define GPIO Pin Names ---
#define RELAY_CH1_PIN   GPIO_NUM_18 // Output Pin for Relay Channel 1
#define RELAY_CH2_PIN   GPIO_NUM_19 // Output Pin for Relay Channel 2
#define ALERT_PIN       GPIO_NUM_4  // Input Pin for Alert signal


// Register addresses (Pointer Register Values)
#define TMP102_REG_TEMP             0x00
#define TMP102_REG_CONFIG           0x01
#define TMP102_REG_TLOW             0x02
#define TMP102_REG_THIGH            0x03

// Example Configuration values
// Set TLOW register (Example: 20°C = 20 / 0.0625 = 320 = 0x0140)
#define TLOW_TEMP_VAL_RAW           0x0140
// Set THIGH register (Example: 30°C = 30 / 0.0625 = 480 = 0x01E0)
#define THIGH_TEMP_VAL_RAW          0x01E0

// Configuration Register Value (TM=1 for Interrupt Mode, rest default)
// Default = 0x60A0. TM bit is D9 (bit 1 of MSB). 0x60A0 | 0x0200 = 0x62A0
#define CONFIG_VAL_MSB              0x62
#define CONFIG_VAL_LSB              0xA0
// --- End TMP102 Defines ---

static const char *TAG = "tmp102_main";




// --- ISR Function (Snippet 3) ---
// This function will be called when the interrupt on ALERT_PIN occurs.
// IRAM_ATTR is recommended for ISRs to ensure they run fast from IRAM,
// especially if calling functions like gpio_set_level. Check docs/config.
static void IRAM_ATTR gpio_isr_handler(void* arg) {
    // Inside the ISR, set RELAY_CH1_PIN and RELAY_CH2_PIN LOW
    gpio_set_level(RELAY_CH1_PIN, 0);
    gpio_set_level(RELAY_CH2_PIN, 0);

    // Optional: Signal a task from ISR for further processing
    // BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    // Example: if you have a task handle named 'alert_processing_task_handle'
    // vTaskNotifyGiveFromISR(alert_processing_task_handle, &xHigherPriorityTaskWoken);
    // portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}







/**
 * @brief Initialize I2C master bus and add TMP102 device.
 *
 * @param[out] bus_handle_ptr Pointer to store the created bus handle.
 * @param[out] dev_handle_ptr Pointer to store the created device handle.
 * @return esp_err_t ESP_OK on success, error code otherwise.
 */
static esp_err_t i2c_master_init(i2c_master_bus_handle_t *bus_handle_ptr, i2c_master_dev_handle_t *dev_handle_ptr)
{
    // Input validation
    if (!bus_handle_ptr || !dev_handle_ptr) {
        return ESP_ERR_INVALID_ARG;
    }

    i2c_master_bus_config_t bus_config = {
        .i2c_port = I2C_MASTER_NUM,
        .sda_io_num = I2C_MASTER_SDA_IO,
        .scl_io_num = I2C_MASTER_SCL_IO,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7, // Recommended value
        .flags.enable_internal_pullup = true, // NOTE: External pullups (2k-10k) recommended for reliability
    };

    esp_err_t ret = i2c_new_master_bus(&bus_config, bus_handle_ptr);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to create I2C master bus: %s", esp_err_to_name(ret));
        return ret;
    }
    ESP_LOGI(TAG, "I2C master bus (%d) created.", I2C_MASTER_NUM);

    i2c_device_config_t dev_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = TMP102_I2C_ADDR,
        .scl_speed_hz = I2C_MASTER_FREQ_HZ,
    };

    ret = i2c_master_bus_add_device(*bus_handle_ptr, &dev_config, dev_handle_ptr);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to add TMP102 device (0x%X): %s", TMP102_I2C_ADDR, esp_err_to_name(ret));
        // Clean up bus if device add fails
        i2c_del_master_bus(*bus_handle_ptr);
        *bus_handle_ptr = NULL; // Prevent dangling pointer use
    } else {
         ESP_LOGI(TAG, "TMP102 device (0x%X) added.", TMP102_I2C_ADDR);
    }
    return ret;
}

/**
 * @brief Write 2 bytes of data to a TMP102 register using i2c_master_transmit.
 *
 * @param dev_handle I2C device handle.
 * @param reg_addr The pointer register value (0x01-0x03 for writing).
 * @param data A pointer to a 2-byte array containing the data (MSB first).
 * @param timeout_ms Timeout in milliseconds.
 * @return ESP_OK on success, error code otherwise.
 */
static esp_err_t tmp102_write_register(i2c_master_dev_handle_t dev_handle, uint8_t reg_addr, const uint8_t* data, int timeout_ms)
{
    // Input validation
    if (!dev_handle || !data) {
        return ESP_ERR_INVALID_ARG;
    }

    uint8_t write_buf[3];
    write_buf[0] = reg_addr;    // First byte is the pointer register address
    write_buf[1] = data[0];     // Second byte is the data MSB
    write_buf[2] = data[1];     // Third byte is the data LSB

    // i2c_master_transmit sends START -> ADDR(W) -> write_buf[0] -> write_buf[1] -> write_buf[2] -> STOP
    esp_err_t ret = i2c_master_transmit(dev_handle, write_buf, sizeof(write_buf), timeout_ms);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "I2C transmit failed to reg 0x%02X: %s", reg_addr, esp_err_to_name(ret));
    }
    return ret;
}

/**
 * @brief Read 2 bytes of data from a TMP102 register using separate transmit (for pointer)
 *        and receive calls, correctly implementing the sequence with STOP/START between.
 *
 * @param dev_handle I2C device handle.
 * @param reg_addr The pointer register value (0x00-0x03).
 * @param[out] data A pointer to a 2-byte array to store the read data (MSB first).
 * @param timeout_ms Timeout in milliseconds for each I2C operation.
 * @return ESP_OK on success, error code otherwise.
 */
static esp_err_t tmp102_read_register(i2c_master_dev_handle_t dev_handle, uint8_t reg_addr, uint8_t* data, int timeout_ms)
{
    // Input validation
    if (!dev_handle || !data) {
        return ESP_ERR_INVALID_ARG;
    }

    esp_err_t ret;

    // Transaction 1: Write the pointer register address.
    // i2c_master_transmit sends START -> ADDR(W) -> reg_addr -> STOP
    ret = i2c_master_transmit(dev_handle, &reg_addr, 1, timeout_ms);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to set pointer register 0x%02X for read: %s", reg_addr, esp_err_to_name(ret));
        return ret;
    }

    // Transaction 2: Read the data from the implicitly selected register.
    // i2c_master_receive sends START -> ADDR(R) -> read data[0] -> read data[1] -> STOP
    ret = i2c_master_receive(dev_handle, data, 2, timeout_ms);
     if (ret != ESP_OK) {
        // Log specific error (timeout vs other failures)
        if (ret == ESP_ERR_TIMEOUT) {
             ESP_LOGW(TAG, "I2C receive timed out reading reg 0x%02X after %dms", reg_addr, timeout_ms);
        } else {
             ESP_LOGE(TAG, "Failed to receive data from reg 0x%02X: %s", reg_addr, esp_err_to_name(ret));
        }
     }
    return ret;
}

/**
 * @brief Convert raw TMP102 temperature data (12-bit normal mode) to Celsius.
 *
 * @param temp_raw Pointer to the 2-byte raw data buffer (MSB first).
 * @return Temperature in degrees Celsius.
 */
static float temp_conv_C (const uint8_t* temp_raw) {
    // Input validation
    if (!temp_raw) {
        ESP_LOGE(TAG, "temp_conv_C received NULL pointer");
        return -999.9f; // Indicate error
    }

    // Combine MSB and LSB into a 16-bit signed integer.
    int16_t digital_temp = ((int16_t)temp_raw[0] << 8) | temp_raw[1];

    // Arithmetic right shift by 4 for 12-bit resolution (preserves sign)
    digital_temp = digital_temp >> 4;

    // Apply resolution (0.0625 °C per LSB)
    float temperature_c = (float)digital_temp * 0.0625f;

    return temperature_c;
}

void app_main(void) {

    // --- Snippet 1: Configure Output Pins (Runs Once at Startup) ---
    ESP_LOGI(TAG, "Configuring output relay GPIOs...");
    // Use C99 designated initializers for concise configuration
    gpio_config_t io_conf_output = {
        .pin_bit_mask = (1ULL << RELAY_CH1_PIN) | (1ULL << RELAY_CH2_PIN),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    ESP_ERROR_CHECK(gpio_config(&io_conf_output));

    // Set initial level to HIGH
    ESP_ERROR_CHECK(gpio_set_level(RELAY_CH1_PIN, 1));
    ESP_ERROR_CHECK(gpio_set_level(RELAY_CH2_PIN, 1));
    ESP_LOGI(TAG, "Output Relay GPIOs (%d, %d) configured and set HIGH.", RELAY_CH1_PIN, RELAY_CH2_PIN);
    // --- End Snippet 1 ---
    
    

    // --- Snippet 2: Configure Input Pin and Interrupt ---
    ESP_LOGI(TAG, "Configuring input alert GPIO and interrupt...");
    // Install GPIO ISR service - required for per-pin handlers
    esp_err_t isr_service_err = gpio_install_isr_service(0); // Use ESP_INTR_FLAG_DEFAULT (0) or specific flags
    if (isr_service_err != ESP_OK && isr_service_err != ESP_ERR_INVALID_STATE) {
         ESP_LOGE(TAG, "Failed to install ISR service: %s", esp_err_to_name(isr_service_err));
         return; // Handle error
    } else if (isr_service_err == ESP_ERR_INVALID_STATE) {
        ESP_LOGW(TAG, "ISR service already installed.");
    }

    // Use C99 designated initializers for concise configuration
    gpio_config_t io_conf_input = {
        .pin_bit_mask = (1ULL << ALERT_PIN),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,     // Enable pull-up for active-low input
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_LOW_LEVEL     // Trigger interrupt when pin is LOW
    };
    ESP_ERROR_CHECK(gpio_config(&io_conf_input));

    // Remove handler first in case of re-configuration (good practice)
    gpio_isr_handler_remove(ALERT_PIN);
    // Add the specific ISR handler for ALERT_PIN
    ESP_ERROR_CHECK(gpio_isr_handler_add(ALERT_PIN, gpio_isr_handler, (void*) ALERT_PIN));

    ESP_LOGI(TAG, "Input Alert GPIO (%d) configured with LOW level interrupt.", ALERT_PIN);
    // --- End Snippet 2 ---


    
    i2c_master_bus_handle_t bus_handle = NULL;
    i2c_master_dev_handle_t dev_handle = NULL;
    esp_err_t op_status; // Variable to check operation status

    ESP_LOGI(TAG, "Initializing I2C master...");
    // Use ESP_ERROR_CHECK for critical init steps - program should not continue if this fails
    ESP_ERROR_CHECK(i2c_master_init(&bus_handle, &dev_handle));
    ESP_LOGI(TAG, "I2C initialization complete.");

    // Prepare data buffers for writing limit and config registers
    uint8_t tlow_data[]  = { (TLOW_TEMP_VAL_RAW >> 8) & 0xFF, TLOW_TEMP_VAL_RAW & 0xFF };
    uint8_t thigh_data[] = { (THIGH_TEMP_VAL_RAW >> 8) & 0xFF, THIGH_TEMP_VAL_RAW & 0xFF };
    uint8_t config_data[] = { CONFIG_VAL_MSB, CONFIG_VAL_LSB };

    // Write configuration and limits to TMP102
    ESP_LOGI(TAG, "Writing TLOW Register (0x%04X)...", TLOW_TEMP_VAL_RAW);
    op_status = tmp102_write_register(dev_handle, TMP102_REG_TLOW, tlow_data, I2C_TIMEOUT_MS);
    if (op_status != ESP_OK) ESP_LOGE(TAG, "TLOW write failed."); // Log error, but continue for example

    ESP_LOGI(TAG, "Writing THIGH Register (0x%04X)...", THIGH_TEMP_VAL_RAW);
    op_status = tmp102_write_register(dev_handle, TMP102_REG_THIGH, thigh_data, I2C_TIMEOUT_MS);
    if (op_status != ESP_OK) ESP_LOGE(TAG, "THIGH write failed.");

    ESP_LOGI(TAG, "Writing Config Register (0x%02X%02X)...", config_data[0], config_data[1]);
    op_status = tmp102_write_register(dev_handle, TMP102_REG_CONFIG, config_data, I2C_TIMEOUT_MS);
    if (op_status != ESP_OK) {
        ESP_LOGE(TAG, "CONFIG write failed.");
    } else {
        vTaskDelay(pdMS_TO_TICKS(50)); // Short delay after config write allows sensor time to process if needed
    }


    // Optional: Read back config to verify
    uint8_t read_config[2];
    ESP_LOGI(TAG, "Reading back Config Register...");
    op_status = tmp102_read_register(dev_handle, TMP102_REG_CONFIG, read_config, I2C_TIMEOUT_MS);
    if (op_status == ESP_OK) {
        ESP_LOGI(TAG, "Read Config = 0x%02X%02X", read_config[0], read_config[1]);
        // Add check if read_config matches config_data if needed
    } else {
         ESP_LOGE(TAG, "Failed to read back config register.");
    }

    // Continuously read temperature
    uint8_t temp_raw[2];
    ESP_LOGI(TAG, "Starting continuous temperature reading loop...");
    while (1) {
        op_status = tmp102_read_register(dev_handle, TMP102_REG_TEMP, temp_raw, I2C_TIMEOUT_MS);

        if (op_status == ESP_OK) {
            float temp_c = temp_conv_C(temp_raw);
            // Avoid logging raw value excessively if not needed for debugging
            ESP_LOGI(TAG, "Temperature = %.4f C", temp_c);
            // ESP_LOGD(TAG, "Raw = 0x%02X%02X", temp_raw[0], temp_raw[1]); // Use Debug level for raw
        }
        // Error logging handled within tmp102_read_register

        // Delay between readings
        vTaskDelay(pdMS_TO_TICKS(2000));
    }

    // --- Cleanup --- (Code below will likely not be reached in this example due to while(1))
    ESP_LOGI(TAG, "De-initializing I2C...");
    if (dev_handle) {
        ESP_ERROR_CHECK(i2c_master_bus_rm_device(dev_handle));
        ESP_LOGI(TAG, "TMP102 device removed.");
    }
    if (bus_handle) {
        ESP_ERROR_CHECK(i2c_del_master_bus(bus_handle));
         ESP_LOGI(TAG, "I2C master bus deleted.");
    }
    ESP_LOGI(TAG, "I2C de-initialized successfully.");
}
