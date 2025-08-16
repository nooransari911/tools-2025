======== ./fan_control.h ========
#ifndef FAN_CONTROL_H
#define FAN_CONTROL_H

#include <stdint.h>

/**
 * @brief Initializes the fan control logic (e.g., sets initial speed).
 */
void FanControl_Init(void);

/**
 * @brief Processes the latest ADC data to update fan speed and check for faults.
 * @param vac_sense_raw The raw ADC value from the Vac_Sense pin.
 * @param current_sense_raw The raw ADC value from the CS pin.
 */
void FanControl_Process(uint16_t vac_sense_raw, uint16_t current_sense_raw);

#endif // FAN_CONTROL_H


======== ./adc.c ========
// adc.c

#include "adc.h"
#include "fan_control.h"
#include "config.h"
#include "ti_msp_dl_config.h"

// Static global buffer to store results from DMA transfer.
// 'volatile' is critical to ensure the compiler doesn't optimize away access.
static volatile ADC_Results g_adcResults = {0, 0};

void Adc_Init(void)
{
    // It is expected that the user will use the TI SysConfig tool to generate
    // the peripheral configurations. This function orchestrates them.

    // 1. POWER, CLOCKS, and IOMUX are assumed to be configured by SYSCFG_DL_init().

    // 2. CONFIGURE DMA CHANNEL 0
    //    - Source: ADC0.MEMRES[0] (start of result registers)
    //    - Destination: g_adcResults struct in SRAM
    //    - Size: 2 (for two 16-bit results)
    //    - Mode: Single transfer per trigger
    // These actions are typically configured in a generated DL_DMA_init() function.
    // We must manually set the destination address at runtime.
    DL_DMA_setDestAddr(DMA, DMA_CH0_CHAN_ID, (uint32_t)&g_adcResults);
    DL_DMA_enableChannel(DMA, DMA_CH0_CHAN_ID);
    DL_DMA_enableInterrupt(DMA, DL_DMA_INTERRUPT_CHANNEL0);

    // 3. CONFIGURE TIMER to trigger ADC at ADC_TIMER_FREQUENCY_HZ
    //    - The period/load value would be calculated based on MCLK and prescaler
    //    - e.g., LoadValue = (SYSTEM_CLOCK_HZ / PRESCALER) / ADC_TIMER_FREQUENCY_HZ - 1;
    //    - Configure the timer's event publisher (e.g., on Zero event).
    //    These are set up in the generated DL_TimerG_init().

    // 4. CONFIGURE ADC
    //    - Set trigger source to the timer's event.
    //    - Set up a sequence of channels from MEM0 to MEM1.
    //    - Map physical pins to these sequence steps (MEM0 -> A0, MEM1 -> A1).
    //    - Enable the ADC and the end-of-sequence trigger for the DMA.
    //    This is set up in the generated DL_ADC12_init().

    // 5. ENABLE NVIC for DMA interrupts
    NVIC_EnableIRQ(DMA_INT_IRQn);

    // 6. START THE TRIGGER TIMER
    DL_TimerG_startCounter(TIMER_0_INST);
}

const ADC_Results* Adc_GetResults(void)
{
    return (const ADC_Results*)&g_adcResults;
}

// DMA Interrupt Service Routine
// The function name must match the name in the startup file (e.g., startup_mspm0c110x_ccs.c)
void DMA_IRQHandler(void)
{
    // Best practice to check for the specific interrupt source
    switch (DL_DMA_getPendingInterrupt(DMA)) {
        case DL_DMA_INTERRUPT_CHANNEL0:
            // The DMA has already transferred the ADC results to g_adcResults.
            // Now, run the application logic to process these new values.
            FanControl_Process(g_adcResults.vac_sense_raw, g_adcResults.current_sense_raw);
            break;
        default:
            // Unexpected DMA interrupt
            break;
    }
}


======== ./config.h ========
#ifndef CONFIG_H
#define CONFIG_H

// --- System Configuration ---
#define SYSTEM_CLOCK_HZ         24000000UL // 24 MHz MCLK
#define ADC_TIMER_FREQUENCY_HZ  16         // 1/16th of a second for sampling

// --- ADC Configuration ---
#define ADC_VREF_V              2.5f       // 2.5V internal reference
#define ADC_RESOLUTION_BITS     12
#define ADC_MAX_VALUE           ((1 << ADC_RESOLUTION_BITS) - 1) // 4095 for 12-bit

// --- Channel Mapping (Assumed from schematic and datasheet)---
#define VAC_SENSE_ADC_CHANNEL   0  // PA27/A0 maps to ADC0.IN0
#define CURRENT_SENSE_ADC_CHANNEL 1  // PA1/NRST maps to ADC0.IN1

// --- Speed Control Logic ---
#define VAC_SENSE_MAX_V         2.5f       // Voltage corresponding to 265 Vac
#define VAC_SENSE_MAX_VAC       265.0f     // 265 Vac
#define VAC_SPEED_HIGH_THRESHOLD_VAC 200.0f    // Above this, speed is pinned to max
#define VAC_SPEED_LOW_THRESHOLD_VAC  30.0f     // Below this, speed is 0

// --- "Efficiency Mode" PWM Cap ---
#define PWM_MAX_EFFICIENT_DUTY  0xF0       // Cap PWM at 240/255 for efficiency

// --- I2C Configuration ---
#define FAN_CONTROLLER_I2C_ADDRESS 0x52
#define FAN_SPEED_REGISTER         0x00

// --- Current Sense (CS) Logic ---
#define CS_MV_PER_WATT          69.0f      // 69mV per Watt
#define MAX_POWER_WATT          100.0f     // Example: 100W safety threshold

#endif // CONFIG_H


======== ./i2c.h ========
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


======== ./adc.h ========
#ifndef ADC_H
#define ADC_H

#include <stdint.h>
#include <stdbool.h>

// Struct to hold the results from the ADC sequence.
// `volatile` is used to prevent the compiler from optimizing away reads.
typedef struct {
    volatile uint16_t vac_sense_raw;
    volatile uint16_t current_sense_raw;
} ADC_Results;

/**
 * @brief Initializes Timer, ADC, and DMA for periodic sampling.
 */
void Adc_Init(void);

/**
 * @brief Returns a constant pointer to the internal ADC results buffer.
 * @return const ADC_Results* Pointer to the results.
 */
const ADC_Results* Adc_GetResults(void);

#endif // ADC_H


======== ./fan_control.c ========
// fan_control.c

#include "fan_control.h"
#include "i2c.h"
#include "config.h"

// --- Static Function Prototypes (Private to this file) ---
static float ConvertRawToVac(uint16_t raw_adc);
static uint8_t MapVacToPwm(float vac);
static void CheckOverCurrent(uint16_t raw_cs);

// --- Public Function Implementations ---

void FanControl_Init(void)
{
    // Set an initial safe state (fan off) at startup.
    I2c_WriteReg(FAN_CONTROLLER_I2C_ADDRESS, FAN_SPEED_REGISTER, 0x00);
}

void FanControl_Process(uint16_t vac_sense_raw, uint16_t current_sense_raw)
{
    float current_vac;
    uint8_t pwm_duty;

    // Process Vac_Sense to determine speed
    current_vac = ConvertRawToVac(vac_sense_raw);
    pwm_duty = MapVacToPwm(current_vac);

    // Send the new speed command via I2C
    // In a production system, one might check the return value.
    I2c_WriteReg(FAN_CONTROLLER_I2C_ADDRESS, FAN_SPEED_REGISTER, pwm_duty);

    // Process Current Sense for closed-loop control (e.g., safety shutdown)
    CheckOverCurrent(current_sense_raw);
}

// --- Static Function Implementations ---

static float ConvertRawToVac(uint16_t raw_adc)
{
    float voltage;
    float vac;
    
    // Convert the 12-bit ADC result to a voltage level
    voltage = ((float)raw_adc / (float)ADC_MAX_VALUE) * ADC_VREF_V;
    
    // Scale the measured voltage to the full AC voltage range
    vac = (voltage / VAC_SENSE_MAX_V) * VAC_SENSE_MAX_VAC;
    
    return vac;
}

static uint8_t MapVacToPwm(float vac)
{
    // Clamp to the lower threshold
    if (vac < VAC_SPEED_LOW_THRESHOLD_VAC) {
        return 0x00;
    }
    // Clamp to the upper threshold and apply efficiency cap
    if (vac > VAC_SPEED_HIGH_THRESHOLD_VAC) {
        return PWM_MAX_EFFICIENT_DUTY;
    }

    // Linearly interpolate the PWM duty cycle for the 30V-200V range
    float vac_range = VAC_SPEED_HIGH_THRESHOLD_VAC - VAC_SPEED_LOW_THRESHOLD_VAC;
    float normalized_vac = (vac - VAC_SPEED_LOW_THRESHOLD_VAC) / vac_range;
    
    uint8_t pwm = (uint8_t)(normalized_vac * (float)PWM_MAX_EFFICIENT_DUTY);
    
    return pwm;
}

static void CheckOverCurrent(uint16_t raw_cs)
{
    float cs_voltage;
    float power_watts;

    cs_voltage = ((float)raw_cs / (float)ADC_MAX_VALUE) * ADC_VREF_V;
    
    // Calculate power using the specified sensitivity (69 mV/W)
    power_watts = (cs_voltage * 1000.0f) / CS_MV_PER_WATT;

    if (power_watts > MAX_POWER_WATT) {
        // Over-current condition detected. For safety, stop the fan.
        I2c_WriteReg(FAN_CONTROLLER_I2C_ADDRESS, FAN_SPEED_REGISTER, 0x00);
        // Additional error handling (e.g., setting a fault LED) could go here.
    }
}


======== ./i2c.c ========
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


======== ./main.c ========
// main.c

#include "i2c.h"
#include "adc.h"
#include "fan_control.h"
#include "ti_msp_dl_config.h"

int main(void)
{
    // The SYSCFG_DL_init() function is generated by the TI SysConfig tool.
    // It is responsible for critical low-level setup including:
    // - Clock system initialization
    // - Power configuration
    // - Pin Muxing for all used peripherals (I2C_0, ADC_0, etc.)
    SYSCFG_DL_init();

    // Initialize our hardware abstraction layer modules.
    // These functions configure the peripherals for their specific roles in this application.
    I2c_Init();
    Adc_Init();

    // Initialize the application logic module.
    FanControl_Init();
    
    // Enable global interrupts. This allows the DMA IRQ to be processed by the CPU.
    __enable_irq();

    // The system is now fully interrupt-driven. The main loop simply enters a
    // low-power state, waiting for an interrupt to occur.
    while (1) {
        // __WFI() puts the CPU to sleep. It will wake up when the DMA
        // completes its transfer and fires the interrupt. The ISR will run,
        // and then execution will return here to go back to sleep.
        __WFI();
    }
}


