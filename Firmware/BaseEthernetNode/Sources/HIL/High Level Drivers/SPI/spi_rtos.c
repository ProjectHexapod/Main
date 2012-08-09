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

#include "spi_rtos.h"
#include "spi.h"       /*SPI low level driver*/

static xSPIPort xPortStatus[NUMBER_OF_SPIs];

/*Semaphore to wake up task*/
xSemaphoreHandle xSPISemaphore;

/***************************Functions*****************************************/

/**
 * Starts SPI port
 *
 * @param SPI port 
 * @param SPI baudrate
 * @param SPI polarity
 * @param SPI phase
 * @param SPI master or slave support
 * @param SPI interrupt or polling
 * @param SPI buffer length      
 * @return SPI handle
 */
xSPIPortHandle 
xSPIinit(eSPIPort ePort, spiBaud eWantedBaud,
        spiPolarity eWantedPolarity, spiPhase eWantedPhase,
        spiMode eWantedMasterSlave,
        spiInterrupt eWantedInterrupt,
        unsigned portBASE_TYPE uxQueueLength) 
{
    // Port struct
    xSPIPort *port;
    
    /*taking xCOM pointer*/
    port = &xPortStatus[ePort];
    
    /*assign elements*/
    port->sPort = ePort;

    /*interrupt allowance*/
    port->xInterruptFlag = eWantedInterrupt;

    // Create the queues
    portENTER_CRITICAL();

    /*create queues even if interrupts are not enabled to switch to/from polling/interrupt*/

    /*check if enough memory is available*/
    if((port->xRxedChars  = xQueueCreate(uxQueueLength, (unsigned portBASE_TYPE) sizeof(signed portCHAR))) == NULL )
    {
      return NULL;
    }
    if((port->xCharsForTx = xQueueCreate(uxQueueLength, (unsigned portBASE_TYPE) sizeof(signed portCHAR))) == NULL )
    {
      return NULL;
    }

    /*FSL: start SPI low level driver*/
    spi_init((uint8)ePort, 
              (uint16)eWantedBaud, 
              (uint8)eWantedPolarity, 
              (uint8)eWantedPhase, 
              (uint8)eWantedMasterSlave
              );
    
    port->xModeFlag = eWantedMasterSlave;
    
    /*assign callback to be called by the SPI ISR*/
    spi_assign_call_back((uint8)ePort,spi_isr);
    
    /*SPI ISR: for slave rx interrupt is always enabled*/    
    if( port->xInterruptFlag == serInterrupt || port->xModeFlag == serSlave )
    {
      spi_enable_rx_interrupt ((uint8)ePort);      
    }    
    
    spi_disable_tx_interrupt ((uint8)ePort);
    
    portEXIT_CRITICAL();
    
    return (xSPIPortHandle)port;
}

/**
 * Change to polling support
 *
 * @param SPI handle to use      
 * @return none
 */
void
xSPIChangeToPolling(xSPIPortHandle xPort)
{
    ((xSPIPort *)xPort)->xInterruptFlag = serPolling;
    spi_disable_rx_interrupt((uint8)((xSPIPort *)xPort)->sPort);
}

/**
 * Change to interrupt support
 *
 * @param SPI handle to use      
 * @return none
 */
void
xSPIChangeToInterruptMode(xSPIPortHandle xPort)
{
    ((xSPIPort *)xPort)->xInterruptFlag = serInterrupt;
    spi_enable_rx_interrupt((uint8)((xSPIPort *)xPort)->sPort);
}
 
/**
 * Close SPI port
 *
 * @param SPI handle to use      
 * @return none
 */
void 
xSPIClose(xSPIPortHandle xPort) 
{
    portENTER_CRITICAL();
    // TX int 
    spi_disable_tx_interrupt((uint8)((xSPIPort *)xPort)->sPort);
    // RX int
    spi_disable_rx_interrupt((uint8)((xSPIPort *)xPort)->sPort);
    
    portEXIT_CRITICAL();
    
    /*FSL: delete allocated memory for Tx and Rx queues*/
    vPortFree(((xSPIPort *)xPort)->xCharsForTx);
    vPortFree(((xSPIPort *)xPort)->xRxedChars);
    
    return;
}

/**
 * Send a character to SPI interface in Master Mode
 *
 * @param SPI handle to use      
 * @return none
 */
void 
xSPIMasterSendChar(xSPIPortHandle pxPort, portCHAR pcTxedChar)
{
    signed portCHAR pcRxedChar;/*don't care*/
        
    xSPIMasterSetGetChar(pxPort, pcTxedChar, &pcRxedChar, portMAX_DELAY);
    
    return;
}

/**
 * Receives a character from SPI interface in Master Mode
 *
 * @param SPI handle to use      
 * @return read character
 */
portCHAR 
xSPIMasterReceiveChar(xSPIPortHandle pxPort)
{
    signed portCHAR pcRxedChar;
        
    xSPIMasterSetGetChar(pxPort, SPI_DONTCARE, &pcRxedChar, portMAX_DELAY);
    
    return pcRxedChar;
}

/**
 * Get and Set the next character from the SPI buffer
 *
 * @param SPI handle to use
 * @param character to send
 * @param character to receive
 * @param expire time         
 * @return one if everything's fine, otherwise zero
 */ 
signed portBASE_TYPE 
xSPIMasterSetGetChar(xSPIPortHandle pxPort,
        signed portCHAR pcTxedChar, signed portCHAR *pcRxedChar, 
        portTickType xBlockTime) 
{    
  if(((xSPIPort *)pxPort)->xInterruptFlag == serInterrupt)
  {
      //TX
      if ( xQueueSend(((xSPIPort *)pxPort)->xCharsForTx, &pcTxedChar, xBlockTime ) != pdPASS)
      {
         return pdFAIL;
      }
      spi_enable_tx_interrupt((uint8)((xSPIPort *)pxPort)->sPort);//Enable TX
      //RX
      if ( xQueueReceive(((xSPIPort *)pxPort)->xRxedChars, pcRxedChar, xBlockTime) != pdPASS)
      {
         return pdFAIL;
      }
  }
  else
  {
      spi_send_receive_waiting((portCHAR)((xSPIPort *)pxPort)->sPort,pcTxedChar,(unsigned portCHAR *)pcRxedChar);  
  }  
  
  return pdTRUE;
}

/**
 * Receives a character from SPI interface in Slave Mode
 *
 * @param SPI handle to use      
 * @param received character
 * @return one if everything's fine, otherwise zero
 */ 
signed portBASE_TYPE 
xSPISlaveReceiveChar(xSPIPortHandle pxPort,
        signed portCHAR *pcRxedChar, 
        portTickType xBlockTime) 
{
  /*dequeue if there is a character available*/
  if ( xQueueReceive(((xSPIPort *)pxPort)->xRxedChars, pcRxedChar, xBlockTime) != pdPASS)
  {
     return pdFAIL;
  }
  
  return pdTRUE;
}

/**
 * Sends a character to SPI interface in Slave Mode
 *
 * @param SPI handle to use      
 * @param tx character
 * @return one if everything's fine, otherwise zero
 */ 
signed portBASE_TYPE 
xSPISlaveSendChar(xSPIPortHandle pxPort,
        signed portCHAR pcTxedChar, 
        portTickType xBlockTime) 
{    
  /*if spi controller buffer has space*/
  if( spi_is_tx_buffer_empty((portCHAR)((xSPIPort *)pxPort)->sPort) )
  {
      /*Push directly to SPI data buffer*/
      spi_putchar((portCHAR)((xSPIPort *)pxPort)->sPort,pcTxedChar);
  }
  /*if spi controller buffer is full*/
  else
  {
      //TX: queue if it's possible
      if ( xQueueSend(((xSPIPort *)pxPort)->xCharsForTx, &pcTxedChar, xBlockTime ) != pdPASS)
      {
         return pdFAIL;
      }    
  }    
  return pdTRUE;
}

/**
 * ISR for master or slave processing for either SPI port
 *
 * @param SPI port number to use      
 * @return none
 */
void
spi_isr(char ePort)
{
  signed portCHAR cChar;
  portBASE_TYPE xHighPriorityTaskWoken = pdFALSE;	

  /*SPI RX processing: means a Tx was sent*/
  if(spi_is_rx_buffer_full(ePort))//RX
  {  
     cChar = spi_getchar(ePort);
     
     /*FSL:try to queue it, if not space then character is dropped!!!*/
     xQueueSendFromISR(xPortStatus[ePort].xRxedChars, ( const void * )&cChar, &xHighPriorityTaskWoken);  
  }
  /*SPI TX processing: means there is free space*/
  else if(spi_is_tx_buffer_empty(ePort))
  {
     /*something to dequeue?*/
     if( xQueueReceiveFromISR(xPortStatus[ePort].xCharsForTx, &cChar, &xHighPriorityTaskWoken ) == pdPASS )
     {
       spi_putchar(ePort,cChar);
     }
     else/*selector between master or slave processing*/
     {
        if( xPortStatus[ePort].xModeFlag == serMaster)
        {
           /*turn off spi tx empty space interrupt*/
           spi_disable_tx_interrupt(ePort);          
        }
        else/*slave: serSlave*/
        {
           /*write don't care byte for next transfer*/
           spi_putchar(ePort,SPI_DONTCARE);
        }
     }
  }
  
  /*unlock semaphore if needed*/
  if(xPortStatus[ePort].xModeFlag == serSlave)
  {
     /*unblock process if needed*/
     xSemaphoreGiveFromISR(xSPISemaphore,&xHighPriorityTaskWoken);
  }
  
  /*Fault feature disabled*/      
spi_isr_exit:
  portEND_SWITCHING_ISR( xHighPriorityTaskWoken );  
}