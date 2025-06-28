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
