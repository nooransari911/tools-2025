/*
 * SPDX-FileCopyrightText: 2024 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Unlicense OR CC0-1.0
 */
/* i2c - Simple Example

   Simple I2C example that shows how to initialize I2C
   as well as reading and writing from and to registers for a sensor connected over I2C.

   The sensor used in this example is a MPU9250 inertial measurement unit.
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



#define I2C_MASTER_SCL_IO           CONFIG_I2C_MASTER_SCL       /*!< GPIO number used for I2C master clock */
#define I2C_MASTER_SDA_IO           CONFIG_I2C_MASTER_SDA       /*!< GPIO number used for I2C master data  */
#define I2C_MASTER_NUM              I2C_NUM_0                   /*!< I2C port number for master dev */
#define I2C_MASTER_FREQ_HZ          CONFIG_I2C_MASTER_FREQUENCY /*!< I2C master clock frequency */
#define I2C_MASTER_TX_BUF_DISABLE   0                           /*!< I2C master doesn't need buffer */
#define I2C_MASTER_RX_BUF_DISABLE   0                           /*!< I2C master doesn't need buffer */
#define I2C_MASTER_TIMEOUT_MS       400


// 7-bit I2C address (ADDO = GND)
#define TMP102_ADDR 0b1001000
// --- Define GPIO Pin Names ---
#define RELAY_CH1_PIN   GPIO_NUM_18 // Output Pin for Relay Channel 1
#define RELAY_CH2_PIN   GPIO_NUM_19 // Output Pin for Relay Channel 2
#define ALERT_PIN       GPIO_NUM_4  // Input Pin for Alert signal


// Register addresses
#define POINTER_TEMP      0x00
#define POINTER_CONFIG    0x01
#define POINTER_TLOW      0x02
#define POINTER_THIGH     0x03


// Set TLOW register (90°C = 0x05A0)
#define TLOW_VALUE 0x05A0
// Set THIGH register (120°C = 0x0780)
#define THIGH_VALUE 0x0780 




static const char *TAG = "tmp102";
static volatile bool alert_triggered = false;




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
 * @brief i2c master initialization
 */
static void i2c_master_init(i2c_master_bus_handle_t *bus_handle, i2c_master_dev_handle_t *dev_handle)
{
    i2c_master_bus_config_t bus_config = {
        .i2c_port = I2C_MASTER_NUM,
        .sda_io_num = I2C_MASTER_SDA_IO,
        .scl_io_num = I2C_MASTER_SCL_IO,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = true,
    };
    ESP_ERROR_CHECK(i2c_new_master_bus(&bus_config, bus_handle));

    i2c_device_config_t dev_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = TMP102_ADDR,
        .scl_speed_hz = I2C_MASTER_FREQ_HZ,
    };
    ESP_ERROR_CHECK(i2c_master_bus_add_device(*bus_handle, &dev_config, dev_handle));
}


static esp_err_t I2C_READ_op (i2c_master_dev_handle_t i2c_dev, uint8_t reg_addr, uint8_t* data, size_t size_bytes_r, int xfer_timeout_ms) {
    uint8_t device_address = TMP102_ADDR;
    uint8_t write_device_addr = (device_address << 1) | 0;
    uint8_t read_device_addr  = (device_address << 1) | 1;
    esp_err_t opres;
    
    i2c_operation_job_t set_reg_pointer [] = {
        {
            .command = I2C_MASTER_CMD_START
        },
        {//WRITE device address
            .command = I2C_MASTER_CMD_WRITE,
            .write   = {
                .ack_check    = true,
                .data         = (uint8_t *) &write_device_addr,
                .total_bytes  = 1
            }
        },
        {//WRITE register address
            .command = I2C_MASTER_CMD_WRITE,
            .write   = {
                .ack_check    = true,
                .data         = (uint8_t *) &reg_addr,
                .total_bytes  = 1
            }
        },
        {
            .command = I2C_MASTER_CMD_STOP
        }
    };
    
    opres = i2c_master_execute_defined_operations (
        i2c_dev,
        set_reg_pointer,
        sizeof (set_reg_pointer) / sizeof (i2c_operation_job_t),
        xfer_timeout_ms
    );

    if (opres != ESP_OK) {
        return opres;
    }

    if (size_bytes_r == 1) {

        i2c_operation_job_t i2c_R_data_ops [] = {
            {
                .command = I2C_MASTER_CMD_START
            },
            {//WRITE device address
                .command = I2C_MASTER_CMD_WRITE,
                .write   = {
                    .ack_check    = true,
                    .data         = (uint8_t *) &read_device_addr,
                    .total_bytes  = 1
                }
            },
            {//READ only byte
                .command = I2C_MASTER_CMD_READ,
                .read = {
                    .ack_value    = I2C_NACK_VAL,
                    .data         = data,
                    .total_bytes  = 1
                }
            },
            {
                .command = I2C_MASTER_CMD_STOP
            }
        };


        opres = i2c_master_execute_defined_operations (
            i2c_dev,
            i2c_R_data_ops,
            sizeof (i2c_R_data_ops) / sizeof (i2c_operation_job_t),
            xfer_timeout_ms
        );

    }


    else {

        i2c_operation_job_t i2c_R_data_ops [] = {
            {
                .command = I2C_MASTER_CMD_START
            },
            {//WRITE device address
                .command = I2C_MASTER_CMD_WRITE,
                .write   = {
                    .ack_check    = true,
                    .data         = (uint8_t *) &read_device_addr,
                    .total_bytes  = 1
                }
            },
            {//READ first size-1 bytes
                .command = I2C_MASTER_CMD_READ,
                .read   = {
                    .ack_value    = I2C_ACK_VAL,
                    .data         = data,
                    .total_bytes  = size_bytes_r-1
                }
            },
            {//READ last byte
                .command = I2C_MASTER_CMD_READ,
                .read = {
                    .ack_value    = I2C_NACK_VAL,
                    .data         = data + (size_bytes_r - 1),
                    .total_bytes  = 1
                }
            },
            {
                .command = I2C_MASTER_CMD_STOP
            }
        };

        opres = i2c_master_execute_defined_operations (
            i2c_dev,
            i2c_R_data_ops,
            sizeof (i2c_R_data_ops) / sizeof (i2c_operation_job_t),
            xfer_timeout_ms
        );


    }



    return opres;


}



static esp_err_t I2C_WRITE_op (i2c_master_dev_handle_t i2c_dev, uint8_t reg_addr, uint8_t* data, size_t size_bytes_w, int xfer_timeout_ms) {
    uint8_t device_address = TMP102_ADDR;
    uint8_t write_device_addr = (device_address << 1) | 0;

    i2c_operation_job_t i2c_W_data_ops [] = {
        {
            .command = I2C_MASTER_CMD_START
        },
        {//WRITE device address
            .command = I2C_MASTER_CMD_WRITE,
            .write   = {
                .ack_check    = true,
                .data         = (uint8_t *) &write_device_addr,
                .total_bytes  = 1
            }
        },
        {//WRITE register address
            .command = I2C_MASTER_CMD_WRITE,
            .write   = {
                .ack_check    = true,
                .data         = (uint8_t *) &reg_addr,
                .total_bytes  = 1
            }
        },
        {//WRITE data
            .command = I2C_MASTER_CMD_WRITE,
            .write   = {
                .ack_check    = true,
                .data         = data,
                .total_bytes  = size_bytes_w
            }
        },
        {
            .command = I2C_MASTER_CMD_STOP
        }
    };


    esp_err_t opres = i2c_master_execute_defined_operations (
        i2c_dev,
        i2c_W_data_ops,
        sizeof (i2c_W_data_ops) / sizeof (i2c_operation_job_t),
        xfer_timeout_ms
    );

    return opres;

}


static float temp_conv_C (const uint8_t* temp_raw) {
    int16_t digital_temp = (
        (int16_t) (temp_raw [0] << 8) |
        (temp_raw [1])
    );

    digital_temp = digital_temp >> 4;

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


    
     
    uint8_t data[2];
    i2c_master_bus_handle_t bus_handle;
    i2c_master_dev_handle_t dev_handle;
    i2c_master_init(&bus_handle, &dev_handle);
    ESP_LOGI(TAG, "I2C initialized successfully");

    uint8_t TLOW []  = {
        (TLOW_VALUE & 0xFF00) >> 8,
        TLOW_VALUE & 0x00FF
    };
    uint8_t THIGH []  = {
        (THIGH_VALUE & 0xFF00) >> 8,
        THIGH_VALUE & 0x00FF
    };
    uint16_t config = 0x62A0;
    uint8_t config_arr [] = {
        (config & 0xFF00) >> 8,
        config & 0x00FF

    };

    uint8_t TEMP_VALUE [2];
    esp_err_t readres;

    ESP_LOGI(TAG, "Writing TLOW Register (0x%04X)....", TLOW_VALUE);
    ESP_ERROR_CHECK (I2C_WRITE_op (dev_handle, POINTER_TLOW, TLOW, sizeof(TLOW), I2C_MASTER_TIMEOUT_MS));

    ESP_LOGI(TAG, "Writing THIGH Register (0x%04X)....", THIGH_VALUE);
    ESP_ERROR_CHECK (I2C_WRITE_op (dev_handle, POINTER_THIGH, THIGH, sizeof(THIGH), I2C_MASTER_TIMEOUT_MS));

    ESP_LOGI(TAG, "Writing CONFIG Register (0x%04X)....", config);
    ESP_ERROR_CHECK (I2C_WRITE_op (dev_handle, POINTER_CONFIG, config_arr, sizeof(config_arr), I2C_MASTER_TIMEOUT_MS));

    while (1) {
        ESP_LOGI(TAG, "Reading TEMP Register....");
        readres = (I2C_READ_op (dev_handle, POINTER_TEMP, TEMP_VALUE, sizeof (TEMP_VALUE), I2C_MASTER_TIMEOUT_MS));

        if (readres == ESP_OK) {
            float temp_c = temp_conv_C (TEMP_VALUE);
            ESP_LOGI(TAG, "Temperature Raw = 0x%02X%02X, Celsius = %.4f °C", TEMP_VALUE[0], TEMP_VALUE[1], temp_c);
        }

        else {
            ESP_LOGE (TAG, "Failed to read temp");
        }

        vTaskDelay(pdMS_TO_TICKS(2000));       


    }
    



    

    ESP_ERROR_CHECK(i2c_master_bus_rm_device(dev_handle));
    ESP_ERROR_CHECK(i2c_del_master_bus(bus_handle));
    ESP_LOGI(TAG, "I2C de-initialized successfully");
}
