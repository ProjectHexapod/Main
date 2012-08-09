
/*********************************************************************
 *
 * Copyright:
 *	2005 FREESCALE, INC. All Rights Reserved.  
 *  You are hereby granted a copyright license to use, modify, and
 *  distribute the SOFTWARE so long as this entire notice is
 *  retained without alteration in any modified and/or redistributed
 *  versions, and that such modified versions are clearly identified
 *  as such. No licenses are granted by implication, estoppel or
 *  otherwise under any patents or trademarks of Motorola, Inc. This 
 *  software is provided on an "AS IS" basis and without warranty.
 *
 *  To the maximum extent permitted by applicable law, FREESCALE 
 *  DISCLAIMS ALL WARRANTIES WHETHER EXPRESS OR IMPLIED, INCLUDING 
 *  IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR
 *  PURPOSE AND ANY WARRANTY AGAINST INFRINGEMENT WITH REGARD TO THE 
 *  SOFTWARE (INCLUDING ANY MODIFIED VERSIONS THEREOF) AND ANY 
 *  ACCOMPANYING WRITTEN MATERIALS.
 * 
 *  To the maximum extent permitted by applicable law, IN NO EVENT
 *  SHALL FREESCALE BE LIABLE FOR ANY DAMAGES WHATSOEVER (INCLUDING 
 *  WITHOUT LIMITATION, DAMAGES FOR LOSS OF BUSINESS PROFITS, BUSINESS 
 *  INTERRUPTION, LOSS OF BUSINESS INFORMATION, OR OTHER PECUNIARY
 *  LOSS) ARISING OF THE USE OR INABILITY TO USE THE SOFTWARE.   
 * 
 *  Freescale assumes no responsibility for the maintenance and support
 *  of this software
 ********************************************************************/

/*
 * File:		io.c
 * Purpose:	Serial Input/Output routines
 *
 */

#include "cf_board.h"

#include "FreeRTOS.h"
#include "queue.h"
#include "task.h"

#include "uart_rtos.h"

//FSL: global variable
static xComPortHandle printf_handle = NULL;

/********************************************************************/
CHAR
in_char (void)
{
   SCHAR c;
   
   //FSL:block it to make it compliant with old in_char!!
   /*if(!(*/xUARTGetChar(printf_handle,&c, portMAX_DELAY);/*))*/
   //{
   //   //error
   //   c = NULL;
   //}
   
   return c;   
}
/********************************************************************/
void
out_char (CHAR ch)
{
   UCHAR c = (UCHAR)ch;
   
   //block process!!
   if (c == '\n')
      xUARTPutChar(printf_handle, '\r', portMAX_DELAY) ;
   xUARTPutChar(printf_handle, ch, portMAX_DELAY) ;   
}

/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/

/*FSL: glue logic to use printf with FreeRTOS*/

void 
set_printf_handle(xComPortHandle UARThandle)
{
   printf_handle = UARThandle;
}

xComPortHandle 
get_printf_handle(void)
{
   return printf_handle;
}

