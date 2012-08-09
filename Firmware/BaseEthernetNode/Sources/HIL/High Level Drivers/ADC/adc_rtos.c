/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

#include "adc_rtos.h"
#include "adc.h"       /*ADC low level driver*/
#include "gpio.h"      /*GPIO Low level driver*/

static xADCPort xADCStatus;

/**
 * Initialize adc controller
 * @param channel may be either channel
 * @return ADC handle
 */
xADCPortHandle 
xADCInit(adcBits bits) 
{
    // Port struct
    xADCPort *port;
    
    /*taking xCOM pointer*/
    port = &xADCStatus;

    // Create the queues
    portENTER_CRITICAL();

    /*FSL: create semaphore*/
    vSemaphoreCreateBinary( port->xADCSemaphore );
    
    /*FSL: start ADC low level driver*/
    ADC_Init((uint8)bits);
    
    /*update number of bits*/
    port->sBits = bits;
        
    /*assign callback to be called by the ADC ISR*/
    ADC_assignCallback(ADC_ISR);
    
    portEXIT_CRITICAL();
    
    return (xADCPortHandle)port;
}

/**
 * Starts ADC controller channel
 *
 * @param ADC channel     
 * @return none
 */
void
xADCchannelInit(eADCchannel channel)
{
    /*init adc channel*/
    GPIO_ADCPinsInit((uint8)channel);
}

/**
 * ADC ISR
 *
 * @param ADC channel     
 * @return none
 */
void
ADC_ISR(void)
{
    portBASE_TYPE xHighPriorityTaskWoken = pdFALSE;
    
    /*clear adc controller flag*/
    ADC_CLEAR_IRQ_FLAG;
    
    /*unlock semaphore*/
    xSemaphoreGiveFromISR(xADCStatus.xADCSemaphore,&xHighPriorityTaskWoken);
    
/*Fault feature disabled*/      
adc_isr_exit:
    portEND_SWITCHING_ISR( xHighPriorityTaskWoken );
}