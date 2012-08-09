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

#ifndef _SPI_RTOS_H
#define _SPI_RTOS_H

#include "queue.h"
#include "spi.h"

typedef void * xSPIPortHandle;

/*FSL: HIL layer glue logic*/
#define xSPISetBaudrate spi_set_baudrate
#define xSPIGetBaudrate spi_get_baudrate

#define xSPIEnableChipSelect       spi_enable_chip_select
#define xSPIDisableChipSelect      spi_disable_chip_select

#define SPI_DONTCARE               0xFF

typedef enum
{ 
	serSPI1, 
	serSPI2, 
	serSPI3, 
	serSPI4, 
	serSPI5, 
	serSPI6, 
	serSPI7, 
	serSPI8 
} eSPIPort;

typedef enum 
{ 
	serIDLEslow, 
	serIDLEshigh 
} spiPolarity;

typedef enum 
{ 
	serMiddleSample, 
	serStartSample  
} spiPhase;

typedef enum 
{ 
	spi12     = BAUD_12,    //12.2KHz
	spi50     = BAUD_50,	  //49KHz
	spi100    = BAUD_100,		//97KHz
	spi300    = BAUD_300,		//312KHz    
	spi500    = BAUD_500,   //520KHz    
	spi1000   = BAUD_1000,  //1.042Mhz    
	spi2000   = BAUD_2000,	//2.083MHz	  
	spi4200   = BAUD_4200,	//4.166MHz	  
	spi6250   = BAUD_6250,	//6.25MHz    
	spi12500  = BAUD_12500	//12.5MHz    
} spiBaud;

typedef enum
{
  serSlave,
  serMaster
} spiMode;

typedef enum
{
  serPolling,
  serInterrupt
} spiInterrupt;

typedef struct xSPI_PORT
{
    eSPIPort     sPort;   /* spi port address (0,1...) */

    /* Read/Write buffers */
    xQueueHandle xRxedChars;
    xQueueHandle xCharsForTx;
    
    /* SPI master/slave selector */
    spiMode xModeFlag;
    
    /* Polling/Interrupt flag */
    spiInterrupt xInterruptFlag;

} xSPIPort;

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
        unsigned portBASE_TYPE uxQueueLength);

/**
 * Change to polling support
 *
 * @param SPI handle to use      
 * @return none
 */
void
xSPIChangeToPolling(xSPIPortHandle xPort);

/**
 * Change to interrupt support
 *
 * @param SPI handle to use      
 * @return none
 */
void
xSPIChangeToInterruptMode(xSPIPortHandle xPort);
 
/**
 * Close SPI port
 *
 * @param SPI handle to use      
 * @return none
 */
void 
xSPIClose(xSPIPortHandle xPort);

/**
 * Send a character to SPI interface in Master Mode
 *
 * @param SPI handle to use      
 * @return none
 */
void 
xSPIMasterSendChar(xSPIPortHandle pxPort, portCHAR pcTxedChar);

/**
 * Receives a character from SPI interface in Master Mode
 *
 * @param SPI handle to use      
 * @return read character
 */
portCHAR 
xSPIMasterReceiveChar(xSPIPortHandle pxPort);

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
        portTickType xBlockTime);

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
        portTickType xBlockTime);

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
        portTickType xBlockTime);

/**
 * ISR for master or slave processing for either SPI port
 *
 * @param SPI port number to use      
 * @return none
 */
void
spi_isr(char ePort);
#endif