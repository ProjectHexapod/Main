#ifndef _ADC_RTOS_H_
#define _ADC_RTOS_H_

#include "adc.h"

#include "queue.h"

typedef void * xADCPortHandle;

typedef enum
{ 
	adcCH0, 
	adcCH1, 
	adcCH2, 
	adcCH3, 
	adcCH4, 
	adcCH5, 
	adcCH6, 
	adcCH7,
	adcCH8,
	adcCH9,
	adcCH10,
	adcCH11,
	adcCH12,
	adcCH13,
	adcCH14,
	adcCH15,
	adcCH16,
	adcCH17,
	adcCH18,
	adcCH19,
	adcCH20,
	adcCH21,
	adcCH22,
	adcCH23,
	adcCH24,
	adcCH25,
	adcCH26,
	adcCH27,
	adcCH28,
	adcCH29,
	adcCH30,
	adcCH31
} eADCchannel;

typedef enum 
{ 
	adcEightBits, 
	adcNineBits,
	adcTenBits,
	adcElevenBits,
	adcTwelveBits  
} adcBits;

typedef struct xADC_PORT
{
    /* Bits used by each conversion */
    adcBits     sBits;

    /*Semaphore to wake up task*/
    xSemaphoreHandle xADCSemaphore;
} xADCPort;

#define ADC_start_get_single_conversion   ADC_StartGetSingleConversion
#define ADC_start_continuous_conversion   ADC_StartContinuousConversion
#define ADC_get_continuous_conversion     ADC_GetContinuousConversion
#define ADC_stop_continuous_conversion    ADC_StopContinuousConversion
#define ADC_set_compare_value             ADC_SetCompareValue

/**
 * Initialize adc controller
 * @param channel may be either channel
 * @return ADC handle
 */
xADCPortHandle 
xADCInit(adcBits bits);

/**
 * Starts ADC controller channel
 *
 * @param ADC channel     
 * @return none
 */
void
xADCchannelInit(eADCchannel channel);

/**
 * ADC ISR
 *
 * @param ADC channel     
 * @return none
 */
void
ADC_ISR(void);

#endif