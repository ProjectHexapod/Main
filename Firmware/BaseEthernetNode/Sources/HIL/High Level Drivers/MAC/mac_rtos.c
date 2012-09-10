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

/* ------------------------ lwIP includes --------------------------------- */
#include "lwip/opt.h"
#include "lwip/def.h"
#include "lwip/mem.h"
#include "lwip/err.h"
#include "lwip/pbuf.h"
#include "lwip/sys.h"
#include "lwip/stats.h"
#include "lwip/debug.h"
#include "netif/etharp.h"

/********************************************************************/
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

/* ------------------------ Type definitions ------------------------------ */
typedef struct
{
    struct netif   *netif;      /* lwIP network interface. */
    struct eth_addr *self;      /* MAC address of FEC interface. */
    sys_sem_t       tx_sem;     /* Control access to transmitter. */
    sys_sem_t       rx_sem;     /* Semaphore to signal receive thread. */
} mcf5xxxfec_if_t;

/* ------------------------ Static variables ------------------------------ */
/*static volatile*/ mcf5xxxfec_if_t *fecif_g;

extern uint8 interface[128];

/* ------------------------ Static functions ------------------------------ */
static err_t    MAC_Send( struct netif *, struct pbuf *, struct ip_addr * );
static err_t    MAC_output_raw( struct netif *, struct pbuf * );

/**
 * Reset MAC controller
 *
 * @param MAC controller descriptor
 * @return none
 */
static void     MAC_Reset( mcf5xxxfec_if_t * fecif );

/**
 * Enable MAC controller
 *
 * @param MAC interface descriptor      
 * @return none
 */
void
MAC_Enable( mcf5xxxfec_if_t * fecif );

/**
 * Stops MAC controller
 *
 * @param MAC interface descriptor      
 * @return none
 */
void
MAC_disable( mcf5xxxfec_if_t * fecif );

//asm void        FEC_IsrError( void );

/* ------------------------ Start implementation -------------------------- */

/**
 * Output information thru Ethernet
 *
 * @param MAC interface descriptor
 * @param network buffer to send
 * @return error code
 */
err_t
MAC_output_raw( struct netif *netif, struct pbuf *p )
{
    err_t           res;
    nbuf_t          *pNBuf;
    mcf5xxxfec_if_t *fecif = netif->state;
    uint16          i;
    struct pbuf     *q;
    uint32 timeout = FEC_TX_TIMEOUT;

#if ETH_PAD_SIZE
    pbuf_header( p, -ETH_PAD_SIZE );    /* drop the padding word */
#endif

    /* Test if we can handle such big frames. If not drop it. */
    if( p->tot_len > MCF_FEC_MTU )
    {
#if LINK_STATS
        lwip_stats.link.lenerr++;
#endif
        res = ERR_BUF;
    }
    /* Test if our network buffer scheme can handle a packet of this size. If
     * not drop it and return a memory error. */
    else if( p->tot_len > TX_BUFFER_SIZE )
    {
#if LINK_STATS
        lwip_stats.link.memerr++;
#endif
        res = ERR_MEM;
    }
    /* Allocate a transmit buffer */
    else 
    {
	    /*FSL:don't block it. More packets produced than consumed*/
	    while( (pNBuf = NBUF_AllocTX() ) == NULL )
	    {
	    	if(!(timeout--))
	    	{
				LWIP_ASSERT( "MAC_output_raw: out of memory\n", FALSE );				
	    	}
	    }
		  /* wait until we have a free Tx buffer */

      q = p;
      i = 0;
      do
      {
          memcpy( &pNBuf->data[i], q->payload, q->len );
          i += q->len;
      }
      while( ( q = q->next ) != NULL );
      pNBuf->length = p->tot_len;

      /* Set Frame ready for transmission. */
      NBUF_ReadyTx( pNBuf );
      /* Mark the buffer as not in use so the FEC can take it. */
      NBUF_ReleaseTX( pNBuf );
      /* Indicate that a new transmit buffer has been produced. */
      FEC_ReadyTx();
#if LINK_STATS
      lwip_stats.link.xmit++;
#endif
      res = ERR_OK;
    }

    sys_sem_signal( fecif->tx_sem );
#if ETH_PAD_SIZE
    buf_header( p, ETH_PAD_SIZE );
#endif

    return res;
}

/**
 * Ethernet rx task being called periodically by FreeRTOS
 *
 * @param MAC interface descriptor
 * @return none
 */
void
MAC_Rx_Task(void *arg )
{
    mcf5xxxfec_if_t *fecif;
    struct pbuf    *p, *q;
    nbuf_t         *pNBuf;
    uint8          *pPayLoad;

    fecif = (mcf5xxxfec_if_t *)arg;

    do
    {    
    
        sys_sem_wait( fecif->rx_sem );
        while( NBUF_ReadyRX(  ) )
        {
            pNBuf = NBUF_AllocRX( );

            if( pNBuf != NULL )
            {
                /*FSL: removed to avoid get stuck if a BABR happens*/
                //LWIP_ASSERT( "MAC_Rx_Task: pNBuf->status & RX_BD_L ",
                //             pNBuf->status & RX_BD_L );

                /* This flags indicate that the frame has been damaged. In
                 * this case we must update the link stats if enabled and
                 * remove the frame from the FEC. */
                //if ( pNBuf->status & RX_ERROR_ALL_FLAGS )
            	// FIXME: turn off CRC checking for now... it is throwing error even when I manually check the received packet
            	// as byte-for-byte correct
                if ( pNBuf->status & (RX_ERROR_ALL_FLAGS & ~RX_ERROR_CHKSM_FLAG) )
                {
#if LINK_STATS
                    lwip_stats.link.drop++;
                    if ( pNBuf->status & RX_ERROR_LENGTH_FLAG )
                    {
                        lwip_stats.link.lenerr++;
                    }
                    else if ( pNBuf->status & RX_ERROR_CHKSM_FLAG )
                    {
                        lwip_stats.link.chkerr++;
                    }
                    else
                    {
                        lwip_stats.link.err++;
                    }
#endif
                }
                else
                {
                    /* The frame must now be valid. Perform some checks to see if the FEC
                     * driver is working correctly.
                     */
                    LWIP_ASSERT( "MAC_Rx_Task: pNBuf->length != 0", pNBuf->length != 0 );

					          p = pbuf_alloc( PBUF_RAW, pNBuf->length, PBUF_POOL );
					
					          if( p != NULL )
                    {						

#if ETH_PAD_SIZE
                        pbuf_header( p, -ETH_PAD_SIZE );
#endif

                        pPayLoad = pNBuf->data;
                        for( q = p; q != NULL; q = q->next )
                        {
                            memcpy( q->payload, pPayLoad, q->len );
                            pPayLoad += q->len;
                        }
#if ETH_PAD_SIZE
                        pbuf_header( p, ETH_PAD_SIZE );
#endif

                        /* Ethernet frame received. Handling it is not device
                         * dependent and therefore done in another function.
                         */
                        eth_input( fecif->netif, p );
                    }
                }
                /*release the buffer under any circumstance*/
                
                /*now we can release buffer*/
                NBUF_ReleaseRX( pNBuf );

                /* Tell the HW that there are new free RX buffers. */
                FEC_ReadyRX();
            }
            else
            {
#if LINK_STATS
                lwip_stats.link.memerr++;
                lwip_stats.link.drop++;
#endif
            }
        }
        /* Set RX Debug PIN to low since handling of next frame is possible. */
        FEC_DEBUG_RX_TIMING( 0 );
    }
    while( 1 );
}

/**
 * This function is called by the TCP/IP stack when an IP packet should be
 * sent. It uses the ethernet ARP module provided by lwIP to resolve the
 * destination MAC address. The ARP module will later call our low level
 * output function MAC_output_raw.
 *
 * @param MAC interface descriptor
 * @param network buffers
 * @param ip address to send ARP message
 * @return none
 */ 
err_t
MAC_Send( struct netif * netif, struct pbuf * p, struct ip_addr * ipaddr )
{
    err_t           res;
    mcf5xxxfec_if_t *fecif = netif->state;

    FEC_DEBUG_TX_TIMING( 1 );
    /* Make sure only one thread is in this function. */
    sys_sem_wait( fecif->tx_sem );
    res = etharp_output( netif, p, ipaddr );
    FEC_DEBUG_TX_TIMING( 0 );
    return res;
}

/**
 * FEC ISR
 *
 * @param none
 * @return none
 */
void 
MAC_ISR(void)
{
	//portBASE_TYPE xHighPriorityTaskWoken;
	mcf5xxxfec_if_t *fecif;
	struct pbuf    *p, *q;
	nbuf_t         *pNBuf;
	nbuf_t		   *pNBufTX;
	uint8          *pPayLoad;
	uint32			i;
	uint8			c, interface_i, block_len;
	
	//xSemaphoreGiveFromISR( fecif_g->rx_sem, &xHighPriorityTaskWoken );
	
	//xHighPriorityTaskWoken = pdFALSE;
    /* Set Debug PIN to high to measure RX latency. */
    FEC_DEBUG_RX_TIMING( 1 );

    /* Clear FEC RX Event from the Event Register (by writing 1) */
    if( FEC_GetAvailableReadyRX() )
    {
        /* ACK interrupt flag */
        FEC_ackRX();
        
        // JWHONG HACK: Short circuit and echo packets back out.
        
        fecif = fecif_g;
	
		while( NBUF_ReadyRX(  ) )
		{
			pNBuf = NBUF_AllocRX( );

			if( pNBuf != NULL )
			{
				/*FSL: removed to avoid get stuck if a BABR happens*/
				//LWIP_ASSERT( "MAC_Rx_Task: pNBuf->status & RX_BD_L ",
				//             pNBuf->status & RX_BD_L );

				/* This flags indicate that the frame has been damaged. In
				 * this case we must update the link stats if enabled and
				 * remove the frame from the FEC. */
				//if ( pNBuf->status & RX_ERROR_ALL_FLAGS )
				// FIXME: turn off CRC checking for now... it is throwing error even when I manually check the received packet
				// as byte-for-byte correct
				if ( !(pNBuf->status & (RX_ERROR_ALL_FLAGS & ~RX_ERROR_CHKSM_FLAG)) )
				{
					// The frame must now be valid.
					// Now interpret the data.
					// First check for magic number in the ethertype field
					// We arbitrarily designate 0x69
					pPayLoad = pNBuf->data;

					/* Ethernet frame received. Handling it is not device
					 * dependent and therefore done in another function.
					 */
					// JWHONG HACK:  Swap MACs so the reply goes back to the sender.
					//for(i = 0; i < 6; i++)
					//{
					//	pPayLoad[i  ] ^= pPayLoad[i+6];
					//	pPayLoad[i+6] ^= pPayLoad[i  ];
					//	pPayLoad[i  ] ^= pPayLoad[i+6];
					//}
					// Interpret the payload
					// Check for magic word
					//if(pPayLoad[12] != 0x69)
					//{
					//	goto MAC_ISR_FREE;
					//}
					/* wait until we have a free Tx buffer */
					while( (pNBufTX = NBUF_AllocTX() ) == NULL );
					// Start after the MAC and magic word
					// But before the CRC
					// TEMP HACK: Just load in a chunk of the interface block
					portDISABLE_INTERRUPTS();
					//memcpy(pPayLoad+12, interface, 24);
					
					memcpy( pNBufTX->data+ 0, pPayLoad+6,  6 );
					memcpy( pNBufTX->data+ 6, pPayLoad+0,  6 );
					memcpy( pNBufTX->data+12,  interface, 52 );
					portENABLE_INTERRUPTS();
					pNBufTX->length = 64;

					/* Set Frame ready for transmission. */
					NBUF_ReadyTx( pNBufTX );
					/* Mark the buffer as not in use so the FEC can take it. */
					NBUF_ReleaseTX( pNBufTX );
					/* Indicate that a new transmit buffer has been produced. */
					FEC_ReadyTx();				

					//p->len -= 4;
					//MAC_output_raw( fecif->netif, p );
					//p->len += 4;
					
					//pbuf_free(p);
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
    
    //portEND_SWITCHING_ISR( xHighPriorityTaskWoken );	
}

/**
 * Handles all ARP timeouts
 *
 * @param none
 * @return none
 */
static void
arp_timer( void *arg )
{
    ( void )arg;
    etharp_tmr(  );
    sys_timeout( ARP_TMR_INTERVAL, arp_timer, NULL );
}

/**
 * Handles all ethernet input from lwIP stacks
 *
 * @param MAC controller descriptor
 * @param buffer to send to upper layers
 * @return none
 */
void
eth_input( struct netif *netif, struct pbuf *p )
{
  struct ethernetif *ethernetif;
  struct eth_hdr *ethhdr;

  ethernetif = netif->state;

  /* no packet could be read, silently ignore this */
  if (p == NULL) return;
  /* points to packet payload, which starts with an Ethernet header */
  ethhdr = p->payload;

  switch (htons(ethhdr->type)) {
  /* IP or ARP packet? */
  case ETHTYPE_IP:
  case ETHTYPE_ARP:
#if PPPOE_SUPPORT
  /* PPPoE packet? */
  case ETHTYPE_PPPOEDISC:
  case ETHTYPE_PPPOE:
#endif /* PPPOE_SUPPORT */
    /* full packet send to tcpip_thread to process */
    if (netif->input(p, netif)!=ERR_OK)
     { LWIP_DEBUGF(NETIF_DEBUG, ("ethernetif_input: IP input error\n"));
       pbuf_free(p);
       p = NULL;
     }
    break;

  default:
    pbuf_free(p);
    p = NULL;
    break;
  }
}

/**
 * Reset MAC controller
 *
 * @param MAC controller descriptor
 * @return none
 */
void
MAC_Reset( mcf5xxxfec_if_t * fecif )
{
    portENTER_CRITICAL();

    /* Set the source address for the controller */
    FEC_ResetProcessing(fecif->self->addr);

    /* Enable Debug support */
    FEC_DEBUG_INIT;
    FEC_DEBUG_RX_TIMING( 0 );
    FEC_DEBUG_TX_TIMING( 0 );
    
    portEXIT_CRITICAL();
    

}

/**
 * returns MAC address
 *
 * @param MAC address holder
 * @return none
 */
void
MAC_GetMacAddress(struct eth_addr *mac )
{
    /*FSL: implemented at setget.c*/
    board_get_eth_ethaddr((uint8*)mac); 
}

/**
 * Enable MAC controller
 *
 * @param MAC interface descriptor      
 * @return none
 */
void
MAC_Enable( mcf5xxxfec_if_t * fecif )
{
    portENTER_CRITICAL();
    
    ( void )fecif;

    /* Configure I/O pins for the FEC. */
    FEC_LowLevelEnable();

    portEXIT_CRITICAL();
}

/**
 * Stops MAC controller
 *
 * @param MAC interface descriptor      
 * @return none
 */
void
MAC_disable( mcf5xxxfec_if_t * fecif )
{
    portENTER_CRITICAL();

    ( void )fecif;

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
err_t
MAC_init( struct netif *netif )
{
    err_t     res;
#if SPEED_10BASET    
    uint16 		mymrdata;  	//temp variable for MII read data
    //uint16		reg0;	
#endif
        
    mcf5xxxfec_if_t *fecif = (mcf5xxxfec_if_t *)mem_malloc( sizeof( mcf5xxxfec_if_t ) );

    if( fecif != NULL )
    {
        /* Global copy used in ISR. */
        fecif_g = fecif;
        fecif->self = ( struct eth_addr * )&netif->hwaddr[0];
        fecif->netif = netif;
        fecif->tx_sem = NULL;
        fecif->rx_sem = NULL;

        if( ( fecif->tx_sem = sys_sem_new( 1 ) ) == NULL )
        {
            res = ERR_MEM;
        }       
        else if( ( fecif->rx_sem = sys_mult_sem_new/*sys_sem_new*/( 0 ) ) == NULL )
        {
            res = ERR_MEM;
        }
        else if( 0 )//JWHONG HACKOUT sys_thread_new("FEC", MAC_Rx_Task, (void *)fecif, FEC_RX_STACK_SPACE, FEC_TASK_PRIORITY) == NULL )
        {
            res = ERR_MEM;
        }
        else
        {
            netif->state = fecif;
            netif->name[0] = 'C';
            netif->name[1] = 'F';
            netif->hwaddr_len = ETH_ADDR_LEN;
            netif->mtu = MCF_FEC_MTU;
            netif->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_LINK_UP;
            netif->output = MAC_Send;
            netif->linkoutput = MAC_output_raw;

            NBUF_init(  );
            MAC_GetMacAddress(fecif->self );        
            MAC_Reset( fecif );
  #if PHY_ON_CHIP         
            PHY_init();
  #endif                          
#if 0
            /*FSL:reset the PHY: quick fix*/
            while(!MII_write(FEC_PHY0, PHY_REG_CR, 0x8000))
            ;	//Force reset

            mymrdata = 0;
            do
            {
               // read if link is up
               MII_read(FEC_PHY0, PHY_REG_SR, &mymrdata);          	                 
            }while( !(mymrdata&PHY_R1_LS) );      	
#endif  
  #if SPEED_10BASET    
            while(!(MII_read(FEC_PHY0, PHY_REG_SR, &mymrdata)))	
          	;           // read PHY AN Ad register
          	if ((mymrdata & PHY_R1_LS)==1)
          	{
          		//gotlink =1;
          		goto exit;
          	}
          	else
          	{
          		while(!MII_write(FEC_PHY0, PHY_REG_CR, /*mymrdata|*/0x0200))
          		;					//Force re-negotiation
          	}
  exit:
            asm(nop);
  #endif

            FEC_SetRxCallback(MAC_ISR);
            MAC_Enable( fecif );

            etharp_init(  );
            sys_timeout( ARP_TMR_INTERVAL, arp_timer, NULL );

            res = ERR_OK;
        }

        if( res != ERR_OK )
        {
        	  /*FSL:change free(fecif) order; from top to bottom*/
            //free( fecif );
            if( fecif->tx_sem != NULL )
            {
                mem_free( fecif->tx_sem );
            }
            if( fecif->rx_sem != NULL )
            {
                mem_free( fecif->rx_sem );
            }
            mem_free( fecif );
        }
    }
    else
    {
        res = ERR_MEM;
    }

    return res;
}

