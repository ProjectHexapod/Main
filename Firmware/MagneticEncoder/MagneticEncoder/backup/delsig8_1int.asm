;;*****************************************************************************
;;*****************************************************************************
;;  FILENAME: DELSIG8_1INT.asm
;;   Version: 3.2, Updated on 2011/6/28 at 6:9:4
;;
;;  DESCRIPTION: Assembler interrupt service routine for the 8-bit Delta-Sigma
;;               A/D Converter User Module. This code works for both the
;;               first and second-order modulator topologies.
;;-----------------------------------------------------------------------------
;;  Copyright (c) Cypress Semiconductor 2011. All Rights Reserved.
;;*****************************************************************************
;;*****************************************************************************

include "m8c.inc"
include "memory.inc"
include "DELSIG8_1.inc"


;-----------------------------------------------
;  Global Symbols
;-----------------------------------------------

export _DELSIG8_1_ADConversion_ISR

IF (DELSIG8_1_POLL_ENABLE)
export _DELSIG8_1_cResult
export  DELSIG8_1_cResult
export _DELSIG8_1_bfStatus
export  DELSIG8_1_bfStatus
ENDIF


;-----------------------------------------------
; Variable Allocation
;-----------------------------------------------
AREA InterruptRAM (RAM, REL, CON)

iOut:                                      BLK  2  ; Converted output value
iTmp2:                                     BLK  2  ; z^-2
iTmp1:                                     BLK  2  ; z^-1

IF (DELSIG8_1_POLL_ENABLE)
_DELSIG8_1_cResult:
 DELSIG8_1_cResult:                        BLK  1  ; A/D value
_DELSIG8_1_bfStatus:
 DELSIG8_1_bfStatus:                       BLK  1  ; Data Valid Flag
ENDIF


;-----------------------------------------------
;  Private Symbols
;-----------------------------------------------
MSB:                   equ  0
LSB:                   equ  1


;@PSoC_UserCode_INIT@ (Do not change this line.)
;---------------------------------------------------
; Insert your custom declarations below this banner
;---------------------------------------------------

;------------------------
; Includes
;------------------------

	
;------------------------
;  Constant Definitions
;------------------------


;------------------------
; Variable Allocation
;------------------------


;---------------------------------------------------
; Insert your custom declarations above this banner
;---------------------------------------------------
;@PSoC_UserCode_END@ (Do not change this line.)


AREA UserModules (ROM, REL)

;-----------------------------------------------------------------------------
;  FUNCTION NAME: _DELSIG8_1_ADConversion_ISR
;
;  DESCRIPTION: Perform final filter operations to produce output samples.
;
;-----------------------------------------------------------------------------
;
;  THEORY of OPERATION or PROCEDURE: In the Z-domain, the DelSig transfer
;     function is given by
;
;        H(Z) = [ (1 - Z^(-n)) / (1 - Z^(-1)) ]^2
;
;    The denominator is implemened by the hardware decimation unit operating
;    at the modulator (single-bit) sample rate. The following code, operating
;    at the decimation rate (n=64), completes the calculation:
;
;        (1 - Z^-n)^2  =  1 - 2z^-1 + Z^-2n  =  (1 - Z^-n) - (Z^-n - Z^-2n)
;    or
;        (Z^-2n - Z^-n) - (Z^-n - 1)  (inverting twice).
;
;    In time domain notation, for samples x[0],...,x[n],...,x[2n],...
;    (where x[0] is the most recent) this is becomes simply
;
;        (x[2n]-x[n])-(x[n]-x[0]) or, for ease of notation, (x2-x1)-(x1-x0)
;
;    The decimation rate is established by the timer interrupt. Four timer
;    clocks elapse for each modulator output (decimator input) since the
;    phi1/phi2 generator divides by 4. This means the timer period and thus
;    its interrupt must equal 4 times the actual decimation rate, in this
;    case, 4*64 = 256.
;
_DELSIG8_1_ADConversion_ISR:
   push A                  ;  Variables:     Out              Tmp2     Tmp1   Deci
                           ;  Initial state: (x3-x2)-(x2-x1)  (x2-x1)  x1     x0

                                           ; --> Tmp2 moved to Out:
   mov  [iOut + LSB],  [iTmp2 + LSB]       ; Out              Tmp2     Tmp1   Deci
   mov  [iOut + MSB],  [iTmp2 + MSB]       ; (x2-x1)          (x2-x1)  x1     x0
										   
                                           ; --> Tmp1 moved to Tmp2:
   mov  [iTmp2 + LSB], [iTmp1 + LSB]       ; Out              Tmp2     Tmp1   Deci
   mov  [iTmp2 + MSB], [iTmp1 + MSB]       ; (x2-x1)          x1       x1     x0  
										   
   mov  A, reg[DEC_DL]                     ; --> Deci to Tmp1 & ...               
   mov  [iTmp1 + LSB],  A                  ;                                      
   sub  [iTmp2 + LSB],  A                  ;   deci subtracted from Tmp2:         
   mov  A, reg[DEC_DH]                     ;                                      
   mov  [iTmp1 + MSB], A                   ; Out              Tmp2     Tmp1   Deci
   sbb  [iTmp2 + MSB], A                   ; (x2-x1)          x1-x0    x0     x0  
										   
   mov  A, [iTmp2 + LSB]                   ; --> Subtract Tmp2 from Out:          
   sub  [iOut + LSB],   A                  ;                                      
   mov  A, [iTmp2 + MSB]                   ; Out              Tmp2     Tmp1   Deci
   sbb  [iOut + MSB],  A                   ; (x2-x1)-(x1-x0)  x1-x0    x0     x0  
										   
   cmp  [iOut + MSB], 10h                  ; Is the value less than full scale?
   jnz  LessThanFullScale                  ;   Yes, go normalize it.
   mov  A, 7fh                             ;    No, limit value to plus full-scale
   jmp  ConversionReady                    ;         range (already normalized).
LessThanFullScale:						   
    mov  A, [iOut + MSB]                   ; Normalize data (multiply by 8 and...
    rlc  [iOut + LSB]                      ;   use only what lies in the upper
    rlc  A                                 ;   byte)
    rlc  [iOut + LSB]
    rlc  A
    rlc  [iOut + LSB]
    rlc  A
ConversionReady:

   ;@PSoC_UserCode_BODY@ (Do not change this line.)
   ;---------------------------------------------------
   ; Insert your custom code below this banner
   ;---------------------------------------------------
   ;  Sample data is now in the A register.
   ;  NOTE: This interrupt service routine has already
   ;  preserved the values of the A CPU register. If
   ;  you need to use the X register you must preserve
   ;  its value and restore it before the return from
   ;  interrupt.


IF (DELSIG8_1_POLL_ENABLE)
   mov  [DELSIG8_1_cResult],  A                                      ; Save result in cResult
   mov  [DELSIG8_1_bfStatus], DELSIG8_1_DATA_READY_BIT               ; Set valid data flag
ENDIF

   ;---------------------------------------------------
   ; Insert your custom code above this banner
   ;---------------------------------------------------
   ;@PSoC_UserCode_END@ (Do not change this line.)

   pop A
   reti

; end of file DELSIG8_1INT.asm
