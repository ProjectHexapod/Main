/*
 * Copyright (c) 2006 Christian Walter
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote products
 *    derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
 * SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
 * IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
 * OF SUCH DAMAGE.
 *
 * Author: Christian Walter <wolti@sil.at>
 *
 * TODO:
 *  - Avoid copying the buffers - this requires changing the nbuf driver code
 *    to use the lwIP pbuf buffer implementation!!!
 *
 * Changes: b06862 (06/16/2008)
 */

/* ------------------------ Platform includes ----------------------------- */
#include "cf_board.h"

#include "mac_rtos.h"
#include "fec.h"
#include "mii.h"

/* ------------------------ Defines --------------------------------------- */
#ifdef FEC_DEBUG

/*FSL: not implemented*/
#define FEC_DEBUG_INIT 			     /*FSL:configure pin as output*/
#define FEC_DEBUG_RX_TIMING( x ) /*FSL:set or clear a pin for debugging purposes*/
#define FEC_DEBUG_TX_TIMING( x ) /*FSL:set or clear a pin for debugging purposes*/

#else
#define FEC_DEBUG               DBG_OFF
#define FEC_DEBUG_INIT
#define FEC_DEBUG_RX_TIMING( x )
#define FEC_DEBUG_TX_TIMING( x )
#endif

#define MCF_FEC_MTU             ( 1518 )
#define ETH_ADDR_LEN            ( 6 )
#define FEC_TASK_PRIORITY       ( configMAX_PRIORITIES - 1 )
#define FEC_TX_TIMEOUT			    0xFFFFFF

/* ------------------------ Static variables ------------------------------ */

extern void interpretCommandBuffer( unsigned char* payload, unsigned short rx_len, unsigned char* tx_payload, unsigned short* tx_len );

/* ------------------------ Static functions ------------------------------ */

/**
 * Reset MAC controller
 *
 * @param MAC controller descriptor
 * @return none
 */
static void     MAC_Reset( struct eth_addr *mac );

/**
 * Enable MAC controller
 *
 * @param MAC interface descriptor      
 * @return none
 */
void
MAC_Enable(  );

/**
 * Stops MAC controller
 *
 * @param MAC interface descriptor      
 * @return none
 */
void
MAC_disable(  );

/* ------------------------ Start implementation -------------------------- */

/**
 * FEC ISR
 *
 * @param none
 * @return none
 */
void 
MAC_ISR(void)
{
	nbuf_t         *pNBuf;
	nbuf_t		   *pNBufTX;
	unsigned char *pPayLoad;
	
	Cpu_DisableInt();
	
    /* Set Debug PIN to high to measure RX latency. */
    FEC_DEBUG_RX_TIMING( 1 );

    /* Clear FEC RX Event from the Event Register (by writing 1) */
    if( FEC_GetAvailableReadyRX() )
    {
        /* ACK interrupt flag */
        FEC_ackRX();
	
		while( NBUF_ReadyRX(  ) )
		{
			pNBuf = NBUF_AllocRX( );

			if( pNBuf != NULL )
			{
				/* This flags indicate that the frame has been damaged. In
				 * this case we must update the link stats if enabled and
				 * remove the frame from the FEC. */
				// FIXME: turn off CRC checking for now... it is throwing error even when I manually check the received packet
				// as byte-for-byte correct
				// FIXME part 2: CRC suddenly works again, don't know what changed.  Spooky.
				//if ( !(pNBuf->status & (RX_ERROR_ALL_FLAGS & ~RX_ERROR_CHKSM_FLAG)) )
				if ( !(pNBuf->status & RX_ERROR_ALL_FLAGS) )
				{
					// The frame must now be valid.
					// Now interpret the data.
					pPayLoad = pNBuf->data;
					/* Ethernet frame received. Handling it is not device
					 * dependent and therefore done in another function.
					 */
					/* wait until we have a free Tx buffer */
					while( (pNBufTX = NBUF_AllocTX() ) == NULL )
					{
						
					}
					interpretCommandBuffer(pPayLoad, pNBuf->length, pNBufTX->data, &(pNBufTX->length));

					/* Set Frame ready for transmission. */
					NBUF_ReadyTx( pNBufTX );
					/* Mark the buffer as not in use so the FEC can take it. */
					NBUF_ReleaseTX( pNBufTX );
					/* Indicate that a new transmit buffer has been produced. */
					FEC_ReadyTx();	
				}
				/*release the buffer under any circumstance*/
				
				/*now we can release buffer*/
				NBUF_ReleaseRX( pNBuf );

				/* Tell the HW that there are new free RX buffers. */
				FEC_ReadyRX();
			}
		}
		/* Set RX Debug PIN to low since handling of next frame is possible. */
		FEC_DEBUG_RX_TIMING( 0 );
	}
    Cpu_EnableInt();	
}

/**
 * Reset MAC controller
 *
 * @param MAC controller descriptor
 * @return none
 */
void
MAC_Reset( struct eth_addr *mac )
{
    Cpu_DisableInt();

    /* Set the source address for the controller */
    FEC_ResetProcessing((unsigned char*)mac);

    /* Enable Debug support */
    FEC_DEBUG_INIT;
    FEC_DEBUG_RX_TIMING( 0 );
    FEC_DEBUG_TX_TIMING( 0 );
    
    Cpu_EnableInt()
    

}

/**
 * Enable MAC controller
 *
 * @param MAC interface descriptor      
 * @return none
 */
void
MAC_Enable(  )
{
    Cpu_DisableInt();
    
    //( void )fecif;

    /* Configure I/O pins for the FEC. */
    FEC_LowLevelEnable();

    Cpu_EnableInt();
}

/**
 * Stops MAC controller
 *
 * @param MAC interface descriptor      
 * @return none
 */
void
MAC_disable(  )
{
    portENTER_CRITICAL();

    //( void )fecif;

    FEC_LowLevelDisable();

    /* Disable I/O pins used by the FEC. */
    PINS_DISABLE();
    
    portEXIT_CRITICAL();
}


/**
 * Starts MAC controller
 *
 * @param MAC interface descriptor      
 * @return error code
 */
unsigned char
MAC_init( struct eth_addr *mac )
{
    unsigned char     res;

	NBUF_init(  );        
	MAC_Reset( mac );                       

	FEC_SetRxCallback(MAC_ISR);
	MAC_Enable(  );

	res = ERR_OK;

    return res;
}

