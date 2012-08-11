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
#include "mag_enc.h"
#include "valve.h"
#include "utilities.h"

/*b06862: Dec/10/2009: startup changes*/

/*********************************Prototypes**********************************/

static void 
start_tasks();

// global mutex to prevent thread conflicts for lwip
xSemaphoreHandle lwip_mutex;

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

#if 0
    // PWM Init 
	/* TPM1SC: TOF=0,TOIE=0,CPWMS=0,CLKSB=0,CLKSA=0,PS2=0,PS1=0,PS0=0 */
	TPM1SC = 0x00;              /* Disable device */ 
	/* TPM1C2SC: CH2F=0,CH2IE=0,MS2B=1,MS2A=1,ELS2B=1,ELS2A=1,??=0,??=0 */
	TPM1C2SC = 0x3C;            /* Set up PWM mode with output signal level low */ 
	// 0x00FF MODULO ends up generating 96kHz PWM - good!
	/* TPM1MOD: BIT15=1,BIT14=1,BIT13=1,BIT12=1,BIT11=1,BIT10=1,BIT9=1,BIT8=1,BIT7=1,BIT6=1,BIT5=1,BIT4=1,BIT3=1,BIT2=1,BIT1=1,BIT0=1 */
	TPM1MOD = 0x00FF;          /* Set modulo register */ 
	/* TPM1SC: TOF=0,TOIE=0,CPWMS=0,CLKSB=0,CLKSA=1,PS2=0,PS1=0,PS0=0 */
	TPM1SC = 0x08;              /* Run the counter (set CLKSB:CLKSA) */ 
	/* PTEPF1: E5=3 */
	PTEPF1 |= 0x0C;
	
	// Set duty cycle 50%
	TPM1C2V = (word)(0x0080);
	
	// PWM Enable
	/* TPM1SC: TOF=0,TOIE=0,CPWMS=0,CLKSB=0,CLKSA=1,PS2=0,PS1=0,PS0=0 */
	TPM1SC = 0x08;              /* Run the counter (set CLKSB:CLKSA) */ 
	/* PTEPF1: E5=3 */
	PTEPF1 |= 0x0C;
#endif
	
	lwip_mutex = xSemaphoreCreateMutex();
	
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

    /* Always start the webserver */
    ( void )sys_thread_new("WEB", HTTP_Server_Task, NULL, WEBSERVER_STACK_SPACE, HTTP_TASK_PRIORITY );
    ( void )sys_thread_new("MAG", MAG_ENC_Task, 	NULL, MAG_ENC_STACK_SPACE, MAG_ENC_TASK_PRIORITY );
    ( void )sys_thread_new("VLV", VALVE_Task, 		NULL, VALVE_STACK_SPACE, VALVE_TASK_PRIORITY );
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