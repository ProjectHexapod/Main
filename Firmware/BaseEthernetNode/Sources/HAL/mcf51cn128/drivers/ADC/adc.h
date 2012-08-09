#ifndef _ADC_H_
#define _ADC_H_

#define ADC_CLEAR_IRQ_FLAG               (void)ADCRL

typedef void(*ADC_CallbackType)(void);

/**
 * ADC ISR assignation
 * @param callback function
 * @return none
 */
void 
ADC_assignCallback(void (*func)(void));

/**
 * ADC init. Can be called multiple times
 * @param none
 * @return none
 */ 
void
ADC_Init(uint8 bits);

/**
 * Start adn Get Result from a ADC Single Conversion Operation
 * @param adc channel
 * @return result
 */
uint16 
ADC_StartGetSingleConversion(uint8 channel);

/**
 * Start continuous conversions
 * @param adc channel
 * @return none
 */
void
ADC_StartContinuousConversion(uint8 channel);

/**
 * Get a result from an ADC continuous conversions
 * @param none
 * @return none
 */
uint16
ADC_GetContinuousConversion(void);

/**
 * stop ADC continuous conversions operation
 * @param none
 * @return none
 */
void
ADC_StopContinuousConversion(void);

/**
 * Start an ADC compare result operation
 * @param adc channel
 * @param compare value to use
 * @param one to use greater than, zero for equal or less than  
 * @return none
 */
void
ADC_SetCompareValue(uint8 channel, uint16 compare_value, uint8 flag);

/**
 * ADC ISR: calls ADC callback assigned
 * @param none 
 * @return none
 */
void interrupt VectorNumber_Vadc 
ADC_ISR_LowLevel( void );

#endif