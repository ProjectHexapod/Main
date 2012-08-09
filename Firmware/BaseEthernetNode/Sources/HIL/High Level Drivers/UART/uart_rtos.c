/*
	FreeRTOS.org V4.7.0 - Copyright (C) 2003-2007 Richard Barry.

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
	See http://www.FreeRTOS.org for documentation, latest information, license 
	and contact details.  Please ensure to read the configuration and relevant 
	port sections of the online documentation.

	Also see http://www.SafeRTOS.com a version that has been certified for use
	in safety critical systems, plus commercial licensing, development and
	support options.
	***************************************************************************
*/
/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

#include "uart_rtos.h"
#include "uart.h"       /*UART low level driver*/

static xComPort xPortStatus[NUMBER_OF_SCIs];

/*buffer length*/
static uint16 buffer_length[NUMBER_OF_SCIs];

#if UART_RTOS_DEBUG
uint16 rx_char_counter = 0;
uint16 xon_counter = 0;
uint16 xoff_counter = 0;
#endif

/*Semaphore to wake up task*/
xSemaphoreHandle xUARTSemaphore;

/***************************Functions*****************************************/

/**
 * Starts UART port
 *
 * @param UART port 
 * @param UART baudrate
 * @param UART parity
 * @param UART data bits
 * @param UART stop bits
 * @param UART flow control: hw or sw
 * @param UART semaphore support 
 * @param UART buffer length      
 * @return UART handle
 */
xComPortHandle 
xUARTinit(eCOMPort ePort, eBaud eWantedBaud,
        eParity eWantedParity, eDataBits eWantedDataBits,
        eStopBits eWantedStopBits, eFlowControl eWantedFlowControl,
        eCOMsemaphore eCOMsem, unsigned portBASE_TYPE uxQueueLength) 
{
    // Port struct
    xComPort *port;
    
    /*taking xCOM pointer*/
    port = &xPortStatus[ePort];
    
    /*assign elements*/
    port->sPort = ePort;
    /*flow control*/
    port->xFlowControl = eWantedFlowControl;
    port->rx_state = rxIDLE;
    port->tx_state = txGO;
    port->semaphoreState = eCOMsem;

    // Create the queues
    portENTER_CRITICAL();
    
    /*assig global variable: for the rx queue*/
    xUARTSetBufferLength(ePort, uxQueueLength>>1);
    
    /*check if enough memory is available*/
    if((port->xRxedChars  = xQueueCreate(uxQueueLength>>1, (unsigned portBASE_TYPE) sizeof(signed portCHAR))) == NULL )
    {
      return NULL;
    }
    if((port->xCharsForTx = xQueueCreate(uxQueueLength, (unsigned portBASE_TYPE) sizeof(signed portCHAR))) == NULL )
    {
      return NULL;
    }

    /*FSL: start low level UART driver*/
    uart_init((uint8)ePort, 
              (uint32)eWantedBaud, 
              (uint8)eWantedParity, 
              (uint8)eWantedDataBits, 
              (uint8)eWantedStopBits,
              (uint8)eWantedFlowControl//uart low level driver needs to know this!!
              );
    
    /*assign callback to be called by the SCI ISR*/
    uart_assign_call_back(RX_HANDLER, xUARTrxISR);
    uart_assign_call_back(TX_HANDLER, xUARTtxISR);
    
    /*SCI ISR*/
    uart_enable_rx_interrupt ((uint8)ePort);
    uart_disable_tx_interrupt ((uint8)ePort);

    portEXIT_CRITICAL();
    
    return (xComPortHandle)port;
}

/**
 * Close UART port
 *
 * @param UART handle      
 * @return none
 */ 
void 
xUARTclose(xComPortHandle xPort) 
{
    portENTER_CRITICAL();
    // TX int
    uart_disable_tx_interrupt((uint8)((xComPort *)xPort)->sPort);
    // RX int
    uart_disable_rx_interrupt((uint8)((xComPort *)xPort)->sPort);
    portEXIT_CRITICAL();
    
    /*FSL: delete allocated memory for Tx and Rx queues*/
    vPortFree(((xComPort *)xPort)->xCharsForTx);
    vPortFree(((xComPort *)xPort)->xRxedChars);
    
    return;
}

/**
 * Minimal Configuration in default mode: port1, 19200bps 8-N-1, No flow control and semaphore support
 *
 * @param buffer length      
 * @return UART handle 
 */
xComPortHandle 
xUARTinitMinimal(unsigned portBASE_TYPE uxQueueLength ) 
{
    return xUARTinit(serCOM1, ser19200, serNO_PARITY, serBITS_8, serSTOP_1, serFlowControlNone, serSemaphoreON, uxQueueLength);
}

/**
 * Set UART buffer length
 *
 * @param port number      
 * @param buffer length
 * @return none 
 */
static void 
xUARTSetBufferLength(eCOMPort ePort, unsigned portBASE_TYPE uxQueueLength)
{
    buffer_length[(uint8)ePort] = uxQueueLength;
}

/**
 * Get UART buffer length
 *
 * @param port number      
 * @return buffer length
 */
static unsigned portBASE_TYPE 
xUARTGetBufferLength(eCOMPort ePort)
{
    return buffer_length[(uint8)ePort];
}

/**
 * Get a UART character with control flow if enabled
 *
 * @param UART handle
 * @param received character pointer 
 * @return 1 if character received, otherwise time expired
 */
signed portBASE_TYPE 
xUARTGetCharWithFlowControl(xComPortHandle pxPort,
        signed portCHAR *pcRxedChar)
{
    if (xQueueReceive(((xComPort *)pxPort)->xRxedChars, pcRxedChar, 0/*non-blocking*/)) 
    {
        return pdTRUE;
    } 
    else 
    {
        /*if no characters available, try to send XON if it's the right state*/
        xUARTSetXON((uint8)((xComPort *)pxPort)->sPort);
        return pdFALSE;
    }  
}

/**
 * Get a UART character
 *
 * @param UART handle
 * @param received character pointer
 * @param expire time  
 * @return 1 if character received, otherwise time expired
 */
signed portBASE_TYPE 
xUARTGetChar(xComPortHandle pxPort,
        signed portCHAR *pcRxedChar, portTickType xBlockTime) 
{
    if (xQueueReceive(((xComPort *)pxPort)->xRxedChars, pcRxedChar, xBlockTime)) 
    {
        return pdTRUE;
    } 
    else 
    {
        return pdFALSE;
    }
}

/**
 * Put a UART character in sending buffer
 *
 * @param UART handle
 * @param tx character
 * @param expiration time
 * @return false if after the block time there is no room on the Tx queue
 */ 
signed portBASE_TYPE 
xUARTPutChar(xComPortHandle pxPort, signed portCHAR cOutChar, portTickType xBlockTime) 
{
    if (xQueueSend(((xComPort *)pxPort)->xCharsForTx, &cOutChar, xBlockTime ) != pdPASS) 
    {
        return pdFAIL;
    }
    uart_enable_tx_interrupt((uint8)((xComPort *)pxPort)->sPort);
    return pdPASS;
}

/**
 * If a UART CTS signal is detected, change UART state machine
 *
 * @param UART handle
 * @return none
 */
inline uint8 
xUARThwFlowControlSignalStatus(xComPort *xPortStatus)
{
  if( (xPortStatus->xFlowControl ) == serFlowControlHardware )
  {
      /*stop tx communication*/
      if( uart_get_CTS_state((uint8)(xPortStatus->sPort))) 
      {
         xPortStatus->tx_state = txSTOP;
      }
      else//everything's fine or resume communication
      {
         xPortStatus->tx_state = txGO;
      }
  }
  return 0;  
}

/**
 * sends XON under software flow control
 *
 * @param UART port
 * @return none
 */
static void
xUARTSetXON(CHAR ePort)
{
  /*low watermark*/
  if( xPortStatus[ePort].rx_state == rxWAITING )
  {            
     /*FSL:set state first*/
     xPortStatus[ePort].rx_state = rxGO;
     /*FSL:outside of an ISR: then interrupt is raised almost immediately*/
     uart_enable_tx_interrupt(ePort);
  }
}

/**
 * Wait for software flow control character. XON or XOFF
 *
 * @param UART handle
 * @param received character
 * @return -1 if characer doesn't need to be queued, otherwise, queue it
 */
inline uint8 
xUARTReceiveSWcontrolFlowSignal(xComPort *xPortStatus, signed portCHAR cChar)
{
  if( (xPortStatus->xFlowControl ) == serFlowControlXONXOFF )
  {
     if( cChar == UART_XOFF )//XOFF received
     {
        xPortStatus->tx_state = txSTOP;        
        /*do not queue it!!*/
        return (uint8)-1;
     }
     else if( cChar == UART_XON )//XON received
     {
        xPortStatus->tx_state = txGO;        
        /*do not queue it!!*/
        return (uint8)-1;
     }
  }

  return 0;  
}

/**
 * UART TX ISR: handles TX state machine
 *
 * @param UART port
 * @return none
 */
void 
xUARTtxISR(CHAR ePort)
{
    signed portCHAR cChar;
    portBASE_TYPE xHighPriorityTaskWoken;
    
    if( ( xPortStatus[ePort].xFlowControl ) == serFlowControlHardware )
    {
       xUARThwFlowControlSignalStatus(&xPortStatus[ePort]);
    }
    
    /*works for both: HW and SW flow control!!*/
    switch(xPortStatus[ePort].rx_state)
    {
        case rxSTOP:
           //XOFF on Tx queue                           
           #if UART_RTOS_DEBUG
           xoff_counter++;              
           #endif           
           
           uart_send_tx_stop(ePort,xPortStatus[ePort].xFlowControl);
           xPortStatus[ePort].rx_state = rxWAITING;
           break;
        case rxGO:                      
           //XON on Tx queue            
           #if UART_RTOS_DEBUG
           xon_counter++;
           #endif
           
           uart_send_tx_go(ePort,xPortStatus[ePort].xFlowControl);
           xPortStatus[ePort].rx_state = rxIDLE;
           break;
        case rxIDLE:
        case rxWAITING:
           switch(xPortStatus[ePort].tx_state)
           {
               case txGO:
                  //send a regular character!!!
                  if (xQueueReceiveFromISR(xPortStatus[ePort].xCharsForTx, &cChar, &xHighPriorityTaskWoken ) == pdTRUE) 
                  {
                      //send the next character queued for Tx.
                      uart_putchar (ePort, cChar);
                  } 
                  else
                  { 
                      //queue empty, nothing to send, stop interrupt
                      uart_disable_tx_interrupt(ePort);
                  }               
                  break;
               case txSTOP:
               default:
                  //do not dequeue anything!!!
                  /*FSL:stop request from the other UART side*/
                  break;
           } 
        default:
           break;                      
    }
      
    portEND_SWITCHING_ISR( xHighPriorityTaskWoken );  
}

/**
 * UART RX ISR: handles RX state machine
 *
 * @param UART port
 * @return none
 */
void
xUARTrxISR(CHAR ePort)
{
	signed portCHAR cChar;
	portBASE_TYPE xHighPriorityTaskWoken = pdFALSE;
	uint16 used_chars;	

  /*FSL:always get character: non blocking*/
  cChar = uart_getchar(ePort);
  
  #if UART_RTOS_DEBUG
  rx_char_counter++;
  #endif
                 
  if( xUARTReceiveSWcontrolFlowSignal(&xPortStatus[ePort],cChar) )
  {
     /*do not queue it: XON and XOFF information sent to Tx ISR process*/
     goto exit_uart_rx_isr;
  }

  if(xPortStatus[ePort].semaphoreState == serSemaphoreON)
  {
     /*unblock process if needed*/
     xSemaphoreGiveFromISR(xUARTSemaphore,&xHighPriorityTaskWoken);
  }

#if 0//for debugging on high watermark
  /*debug: check if queue is full!!*/
  if(xQueueSendFromISR(xPortStatus[ePort].xRxedChars, ( const void * )&cChar, &xHighPriorityTaskWoken) 
     == errQUEUE_FULL)
  {
    /*assert: sw with flow control is not supposed to get here  */
    asm("halt");
  }
#else
  /*FSL:try to queue it, if not space then character is dropped!!!*/
  xQueueSendFromISR(xPortStatus[ePort].xRxedChars, ( const void * )&cChar, &xHighPriorityTaskWoken);
#endif
   
  /*character already enqueued*/
  
  /*flow control used: HW or SW*/
  if( ( xPortStatus[ePort].xFlowControl ) != serFlowControlNone )
  {          
     /*check state machine: SW flow control*/
     switch( xPortStatus[ePort].rx_state )
     {
        case rxIDLE:
        case rxGO:
            /*how many characters are still on queue?*/
            used_chars = uxQueueMessagesWaitingFromISR(xPortStatus[ePort].xRxedChars);

            /*FSL:high watermark: tested up to 115.2Kbps*/
            if(used_chars > (xUARTGetBufferLength(xPortStatus[ePort].sPort)-20))
            {              
              /*change state*/
              xPortStatus[ePort].rx_state = rxSTOP;              
              uart_enable_tx_interrupt(ePort);
            }         
            break;
        case rxSTOP:
        case rxWAITING:
        default:        
            break;                                    
     }    
  } 
      
exit_uart_rx_isr:  
  portEND_SWITCHING_ISR( xHighPriorityTaskWoken );  
}