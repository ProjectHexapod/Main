/* ------------------------ System includes ------------------------------- */
#include "stdlib.h"
#include "mcu_init.h"

/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"

/* ------------------------ LWIP includes --------------------------------- */
#include "lwip/api.h"
#include "lwip/tcpip.h"
#include "lwip/memp.h"

/* ------------------------ Application includes -------------------------- */
#include "http_server.h"
#include "uart_bridge.h"
#include "uif_terminal.h"
#include "sdcard_main.h"
#include "spi_bridge.h"
#include "serial_configuration.h"
#include "email_client.h"
#include "ftp_server.h"
#include "utilities.h"

/*b06862: Dec/10/2009: startup changes*/

/*********************************Prototypes**********************************/

static void 
start_tasks();

/*********************************Functions***********************************/

/**
 * Main Routine: calls all inits
 *
 * @param none 
 * @return none
 */
void 
main(void) 
{
    /*FSL: independent platform standard init*/
    MCU_startup();
    
    /*TCP/IP stack init*/
    vlwIPInit(  );

    /*FSL:start the applications*/
    start_tasks();
            
    /* Now all the tasks have been started - start the scheduler. */
    vTaskStartScheduler();
    
    /* please make sure that you never leave main */
    for(;;)
    ;
}

/**
 * Starts tasks to be schedulled by FreeRTOS
 *
 * @param none 
 * @return none
 */
static void 
start_tasks()
{
#if 1
#if 1
    /* Always start the webserver */
    ( void )sys_thread_new("WEB", HTTP_Server_Task, NULL, WEBSERVER_STACK_SPACE, HTTP_TASK_PRIORITY );
    /*configuration mode*/
    if( !(uint8)board_get_bridge_configuration() )
    {
      /* Start the FTP server: FAT + SDcard */
      ( void )sys_thread_new("FTP", vBasicFTPServer, NULL, FTPSERVER_STACK_SPACE, FTP_TASK_PRIORITY );
      
      /*Serial configuration: UART & SPI*/   
      xTaskCreate( vSerialBridgeConfiguration, (const signed portCHAR *)"CONF", SRL_BRIDGE_BUFFER_LIMIT, NULL, SERIAL_BRIDGE_TASK_PRIORITY, NULL );      
    }
    else
    {
       if( (uint8)board_get_bridge_tcp_mode() == 0 )/*UART*/
       {
         /*UART-Ethernet Bridge*/
         ( void )sys_thread_new("SCI", BRIDGE_UART_Task, NULL, UART_BRIDGE_STACK_SPACE, UART_TASK_PRIORITY );        
       }
       else if( (uint8)board_get_bridge_tcp_mode() == 1 )/*SPI*/
       {
         /*SPI-Ethernet Bridge*/
         ( void )sys_thread_new("SPI", BRIDGE_SPI_Task, NULL, SPI_BRIDGE_STACK_SPACE, SPI_BRIDGE_TASK_PRIORITY );
       }
       else
       {
         /*I2C-Ethernet Bridge*/
         //WIP
       }      
    }
#else
    //Example: SDcard example
    xTaskCreate( vSDCardExample, (const signed portCHAR *)"SDC", SDCARD_STACK_SPACE, NULL, SDCARD_TASK_PRIORITY, NULL );    
 
    //Example: serial terminal
    xTaskCreate( vBasicSerialTerminal, (const signed portCHAR *)"UIF", TERMINAL_STACK_SPACE, NULL, TERMINAL_TASK_PRIORITY, NULL );
#endif
#endif
}

/*-----------------------------------------------------------*/
#if 0
/**
 * Callback if a task's stack is overflow
 *
 * @param task
 * @param task's name
 * @return none
 */
void vApplicationStackOverflowHook( xTaskHandle *pxTask, signed portCHAR *pcTaskName )
{
	/* This will get called if a stack overflow is detected during the context
	switch.  Set configCHECK_FOR_STACK_OVERFLOWS to 2 to also check for stack
	problems within nested interrupts, but only do this for debug purposes as
	it will increase the context switch time. */

	( void ) pxTask;
	( void ) pcTaskName;

	for( ;; )
	;/*infinite loop*/
}
#endif