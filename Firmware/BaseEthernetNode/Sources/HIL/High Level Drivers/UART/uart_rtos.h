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

#ifndef _UART_RTOS_H
#define _UART_RTOS_H

#include "queue.h"
#include "uart.h"

#define RX_HANDLER        0/*rx*/
#define TX_HANDLER        1/*tx*/

#ifndef UART_RTOS_DEBUG
#define UART_RTOS_DEBUG   0/*OFF!!*/
#endif /*UART_RTOS_DEBUG*/

typedef void * xComPortHandle;

typedef enum
{ 
	serCOM1, 
	serCOM2, 
	serCOM3, 
	serCOM4, 
	serCOM5, 
	serCOM6, 
	serCOM7, 
	serCOM8 
} eCOMPort;

typedef enum 
{ 
	serNO_PARITY, 
	serODD_PARITY, 
	serEVEN_PARITY, 
	serMARK_PARITY, 
	serSPACE_PARITY 
} eParity;

typedef enum 
{ 
	serSTOP_1, 
	serSTOP_2 
} eStopBits;

typedef enum 
{ 
	serBITS_5, 
	serBITS_6, 
	serBITS_7, 
	serBITS_8,
	serBITS_9 
} eDataBits;

typedef enum 
{ 
	ser50,//no		
	ser75,//no		
	ser110    = 110,		
	ser134    = 134,		
	ser150    = 150,    
	ser200    = 200,
	ser300    = 300,		
	ser600    = 600,		
	ser1200   = 1200,	
	ser1800   = 1800,	
	ser2400   = 2400,   
	ser4800   = 4800,
	ser9600   = 9600,		
	ser19200  = 19200,	
	ser38400  = 38400,	
	ser57600  = 57600,	
	ser115200 = 115200
} eBaud;

typedef enum
{
  serFlowControlNone,
  serFlowControlHardware,
  serFlowControlXONXOFF
} eFlowControl;

typedef enum
{
  rxIDLE,
  rxSTOP,
  rxWAITING,
  rxGO
} eCOMrxState;

typedef enum
{
  txGO,
  txSTOP
} eCOMtxState;

typedef enum
{
  serSemaphoreOFF,
  serSemaphoreON
} eCOMsemaphore;

typedef struct xCOM_PORT
{
    eCOMPort     sPort;   /* comm port address (0,1,2) */

    /* Read/Write buffers */
    xQueueHandle xRxedChars;
    xQueueHandle xCharsForTx;
    
    /* Flow control information*/
    eFlowControl xFlowControl;
    
    /*RTOS semaphore support during SCI RX*/
    eCOMsemaphore semaphoreState;
    
    /*state machine for xmit and rx full-duplex channels*/
    eCOMrxState  rx_state;
    eCOMtxState  tx_state;
} xComPort;


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
        eCOMsemaphore eCOMsem, unsigned portBASE_TYPE uxQueueLength);

/**
 * Close UART port
 *
 * @param UART handle      
 * @return none
 */ 
void 
xUARTclose(xComPortHandle xPort);

/**
 * Minimal Configuration in default mode: port1, 19200bps 8-N-1, No flow control and semaphore support
 *
 * @param buffer length      
 * @return UART handle 
 */
xComPortHandle 
xUARTinitMinimal(unsigned portBASE_TYPE uxQueueLength );

/**
 * Set UART buffer length
 *
 * @param port number      
 * @param buffer length
 * @return none 
 */
static void 
xUARTSetBufferLength(eCOMPort ePort, unsigned portBASE_TYPE uxQueueLength);

/**
 * Get UART buffer length
 *
 * @param port number      
 * @return buffer length
 */
static unsigned portBASE_TYPE 
xUARTGetBufferLength(eCOMPort ePort);

/**
 * Get a UART character with control flow if enabled
 *
 * @param UART handle
 * @param received character pointer 
 * @return 1 if character received, otherwise time expired
 */
signed portBASE_TYPE 
xUARTGetCharWithFlowControl(xComPortHandle pxPort,
        signed portCHAR *pcRxedChar);

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
        signed portCHAR *pcRxedChar, portTickType xBlockTime);

/**
 * Put a UART character in sending buffer
 *
 * @param UART handle
 * @param tx character
 * @param expiration time
 * @return false if after the block time there is no room on the Tx queue
 */ 
signed portBASE_TYPE 
xUARTPutChar(xComPortHandle pxPort, signed portCHAR cOutChar, portTickType xBlockTime);

/**
 * If a UART CTS signal is detected, change UART state machine
 *
 * @param UART handle
 * @return none
 */
inline uint8 
xUARThwFlowControlSignalStatus(xComPort *xPortStatus);

/**
 * sends XON under software flow control
 *
 * @param UART port
 * @return none
 */
static void
xUARTSetXON(CHAR ePort);

/**
 * Wait for software flow control character. XON or XOFF
 *
 * @param UART handle
 * @param received character
 * @return -1 if characer doesn't need to be queued, otherwise, queue it
 */
inline uint8 
xUARTReceiveSWcontrolFlowSignal(xComPort *xPortStatus, signed portCHAR cChar);

/**
 * UART TX ISR: handles TX state machine
 *
 * @param UART port
 * @return none
 */
void 
xUARTtxISR(CHAR ePort);

/**
 * UART RX ISR: handles RX state machine
 *
 * @param UART port
 * @return none
 */
void
xUARTrxISR(CHAR ePort);
#endif