#ifndef I2C_H
#define I2C_H

#include <stdint.h>
#include <stdbool.h>

/**
 * @brief Initializes the I2C peripheral in controller mode.
 */
void I2c_Init(void);

/**
 * @brief Writes a single byte to a specific register on an I2C slave device.
 * @param slave_addr The 7-bit I2C address of the slave.
 * @param reg_addr The register address to write to.
 * @param data The 8-bit data to write.
 * @return true if the write was successful, false otherwise.
 */
bool I2c_WriteReg(uint8_t slave_addr, uint8_t reg_addr, uint8_t data);

#endif // I2C_H
