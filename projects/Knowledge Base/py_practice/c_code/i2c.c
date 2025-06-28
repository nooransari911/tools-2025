// i2c.c

#include "i2c.h"
#include "config.h"

// It is expected that the user will use the TI SysConfig tool to generate
// the ti_msp_dl_config.h file, which provides the necessary peripheral instances.
#include "ti_msp_dl_config.h"

void I2c_Init(void)
{
    // The SYSCFG_DL_init() function, called in main, has already configured
    // the I2C pins (SCL/SDA), enabled the peripheral's power, and set the bus clock.

    // This function ensures the peripheral is reset and enabled for operation.
    DL_I2C_reset(I2C_0_INST);
    DL_I2C_enable(I2C_0_INST);
}

bool I2c_WriteReg(uint8_t slave_addr, uint8_t reg_addr, uint8_t data)
{
    // Wait until the I2C bus is not busy to prevent collisions.
    while (DL_I2C_isControllerBusy(I2C_0_INST));

    // Prepare the payload: [register address, data byte]
    uint8_t payload[2] = {reg_addr, data};

    // Transmit the payload in a blocking manner.
    // The function handles START, addressing, data transmission, and STOP.
    DL_I2C_CONTROLLER_STATUS status = DL_I2C_transmitDataBlocking(
        I2C_0_INST,
        slave_addr,
        (uint8_t*)&payload,
        sizeof(payload),
        DL_I2C_CONTROLLER_FLAG_SEND_STOP
    );

    // Return true on success, false if the slave did not acknowledge.
    return !(status & DL_I2C_CONTROLLER_STATUS_NACK_RECEIVED);
}
