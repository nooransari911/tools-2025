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
