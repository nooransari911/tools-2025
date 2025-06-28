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
