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
