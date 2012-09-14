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
#include "api.h"

/* ------------------------ Project includes ------------------------------ */
#include "mag_enc.h"
#include "spi_rtos.h"
#include "setget.h"
#include "mem.h"

/*****************************************************************************/

// global mutex to prevent thread conflicts for lwip
extern xSemaphoreHandle lwip_mutex;

/*buffer to hold received spi information*/
static signed portCHAR *spi_receive_array;

/*Handle for SPI capabilities*/
extern xSPIPortHandle SPIhandle;

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
	struct netconn* send_conn;
	struct netbuf* send_buf;
	struct ip_addr target_addr;
	int8*  spi_receive_array;
	
    /*SPI array space*/
	/* 3 bytes is all that is required for mag enc */
    if( (spi_receive_array = ( int8 * )mem_malloc( 3 )) == NULL )
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

    /* Create a new UDP connection handle. */
    send_conn = netconn_new(NETCONN_UDP);
    send_buf  = netbuf_new();
    
    // Set target IP
    target_addr.addr = board_get_eth_gateway();
    send_buf->addr = &target_addr;
    send_buf->port = 1544;
	
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
			// TODO: There will be filtering and intelligence here,
			// but for now just blindly copy what we get over SPI
			// Point the netbuf at the data we want to send
			netbuf_ref(send_buf, spi_receive_array, 3);
			netconn_send( send_conn, send_buf );
		}
		xSemaphoreGive(SPImutex);
		/* Leave execution for 1 tick */
		/* Ends up running at 500Hz */
		vTaskDelay(1);
	}      
 
    return;/*FSL:never get here!!*/
}