#include "cf_board.h"
#include "adc.h"
#include "gpio.h"

//global variable to contain ADC callback
static ADC_CallbackType adc_callback;

/**
 * ADC ISR assignation
 * @param callback function
 * @return none
 */
void 
ADC_assignCallback(void (*func)(void))
{
  adc_callback = func;
}

/**
 * ADC init. Can be called multiple times
 * @param none
 * @return none
 */ 
void
ADC_Init(uint8 bits)
{
 //if(!ADCCFG_ADLPC)/*using ADLPC as config loaded - if clear, configure*/
 //{
  DEMO_SELECTOR_ON;

  /*using asynch clock: ADACK = ~2MHz, long sample time, low power configuration*/
  ADCCFG = ADCCFG_ADLPC_MASK | ADCCFG_ADLSMP_MASK | (ADCCFG_ADICLK0_MASK | ADCCFG_ADICLK1_MASK);
  
  ADCSC2 = 0;/*software trigger, compare function disabled*/
  ADCSC1 = 0x1F;/*disable module*/
  
  /*write number of bits to use: default is 8 bits*/
#if 0  
  if(bits == 0)//8 bits
  {
    ADCCFG_MODE = 0;
  }
#endif  
  if(bits == 2)//10 bits
  {
    ADCCFG_MODE = 2;
  }
  else if(bits == 4)//12 bits
  {
    ADCCFG_MODE = 1;
  }
 //}  
}

/**
 * Start adn Get Result from a ADC Single Conversion Operation
 * @param adc channel
 * @return result
 */
uint16 
ADC_StartGetSingleConversion(uint8 channel)
{
  T16_8 var;
  
  /*one conversion*/
  //////ADCSC2 = 0;/*software trigger, compare function disabled*/
  //ADCSC1 = channel & 0x1F;
  ADCSC1_ADCH = channel;
    
  while(!ADCSC1_COCO)
  ;/*wait until conversion is over*/

  var.u8[0] = ADCRH;
  var.u8[1] = ADCRL;  
  
  return var.u16;
}

/**
 * Start continuous conversions
 * @param adc channel
 * @return none
 */
void
ADC_StartContinuousConversion(uint8 channel)
{
  ADCSC2 = 0;/*software trigger, compare function disabled*/
  /*configure continuos conversion*/
  ADCSC1 = ADCSC1_ADCO_MASK | (ADCSC1_ADCH4_MASK | ADCSC1_ADCH3_MASK | ADCSC1_ADCH2_MASK | ADCSC1_ADCH1_MASK | ADCSC1_ADCH0_MASK);  
  /*start conversions*/
  ADCSC1_ADCH = channel & 0x1F;
}

/**
 * Get a result from an ADC continuous conversions
 * @param none
 * @return none
 */
uint16
ADC_GetContinuousConversion(void)
{
  T16_8 var;
  
  var.u8[0] = ADCRH;
  var.u8[1] = ADCRL;  
  
  return var.u16;
}

/**
 * stop ADC continuous conversions operation
 * @param none
 * @return none
 */
void
ADC_StopContinuousConversion(void)
{
  ADCSC1 = 0x1F;
}

/**
 * Start an ADC compare result operation
 * @param adc channel
 * @param compare value to use
 * @param one to use greater than, zero for equal or less than  
 * @return none
 */
void
ADC_SetCompareValue(uint8 channel, uint16 compare_value, uint8 flag)
{
  T16_8 var;
  
  /*compare function enabled*/
  ADCSC2 = ADCSC2_ACFE_MASK;
  /*configure interrupts enabled*/
  ADCSC1 = ADCSC1_AIEN_MASK | (ADCSC1_ADCH4_MASK | ADCSC1_ADCH3_MASK | ADCSC1_ADCH2_MASK | ADCSC1_ADCH1_MASK | ADCSC1_ADCH0_MASK);
  
  if(flag)
  {
     ADCSC2_ACFGT = 1;/*greater than or equal to*/
  }/*then less than*/

  var.u16 = compare_value;

  ADCCVH = var.u8[0];
  ADCCVL = var.u8[1];  
  
  /*set channel and start comparison value*/
  ADCSC1_ADCH = channel;
}

/**
 * ADC ISR: calls ADC callback assigned
 * @param none 
 * @return none
 */
void interrupt VectorNumber_Vadc 
ADC_ISR_LowLevel( void )
{
    /* This ISR can cause a context switch, so the first statement must be
     * a call to the portENTER_SWITCHING_ISR() macro.
     */
    adc_callback();
}