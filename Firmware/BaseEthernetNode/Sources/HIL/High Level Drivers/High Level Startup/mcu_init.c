/* ------------------------ System includes ------------------------------- */
#include "mcu_init.h"
#include "mac_rtos.h"
#include "clock.h"

/**
 * Low level call to init hardware
 *
 * @param none 
 * @return none
 */
void 
MCU_startup()
{
   /*basic MCU startup*/
   MCU_init();

   /*FSL: init flash once*/  
   FlashInit();
   
   return;
}

/**
 * set targeted MCU
 *
 * @param none
 * @return none
 */
void
MCU_reset(void)
{
  MCU_low_level_reset();
}