/*
 * Copyright (c) 2001-2003 Swedish Institute of Computer Science.
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
 * This file is part of the lwIP TCP/IP stack.
 *
 * Author: Adam Dunkels <adam@sics.se>
 *
 */
#ifndef __SYS_ARCH_H__
#define __SYS_ARCH_H__

/* ------------------------ Project includes ------------------------------ */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"

/* ------------------------ Defines --------------------------------------- */
#define SYS_MBOX_NULL           ( xQueueHandle )0
#define SYS_THREAD_NULL         NULL
#define SYS_SEM_NULL            ( xSemaphoreHandle )0
#define SIO_FD_NULL             ( sio_fd_t )NULL

/* ------------------------ STACK options --------------------------------- */
/*FSL: stack spaces for threads being running*/
#define TCPIP_THREAD_STACKSIZE		216//216//216//256
#define FEC_RX_STACK_SPACE			  80//112//112//112//112

/* ------------------------ Type definitions ------------------------------ */
typedef xSemaphoreHandle sys_sem_t;
typedef xQueueHandle sys_mbox_t;
typedef void   *sys_thread_t;

/* ------------------------ Prototypes ------------------------------------ */
//FSL:not longer necessary
//sys_thread_t    sys_arch_thread_new( void ( *thread ) ( void *arg ), void *arg,
//                                     int prio, unsigned /*size_t*/ ssize );

/*FSL:workaround from lwIP port (1.1.1 to 1.3.1)*/
#define sys_arch_mbox_tryfetch(mbox,msg) \
    sys_arch_mbox_fetch(mbox,msg,1)

sys_thread_t    sys_arch_thread_current( void );
void            sys_arch_thread_remove( sys_thread_t hdl );
void            sys_assert( const char *const msg );
void            sys_debug( const char *const fmt, ... );

#endif
