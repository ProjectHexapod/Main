/*
 * SDcard Reader: example reading and writing to a SDcard using FAT16 file system
 */

/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

/* ------------------------ SDcard includes --------------------------------- */
#include "sdcard_main.h"

/* ------------------------ Project includes ------------------------------ */
#include "SD.h"         /* SD Card Driver (SPI mode) */
#include "FAT.h"

/*Handle SD card*/
static FATHandler *SDcardHandle;

UINT8 
sdcard_example(void *OUTHandle,UINT8* filename)
{
    (void)OUTHandle;
    (void)filename;
    /*continue operation*/
    return 1;
}

/*FSL: running task*/
void
vSDCardExample( void *pvParameters )
{
    //volatile UINT16 u16Length;
    //volatile UINT8 u8Error;

    /*Read Buffer for App*/
    UINT8 *u8TempBuffer;
    //UINT16 u16Length;
    
    volatile UINT8 i=0, j=0;
    
    /* Parameters are not used - suppress compiler error */
    ( void )pvParameters;
    
    /*recycling buffer space due to low RAM space*/
    if( (u8TempBuffer=(static uint8 *)pvPortMalloc( BLOCK_SIZE )) != NULL )
    {
      /* SD Card Initialization */
      if( (SDcardHandle = FAT_INIT(u8TempBuffer)) == NULL )
      {
        /*delete requested memory*/
        vPortFree(u8TempBuffer);
        /*error*/
        FAT_Close();
      }
    }
    else
    {
      /*delete requested memory*/
      vPortFree(u8TempBuffer);        
    }
    
    /*list files*/
    i = FAT_LS(SDcardHandle,u8TempBuffer,NULL,sdcard_example);
    
#if 0
    /*Read File*/
    u8Error=FAT_FileOpen(SDcardHandle,u8TempBuffer,(uint8 *)"ONE.TXT",READ);
    while( (u16Length=FAT_FileRead(SDcardHandle,u8TempBuffer)) == BLOCK_SIZE)
    {
       /*BLOCK reading*/
       asm(nop);
       i++;/*counter*/
    }
    if(u16Length)
    {
       /*less than a BLOCK reading*/
       asm(nop);
       i++;/*counter*/
    }

    /*Write File: remaining bits: doesn't check for file names' duplication*/
    u8Error=FAT_FileOpen(SDcardHandle,u8TempBuffer,(uint8 *)"VIERNES.TXT",CREATE);
    FAT_FileWrite(SDcardHandle,u8TempBuffer,u8TempBuffer,u16Length);
    FAT_FileClose(SDcardHandle,u8TempBuffer);
#endif
    ///* Loop forever */
    //for( ;; )
    //{
    //  
    //}
    /*Task no longer needed, delete it!*/
    vTaskDelete( NULL );
      
    return;/*FSL:never get here!!*/
}