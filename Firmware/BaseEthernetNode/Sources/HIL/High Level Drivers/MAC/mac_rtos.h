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
 * File: $Id: fec.h,v 1.1 2008/09/17 13:51:53 b06862 Exp $
 */

#ifndef _MAC_RTOS_H_
#define _MAC_RTOS_H_

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

/* ------------------------ Defines --------------------------------------- */

/* ------------------------ Prototypes ------------------------------------ */
/**
 * Output information thru Ethernet
 *
 * @param MAC interface descriptor
 * @param network buffer to send
 * @return error code
 */
err_t
MAC_output_raw( struct netif *netif, struct pbuf *p );

/**
 * Ethernet rx task being called periodically by FreeRTOS
 *
 * @param MAC interface descriptor
 * @return none
 */
void
MAC_Rx_Task(void *arg );

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
MAC_Send( struct netif * netif, struct pbuf * p, struct ip_addr * ipaddr );

/**
 * FEC ISR
 *
 * @param none
 * @return none
 */
void 
MAC_ISR(void);

/**
 * Handles all ARP timeouts
 *
 * @param none
 * @return none
 */
static void
arp_timer( void *arg );
/**
 * Handles all ethernet input from lwIP stacks
 *
 * @param MAC controller descriptor
 * @param buffer to send to upper layers
 * @return none
 */
void
eth_input( struct netif *netif, struct pbuf *p );


/**
 * returns MAC address
 *
 * @param MAC address holder
 * @return none
 */
void
MAC_GetMacAddress(struct eth_addr *mac );


/**
 * Starts MAC controller
 *
 * @param MAC interface descriptor      
 * @return error code
 */
err_t
MAC_init( struct netif *netif );

#endif
