#include <stdint.h>
#include <stdio.h>
#include <string.h> // Needed for memcpy
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "driver/i2c_master.h"
#include "driver/i2c_types.h"


#define I2C_MASTER_SCL_IO           CONFIG_I2C_MASTER_SCL       /*!< GPIO number used for I2C master clock */
#define I2C_MASTER_SDA_IO           CONFIG_I2C_MASTER_SDA       /*!< GPIO number used for I2C master data  */
#define I2C_MASTER_NUM              I2C_NUM_0                   /*!< I2C port number for master dev */
#define I2C_MASTER_FREQ_HZ          CONFIG_I2C_MASTER_FREQUENCY /*!< I2C master clock frequency */
#define I2C_MASTER_TX_BUF_DISABLE   0                           /*!< I2C master doesn't need buffer */
#define I2C_MASTER_RX_BUF_DISABLE   0                           /*!< I2C master doesn't need buffer */
#define I2C_MASTER_TIMEOUT_MS       1000

// --- MCP9800 Specific Defines ---

// IMPORTANT: Verify this address matches your specific MCP9800 variant or A0-A2 pin settings.
// Default for MCP9801/03 (A2=A1=A0=GND) or MCP9800/02A0 variant is 0x48.
#define MCP9800_I2C_ADDR 0x48 // 0b1001000

// Register Pointer Addresses (MCP9800/1/2/3)
#define MCP9800_REG_TA      0x00 // Ambient Temperature Register (Read Only)
#define MCP9800_REG_CONFIG  0x01 // Configuration Register (Read/Write)
#define MCP9800_REG_THYST   0x02 // Temperature Hysteresis Register (Read/Write) - Lower threshold
#define MCP9800_REG_TSET    0x03 // Temperature Limit-Set Register (Read/Write) - Upper threshold

// Configuration Register Settings (MCP9800 - 8 bits)
// Example: 12-bit resolution, Continuous conversion, Comparator mode, Active Low Alert, 1 Fault queue count
// Bits: [OS(0)|RES1(1)|RES0(1)|FTS1(0)|FTS0(0)|AL(0)|CMP/INT(0)|SHDN(0)] = 0b01100000
#define MCP9800_CONFIG_VALUE 0x60

// Temperature Limit Settings (MCP9800 - 9-bit value, 0.5 C LSB, stored in 16-bit reg)
// The 9-bit value uses bits 8 down to 0 of the MSB. Bit 8 is sign.
// LSBs of register (byte 2) are ignored on write, read as 0.
// TSET = 120 C = 240 * 0.5 C -> Binary 0 1111 0000 -> Store as 0x7800
#define MCP9800_TSET_VALUE  0x7800 // 120 C Limit
// THYST = 90 C = 180 * 0.5 C -> Binary 0 1011 0100 -> Store as 0x5A00
#define MCP9800_THYST_VALUE 0x5A00 // 90 C Hysteresis Limit


static const char *TAG = "mcp9800";
// static volatile bool alert_triggered = false; // Alert logic not implemented

/**
 * @brief i2c master initialization
 */
static esp_err_t i2c_master_init(i2c_master_bus_handle_t *bus_handle, i2c_master_dev_handle_t *dev_handle)
{
    i2c_master_bus_config_t bus_config = {
        .i2c_port = I2C_MASTER_NUM,
        .sda_io_num = I2C_MASTER_SDA_IO,
        .scl_io_num = I2C_MASTER_SCL_IO,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = true,
    };
    esp_err_t ret = i2c_new_master_bus(&bus_config, bus_handle);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to initialize I2C master bus: %s", esp_err_to_name(ret));
        return ret;
    }

    i2c_device_config_t dev_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = MCP9800_I2C_ADDR, // Use MCP9800 Address
        .scl_speed_hz = I2C_MASTER_FREQ_HZ,
    };
    ret = i2c_master_bus_add_device(*bus_handle, &dev_config, dev_handle);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to add I2C device: %s", esp_err_to_name(ret));
        i2c_del_master_bus(*bus_handle); // Clean up bus if device add fails
        return ret;
    }
    return ESP_OK;
}

/**
 * @brief Write sequence to MCP9800 Register using standard ESP-IDF functions
 * @param i2c_dev       I2C device handle
 * @param reg_addr      Register pointer address
 * @param data          Pointer to data buffer to write
 * @param size_bytes_w  Number of data bytes to write (excluding register pointer)
 * @return esp_err_t
 */
static esp_err_t mcp9800_write_register(i2c_master_dev_handle_t i2c_dev, uint8_t reg_addr, const uint8_t* data, size_t size_bytes_w)
{
    // Allocate buffer: 1 byte for register pointer + data bytes
    uint8_t *write_buf = malloc(size_bytes_w + 1);
    if (write_buf == NULL) {
        ESP_LOGE(TAG, "Failed to allocate memory for I2C write buffer");
        return ESP_ERR_NO_MEM;
    }

    // First byte is the register pointer
    write_buf[0] = reg_addr;
    // Copy data bytes after the register pointer
    memcpy(&write_buf[1], data, size_bytes_w);

    // Transmit the combined buffer (Reg Pointer + Data)
    esp_err_t ret = i2c_master_transmit(i2c_dev, write_buf, size_bytes_w + 1, I2C_MASTER_TIMEOUT_MS);

    free(write_buf); // Free allocated buffer

    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "I2C Transmit Error to reg 0x%02X: %s", reg_addr, esp_err_to_name(ret));
    }
    return ret;
}

/**
 * @brief Read sequence from MCP9800 Register using standard ESP-IDF functions
 *        Handles: START -> AddrW -> ACK -> RegPtr -> ACK -> REPEATED_START -> AddrR -> ACK -> Read... -> STOP
 * @param i2c_dev       I2C device handle
 * @param reg_addr      Register pointer address
 * @param data          Pointer to buffer to store read data
 * @param size_bytes_r  Number of data bytes to read
 * @return esp_err_t
 */
static esp_err_t mcp9800_read_register(i2c_master_dev_handle_t i2c_dev, uint8_t reg_addr, uint8_t* data, size_t size_bytes_r)
{
    // Write the register pointer first, then read the data using a repeated start
    esp_err_t ret = i2c_master_transmit_receive(
        i2c_dev,        // Device handle
        &reg_addr,      // Pointer to write data (register address)
    1,              // Write data size (1 byte for register pointer)
    data,           // Pointer to read buffer
    size_bytes_r,   // Read data size
    I2C_MASTER_TIMEOUT_MS // Timeout
    );
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "I2C Transmit/Receive Error from reg 0x%02X: %s", reg_addr, esp_err_to_name(ret));
    }
    return ret;
}


/**
 * @brief Converts raw temperature data (assuming 12-bit resolution is set) to Celsius
 * @param temp_raw Pointer to the 2-byte raw temperature data (MSB first)
 * @return Temperature in degrees Celsius
 */
static float temp_conv_C (const uint8_t* temp_raw) {
    // Combine MSB and LSB
    int16_t digital_temp = ((int16_t)temp_raw[0] << 8) | temp_raw[1];

    // Data is in the upper 12 bits (bit 15 to bit 4). Shift right by 4.
    // Arithmetic right shift handles sign extension correctly.
    digital_temp = digital_temp >> 4;

    // Convert to Celsius (LSB = 0.0625 C for 12-bit resolution)
    float temperature_c = (float)digital_temp * 0.0625f;

    return temperature_c;
}


void app_main(void)
{
    uint8_t temp_data_raw[2];
    i2c_master_bus_handle_t bus_handle;
    i2c_master_dev_handle_t dev_handle;

    if (i2c_master_init(&bus_handle, &dev_handle) != ESP_OK) {
        ESP_LOGE(TAG, "I2C initialization failed. Halting.");
        return; // Or handle error appropriately
    }
    ESP_LOGI(TAG, "I2C initialized successfully");

    // Prepare TSET and THYST data (MSB first) - Note: MCP9800 only uses upper 9 bits
    uint8_t thyst_data[] = {
        (MCP9800_THYST_VALUE >> 8) & 0xFF, // MSB
        MCP9800_THYST_VALUE & 0xFF         // LSB (Lower bits ignored by MCP9800 on write)
    };
    uint8_t tset_data[] = {
        (MCP9800_TSET_VALUE >> 8) & 0xFF,  // MSB
        MCP9800_TSET_VALUE & 0xFF          // LSB (Lower bits ignored by MCP9800 on write)
    };

    // Prepare Config data (single byte)
    uint8_t config_data = MCP9800_CONFIG_VALUE;

    ESP_LOGI(TAG, "Writing THYST Register (0x%02X = %.1f C Hysteresis Limit)...", MCP9800_REG_THYST, 90.0);
    // Write 2 bytes (pointer + data)
    ESP_ERROR_CHECK(mcp9800_write_register(dev_handle, MCP9800_REG_THYST, thyst_data, sizeof(thyst_data)));
    vTaskDelay(pdMS_TO_TICKS(20)); // Small delay after write

    ESP_LOGI(TAG, "Writing TSET Register (0x%02X = %.1f C Upper Limit)...", MCP9800_REG_TSET, 120.0);
    // Write 2 bytes (pointer + data)
    ESP_ERROR_CHECK(mcp9800_write_register(dev_handle, MCP9800_REG_TSET, tset_data, sizeof(tset_data)));
    vTaskDelay(pdMS_TO_TICKS(20)); // Small delay after write

    ESP_LOGI(TAG, "Writing CONFIG Register (0x%02X - Setting 12-bit resolution)...", config_data);
    // Write 1 byte (pointer + data)
    ESP_ERROR_CHECK(mcp9800_write_register(dev_handle, MCP9800_REG_CONFIG, &config_data, 1));
    vTaskDelay(pdMS_TO_TICKS(20)); // Small delay after write


    // --- Read back config to verify ---
    uint8_t read_config;
    ESP_LOGI(TAG, "Reading back CONFIG Register (0x%02X)...", MCP9800_REG_CONFIG);
    // Read 1 byte
    if (mcp9800_read_register(dev_handle, MCP9800_REG_CONFIG, &read_config, 1) == ESP_OK) {
        ESP_LOGI(TAG, "CONFIG Read back = 0x%02X", read_config);
        if (read_config != config_data) {
            ESP_LOGW(TAG, "CONFIG read back mismatch! Expected 0x%02X", config_data);
        }
    } else {
        ESP_LOGE(TAG, "Failed to read back CONFIG register.");
    }
    // Wait > 240ms (max 12-bit conversion time) after config write before first temp read
    vTaskDelay(pdMS_TO_TICKS(300));


    while (1) {
        ESP_LOGI(TAG, "Reading Temperature (TA) Register (0x%02X)...", MCP9800_REG_TA);
        // Read 2 bytes
        esp_err_t read_status = mcp9800_read_register(dev_handle, MCP9800_REG_TA, temp_data_raw, sizeof(temp_data_raw));

        if (read_status == ESP_OK) {
            // Assuming 12-bit resolution was successfully set
            float temp_c = temp_conv_C(temp_data_raw);
            ESP_LOGI(TAG, "Temperature Raw = 0x%02X%02X, Celsius = %.4f C", temp_data_raw[0], temp_data_raw[1], temp_c);
        } else {
            ESP_LOGE(TAG, "Failed to read temperature: %s", esp_err_to_name(read_status));
            vTaskDelay(pdMS_TO_TICKS(500)); // Longer delay on error
        }

        vTaskDelay(pdMS_TO_TICKS(2000)); // Read every 2 seconds
    }

    // Cleanup (code might not reach here in typical embedded loop)
    ESP_LOGI(TAG, "De-initializing I2C...");
    ESP_ERROR_CHECK(i2c_master_bus_rm_device(dev_handle));
    ESP_ERROR_CHECK(i2c_del_master_bus(bus_handle));
    ESP_LOGI(TAG, "I2C de-initialized successfully");
}
