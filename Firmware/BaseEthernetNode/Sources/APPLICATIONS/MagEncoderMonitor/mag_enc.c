/*
 * A simple server/client socket interfacing the tcp/ip stack directly:
 * b06862
 *
 * Features:
 *   session is not closed until client does it first: TODO: automatic close
 *   SERIAL side sends if: at least a character is ready AND a 1/2 second has occurred.
 *   tcp packet length sent from the client only depends on client
 *   serial buffers lengths were selected according to performance and limits in memory
 *   will drop characters if internal queue is full
 */

/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"
#include "sockets.h"

/* ------------------------ Project includes ------------------------------ */
#include "mag_enc.h"
#include "spi_rtos.h"
#include "setget.h"

/*****************************************************************************/

// global mutex to prevent thread conflicts for lwip
extern xSemaphoreHandle lwip_mutex;

/*buffer to hold received spi information*/
static signed portCHAR *spi_receive_array;

/*Handle for SPI capabilities*/
xSPIPortHandle SPIhandle;

/*Mutex to MAC buffers*/
xSemaphoreHandle SPImutex;

/**
 * Mag Enc task
 *
 * @param none  
 * @return none
 */
void
MAG_ENC_Task( void *pvParameters )
{
	static uint8 i;
	int send_sock;
	struct sockaddr_in* target;
	uint32 gateway_addr;

	gateway_addr = board_get_eth_gateway();
	
	target = (struct sockaddr_in*)mem_malloc(sizeof(struct sockaddr_in));
	target->sin_family = AF_INET;
	target->sin_len    = sizeof(gateway_addr);
	target->sin_port   = 1544;
	target->sin_addr.s_addr = gateway_addr; 
	
    /*SPI array space*/
	/* 3 bytes is all that is required for mag enc */
    if( (spi_receive_array = ( static int8 * )mem_malloc( 3 )) == NULL )
    {
      vTaskDelete(NULL);
    }
    
    /*FSL: create mutex for shared resource*/
    SPImutex = xSemaphoreCreateMutex();
    
    /*wait until ip stack has a valid IP address*/
	while( get_lwip_ready() == FALSE )
	{
	   /*Leave execution for 100 ticks*/
	   vTaskDelay(100);
	}
	while( !xSemaphoreTake(lwip_mutex, 1) )
	    			;
    // Create a socket to blast UDP data out on
    if( (send_sock = lwip_socket(0x00, SOCK_DGRAM, IPPROTO_UDP)) == -1)
    {
    	vTaskDelete(NULL);
    }
    xSemaphoreGive(lwip_mutex);
    /**********************FSL: spi start-up*******************************/
    SPIhandle = xSPIinit(    (eSPIPort)board_get_spi_port(), 
                             (spiBaud)board_get_spi_baud(), 
                             (spiPolarity)board_get_spi_polarity()/*serIDLEslow*/, 
                             (spiPhase)board_get_spi_phase()/*serMiddleSample*/, 
                             (spiMode)board_get_spi_master()/*serMaster*/,
                             (spiInterrupt)board_get_spi_interrupt()/*serPolling*/,  
                             SPI_BUFFER_LIMIT/*defined at header file*/); 

    /**********************FSL: low level start-up****************************/

    // Set GPIO direction
    PTCD_PTCD4 = 0;
    PTCDD_PTCDD4 = 1;
    
	/* Loop forever */
	for( ;; )
	{
		while( !xSemaphoreTake(SPImutex, 1) )
			;
		// Activate CS
		PTCD_PTCD4 = 0;
		for( i=0; i < 3; i++ )
		{
			xSPIMasterSetGetChar(	SPIhandle,
									SPI_DONTCARE,  // Data to write
			        				(spi_receive_array + i), //Address to write to 
			        				portMAX_DELAY); //Timeout 
		}
		PTCD_PTCD4 = 1;
		if( lwip_interface_is_up() )
		{
			lwip_sendto(	send_sock, 	// Socket number
							(const void*)(spi_receive_array), // Buffer to send from 
							3, 			// Number of bytes to send
							0x00000000, // Flags
							(struct sockaddr*)target,		// Address to send to
							sizeof(struct sockaddr_in));	// Length of the address structure
		}
		xSemaphoreGive(SPImutex);
		/* Leave execution for 1 tick */
		/* Ends up running at 500Hz */
		vTaskDelay(1);
	}      
 
    return;/*FSL:never get here!!*/
}