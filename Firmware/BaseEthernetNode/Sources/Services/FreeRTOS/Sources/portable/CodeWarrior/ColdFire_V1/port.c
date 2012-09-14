/*
	FreeRTOS.org V5.0.3 - Copyright (C) 2003-2008 Richard Barry.

	This file is part of the FreeRTOS.org distribution.

	FreeRTOS.org is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 2 of the License, or
	(at your option) any later version.

	FreeRTOS.org is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with FreeRTOS.org; if not, write to the Free Software
	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

	A special exception to the GPL can be applied should you wish to distribute
	a combined work that includes FreeRTOS.org, without being obliged to provide
	the source code for any proprietary components.  See the licensing section
	of http://www.FreeRTOS.org for full details of how and when the exception
	can be applied.

    ***************************************************************************
    ***************************************************************************
    *                                                                         *
    * SAVE TIME AND MONEY!  We can port FreeRTOS.org to your own hardware,    *
    * and even write all or part of your application on your behalf.          *
    * See http://www.OpenRTOS.com for details of the services we provide to   *
    * expedite your project.                                                  *
    *                                                                         *
    ***************************************************************************
    ***************************************************************************

	Please ensure to read the configuration and relevant port sections of the
	online documentation.

	http://www.FreeRTOS.org - Documentation, latest information, license and
	contact details.

	http://www.SafeRTOS.com - A version that is certified for use in safety
	critical systems.

	http://www.OpenRTOS.com - Commercial support, development, porting,
	licensing and training services.
*/

/* Kernel includes. */
#include "FreeRTOS.h"
#include "task.h"


#define portINITIAL_FORMAT_VECTOR		( ( portSTACK_TYPE ) 0x4000 )

/* Supervisor mode set. */
#define portINITIAL_STATUS_REGISTER		( ( portSTACK_TYPE ) 0x2000)

/* The clock prescale into the timer peripheral. */
#define portPRESCALE_VALUE				( ( unsigned portCHAR ) 10 )

/* The clock frequency into the RTC. */
#define portRTC_CLOCK_HZ				( ( unsigned portLONG ) 1000 )

asm void __declspec(register_abi) interrupt VectorNumber_VL1swi vPortYieldISR( void );
static void prvSetupTimerInterrupt( void );

/* Used to keep track of the number of nested calls to taskENTER_CRITICAL().  This
will be set to 0 prior to the first task being started. */
static unsigned portLONG ulCriticalNesting = 0x9999UL;

/*-----------------------------------------------------------*/

portSTACK_TYPE *pxPortInitialiseStack( portSTACK_TYPE * pxTopOfStack, pdTASK_CODE pxCode, void *pvParameters )
{
#ifndef STANDARD_PASSING
  unsigned portLONG ulOriginalA5;

	__asm{ MOVE.L A5, ulOriginalA5 };
	
	
	*pxTopOfStack = (portSTACK_TYPE) 0xDEADBEEF;
	pxTopOfStack--;

	/* Exception stack frame starts with the return address. */
	*pxTopOfStack = ( portSTACK_TYPE ) pxCode;
	pxTopOfStack--;

	*pxTopOfStack = ( portINITIAL_FORMAT_VECTOR << 16UL ) | ( portINITIAL_STATUS_REGISTER );
	pxTopOfStack--;

	*pxTopOfStack = ( portSTACK_TYPE ) 0x0; /*FP*/
	pxTopOfStack -= 14; /* A5 to D0. */
	
	/* Parameter in A0. */
	*( pxTopOfStack + 8 ) = ( portSTACK_TYPE ) pvParameters;
	
	/* A5 must be maintained as it is resurved by the compiler. */
	*( pxTopOfStack + 13 ) = ulOriginalA5;

    return pxTopOfStack;
#else  
	*pxTopOfStack = ( portSTACK_TYPE ) pvParameters;
	pxTopOfStack--;

	*pxTopOfStack = (portSTACK_TYPE) 0/*0xDEADBEEF*/;
	pxTopOfStack--;

	/* Exception stack frame starts with the return address. */
	*pxTopOfStack = ( portSTACK_TYPE ) pxCode;
	pxTopOfStack--;

	*pxTopOfStack = ( portINITIAL_FORMAT_VECTOR << 16UL ) | ( portINITIAL_STATUS_REGISTER );
	pxTopOfStack--;

	*pxTopOfStack = ( portSTACK_TYPE ) 0x0; /*FP*/
	pxTopOfStack -= 14; /* A5 to D0. */

  return pxTopOfStack;  
#endif    
}
/*-----------------------------------------------------------*/

portBASE_TYPE xPortStartScheduler( void )
{
extern void vPortStartFirstTask( void );

	ulCriticalNesting = 0UL;

	/* Configure a timer to generate the tick interrupt. */
	prvSetupTimerInterrupt();

	/* Start the first task executing. */
	vPortStartFirstTask();

	return pdFALSE;
}
/*-----------------------------------------------------------*/

static void prvSetupTimerInterrupt( void )
{

	/* 1KHz clock. */
	RTCSC |= 8;

	RTCMOD = portRTC_CLOCK_HZ / configTICK_RATE_HZ;
	
	/* Enable the RTC to generate interrupts - interrupts are already disabled
	when this code executes. */
	RTCSC_RTIE = 1;

#if 0
const unsigned portSHORT usCompareMatchValue = ( unsigned portSHORT ) ( ( configCPU_CLOCK_HZ / portPRESCALE_VALUE ) / configTICK_RATE_HZ );

	/* Bus rate clock. */
	TPM1SC_CLKSA = 1;
	TPM1SC_CLKSB = 0;
	
	/* Prescale by 32. */
	TPM1SC_PS0 = 1;
	TPM1SC_PS1 = 0;
	TPM1SC_PS2 = 1;
	
	TPM1MODH = ( unsigned portCHAR ) ( usCompareMatchValue >> ( unsigned portLONG ) 8 );
	TPM1MODL = ( unsigned portCHAR ) ( usCompareMatchValue & ( unsigned portLONG ) 0xff );
	
	/* Clear any pending interrupts. */
	TPM1SC &= ~( portTPM_TOF_BIT );
	
	/* Enable the interrupt.  Interrupts are already disabled when this 
	function is called. */
	TPM1SC_TOIE = 1;
	TPM1C1SC_CH1IE = 1;	
#endif
}
/*-----------------------------------------------------------*/

void vPortEndScheduler( void )
{
	/* Not implemented as there is nothing to return to. */
}
/*-----------------------------------------------------------*/

void vPortEnterCritical( void )
{
	if( ulCriticalNesting == 0UL )
	{
		/* Guard against context switches being pended simultaneously with a
		critical section being entered. */
		do
		{
			portDISABLE_INTERRUPTS();
			if( INTC_FRC == 0UL )
			{
				break;
			}

			portENABLE_INTERRUPTS();

		} while( 1 );
	}
	ulCriticalNesting++;
}
/*-----------------------------------------------------------*/

void vPortExitCritical( void )
{
	ulCriticalNesting--;
	if( ulCriticalNesting == 0 )
	{
		portENABLE_INTERRUPTS();
	}
}
/*-----------------------------------------------------------*/

void vPortYieldHandler( void )
{
unsigned portLONG ulSavedInterruptMask;

	ulSavedInterruptMask = portSET_INTERRUPT_MASK_FROM_ISR();
	{
		/* Note this will clear all forced interrupts - this is done for speed. */
		INTC_FRC = 0;
		vTaskSwitchContext();
	}
	portCLEAR_INTERRUPT_MASK_FROM_ISR( ulSavedInterruptMask );
}
/*-----------------------------------------------------------*/
 // JWHONG HACKERY
#if 0
void interrupt VectorNumber_Vrtc vPortTickISR( void )
{
unsigned portLONG ulSavedInterruptMask;

	/* Clear the interrupt. */
	RTCSC |= RTCSC_RTIF_MASK;

  //__RESET_WATCHDOG(); /* feeds the dog */

	/* Increment the RTOS tick. */
	ulSavedInterruptMask = portSET_INTERRUPT_MASK_FROM_ISR();
	{
		vTaskIncrementTick();
	}
	portCLEAR_INTERRUPT_MASK_FROM_ISR( ulSavedInterruptMask );

	/* If we are using the pre-emptive scheduler then also request a
	context switch as incrementing the tick could have unblocked a task. */
	#if configUSE_PREEMPTION == 1
	{
		taskYIELD();
	}
	#endif
}
#endif
