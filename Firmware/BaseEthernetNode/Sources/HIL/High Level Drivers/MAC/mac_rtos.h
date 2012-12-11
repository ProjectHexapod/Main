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

#include "interface.h"

/* ------------------------ Defines --------------------------------------- */

#define   Cpu_DisableInt() asm {move.w SR,D0; ori.l #0x0700,D0; move.w D0,SR;} /* Disable interrupts */
#define   Cpu_EnableInt()  asm {move.w SR,D0; andi.l #0xF8FF,D0; move.w D0,SR;} /* Enable interrupts */


#define ERR_OK          0    /* No error, everything OK. */
#define ERR_MEM        -1    /* Out of memory error.     */
#define ERR_BUF        -2    /* Buffer error.            */
#define ERR_RTE        -3    /* Routing problem.         */

#define ERR_IS_FATAL(e) ((e) < ERR_RTE)

#define ERR_ABRT       -4    /* Connection aborted.      */
#define ERR_RST        -5    /* Connection reset.        */
#define ERR_CLSD       -6    /* Connection closed.       */
#define ERR_CONN       -7    /* Not connected.           */

#define ERR_VAL        -8    /* Illegal value.           */

#define ERR_ARG        -9    /* Illegal argument.        */

#define ERR_USE        -10   /* Address in use.          */

#define ERR_IF         -11   /* Low-level netif error    */
#define ERR_ISCONN     -12   /* Already connected.       */

#define ERR_TIMEOUT    -13   /* Timeout.                 */

#define ERR_INPROGRESS -14   /* Operation in progress    */

/* ------------------------ Prototypes ------------------------------------ */

/**
 * FEC ISR
 *
 * @param none
 * @return none
 */
void 
MAC_ISR(void);


/**
 * Starts MAC controller
 *
 * @param MAC interface descriptor      
 * @return error code
 */
unsigned char
MAC_init( struct eth_addr *mac );

#endif
