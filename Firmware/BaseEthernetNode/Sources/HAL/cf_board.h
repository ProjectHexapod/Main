/*
 * File:		cf_board.h
 * Purpose:		Link between EVB and CW Project 
 *
 * Notes:
 */

#ifndef _CF_BOARD_H_
#define _CF_BOARD_H_

/********************************************************************/

/*FSL: select platform being used*/

#ifdef M51CN128EVB
#include "mcf51cn128/m51cn128evb.h"	      //Lasko: pass
#elif defined M5223xEVB
#include "mcf5223x/system/m5223xevb.h"		//k2e: ??
#elif defined M5225xEVB
#include "mcf5225x/system/m5225xevb.h"		//k3:  ??
#elif defined M523xEVB
#include "m523xevb.h"
#elif defined M5208EVB
#include "m5208evb.h"
#elif defined M5271EVB
#include "m5271evb.h"
#elif defined M5275EVB
#include "m5275evb.h"
#elif defined M5282EVB
#include "m528xevb.h"
#elif defined M5329EVB
#include "m5329evb.h"
/*FSL:to be determined*/
#elif defined M5272EVB
#include "m5272evb.h"
#elif defined M5475EVB
#include "m5475evb.h"
#elif defined M5485EVB
#include "m5485evb.h"
#else
#error "No CPU selected!!!"
#endif


/********************************************************************/

#endif /* _CF_BOARD_H_ */
