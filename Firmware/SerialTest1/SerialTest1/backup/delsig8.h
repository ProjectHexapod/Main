//*****************************************************************************
//*****************************************************************************
//  FILENAME: DELSIG8.h
//   Version: 3.2, Updated on 2011/6/28 at 6:9:4
//
//  DESCRIPTION:  C declarations for the DELSIG8 User Module with
//                a 1st-order modulator.
//-----------------------------------------------------------------------------
//      Copyright (c) Cypress Semiconductor 2011. All Rights Reserved.
//*****************************************************************************
//*****************************************************************************
#ifndef DELSIG8_INCLUDE
#define DELSIG8_INCLUDE

#include <m8c.h>

#define DELSIG8_POLL_ENABLE 0

#pragma fastcall16 DELSIG8_Start
#pragma fastcall16 DELSIG8_SetPower
#pragma fastcall16 DELSIG8_StartAD
#pragma fastcall16 DELSIG8_StopAD
#pragma fastcall16 DELSIG8_Stop

#if ( DELSIG8_POLL_ENABLE )
#pragma fastcall16 DELSIG8_fIsDataAvailable
#pragma fastcall16 DELSIG8_cGetData
#pragma fastcall16 DELSIG8_cGetDataClearFlag
#pragma fastcall16 DELSIG8_ClearFlag
#endif

//-------------------------------------------------
// Prototypes of the DELSIG8 API.
//-------------------------------------------------
extern void DELSIG8_Start(BYTE bPower);       // RAM use class 2
extern void DELSIG8_SetPower(BYTE bPower);    // RAM use class 2
extern void DELSIG8_StartAD(void);            // RAM use class 1
extern void DELSIG8_StopAD(void);             // RAM use class 1
extern void DELSIG8_Stop(void);               // RAM use class 1

#if ( DELSIG8_POLL_ENABLE )
extern BYTE DELSIG8_fIsDataAvailable(void);   // RAM use class 4
extern CHAR DELSIG8_cGetData(void);           // RAM use class 4
extern CHAR DELSIG8_cGetDataClearFlag(void);  // RAM use class 4
extern void DELSIG8_ClearFlag(void);          // RAM use class 4
#endif

//-------------------------------------------------
// Defines for DELSIG8 API's.
//-------------------------------------------------
#define DELSIG8_OFF         0
#define DELSIG8_LOWPOWER    1
#define DELSIG8_MEDPOWER    2
#define DELSIG8_HIGHPOWER   3

#define DELSIG8_DATA_READY_BIT  0x10
//-------------------------------------------------
// Hardware Register Definitions
//-------------------------------------------------
#pragma ioport  DELSIG8_TimerDR0:   0x020              //Time base Counter register
BYTE            DELSIG8_TimerDR0;
#pragma ioport  DELSIG8_TimerDR1:   0x021              //Time base Period value register
BYTE            DELSIG8_TimerDR1;
#pragma ioport  DELSIG8_TimerDR2:   0x022              //Time base CompareValue register
BYTE            DELSIG8_TimerDR2;
#pragma ioport  DELSIG8_TimerCR0:   0x023              //Time base Control register
BYTE            DELSIG8_TimerCR0;
#pragma ioport  DELSIG8_TimerFN:    0x120               //Time base Function register
BYTE            DELSIG8_TimerFN;
#pragma ioport  DELSIG8_TimerSL:    0x121               //Time base Input register
BYTE            DELSIG8_TimerSL;
#pragma ioport  DELSIG8_TimerOS:    0x122               //Time base Output register
BYTE            DELSIG8_TimerOS;

#pragma ioport  DELSIG8_AtoDcr0:    0x080               //Analog control register 0
BYTE            DELSIG8_AtoDcr0;
#pragma ioport  DELSIG8_AtoDcr1:    0x081               //Analog control register 1
BYTE            DELSIG8_AtoDcr1;
#pragma ioport  DELSIG8_AtoDcr2:    0x082               //Analog control register 2
BYTE            DELSIG8_AtoDcr2;
#pragma ioport  DELSIG8_AtoDcr3:    0x083               //Analog control register 3
BYTE            DELSIG8_AtoDcr3;

#endif
// end of file DELSIG8.h
