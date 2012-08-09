#ifndef _FLASH_H_
#define _FLASH_H_
  
#define FLASH_MASS_ERASE_CMD  0x41
#define FLASH_ERASE_CMD       0x40
#define FLASH_PROGRAM_CMD     0x20
#define FLASH_BURST_CMD       0x25
  
#if (SYSTEM_CLOCK/2) > 12800000 /* 12.8 MHz */
    #define FLASH_CLOCK (uint8)(( (SYSTEM_CLOCK/3200000) -1) | 0x40)
#else
    #define FLASH_CLOCK (unsigned char)( (SYSTEM_CLOCK/400000) -1)//<200KHz
#endif
  
/* Macros to call the function using the different features */
#define Flash_Erase(Address) \
          Flash_Cmd((uint32)Address, (uint16)1, (uint32*)ROM_ADDRESS, FLASH_ERASE_CMD)
  
#define Flash_Program(Address, Data) \
          Flash_Cmd((uint32)Address, (uint16)1, (uint32*)&Data, FLASH_PROGRAM_CMD)
  
#define Flash_Burst(Address, Size, DataPtr) \
          Flash_Cmd((uint32)Address, (uint16)Size, (uint32*)DataPtr, FLASH_BURST_CMD)

/****************************Prototypes***************************************/
          
/**
 * Start FLASH controller init
 * @param none
 * @return none
 */
void 
FlashInit(void);

/**
 * Execute Flash command at runtime: must run at another FLASH block 
 * that is being modified. Usually from RAM
 * @param flash address to modify
 * @param flash number of longwords to modify
 * @param flash data pointer
 * @param flash command  
 * @return none
 */
uint8 
Flash_Cmd(uint32 FlashAddress, 
          uint16 FlashDataCounter, 
          uint32 *pFlashDataPtr, 
          uint8 FlashCommand);

#endif