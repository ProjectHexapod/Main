/*
 * File:
 *
 * Notes:       
 *              
 */
#include "cf_board.h"
#include "flash.h"

/**
 * Start FLASH controller init
 * @param none
 * @return none
 */                              
void 
FlashInit(void)
{
#if 0
  const byte NVPROT_INIT @0x0000040D = 0xFF
  const byte NVOPT_INIT @0x0000040F = 0xC3;
  
  const byte NVBACKKEY0_INIT @0x00000400 = 0;
  const byte NVBACKKEY1_INIT @0x00000401 = 0;
  const byte NVBACKKEY0_INIT @0x00000402 = 0;
  const byte NVBACKKEY1_INIT @0x00000403 = 0;
  const byte NVBACKKEY0_INIT @0x00000404 = 0;
  const byte NVBACKKEY1_INIT @0x00000405 = 0;
  const byte NVBACKKEY0_INIT @0x00000406 = 0;
  const byte NVBACKKEY1_INIT @0x00000407 = 0;
#endif
  
  if (!(FCDIV & FCDIV_FDIVLD_MASK))
  {
    /*set flash freq*/
    FCDIV = FLASH_CLOCK;
  }
}

/**
 * Execute Flash command at runtime: must run at another FLASH block 
 * that is being modified. Usually from RAM
 * @param flash address to modify
 * @param flash number of longwords to modify
 * @param flash data pointer
 * @param flash command  
 * @return none
 */
__relocate_code__
uint8 /*far*/ 
Flash_Cmd(uint32 FlashAddress, 
          uint16 FlashDataCounter, 
          uint32 *pFlashDataPtr, 
          uint8 FlashCommand)
{
    /* Check to see if FACCERR or PVIOL is set */
    if (FSTAT&0x30)  
    {         
        /* Clear Flags if set*/
        FSTAT = 0x30;  
    }

    if (FlashDataCounter)
    {
      do
      {
          /* Wait for the Last Busrt Command to complete */
          while(!(FSTAT&FSTAT_FCBEF_MASK))
          {
            __RESET_WATCHDOG(); /* feeds the dog */
          }/*wait until termination*/
          
          /* Write Data into Flash*/
          (*((volatile unsigned long *)(FlashAddress))) = *pFlashDataPtr;
          FlashAddress += 4;
          pFlashDataPtr++;
          
          /* Write Command */
          FCMD = FlashCommand;
          
          /* Put FCBEF at 1 */
          FSTAT = FSTAT_FCBEF_MASK;
          
          asm(nop);
          asm(nop);
          asm(nop);
          asm(nop);
          
          /* Check if Flash Access Error or Protection Violation Error are Set */
          if (FSTAT&0x30)
          {     
            /* If so, finish the function returning 1 to indicate error */
            return (1);
          }
          
      }while (--FlashDataCounter);
    }
    /* wait for the last command to complete */
    while ((FSTAT&FSTAT_FCCF_MASK)==0)
    ;/*wait until termination*/
    
    /* Return zero to indicate that the function executed OK */
    return (0);
}
