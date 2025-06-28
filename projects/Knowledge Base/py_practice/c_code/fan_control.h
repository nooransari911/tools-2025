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
