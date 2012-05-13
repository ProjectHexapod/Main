;;*****************************************************************************
;;*****************************************************************************
;;  FILENAME: ADCINCINT.asm
;;  Version: 1.20, Updated on 2011/6/28 at 6:7:58
;;
;;  DESCRIPTION: Assembler interrupt service routine for the ADCINC
;;               A/D Converter User Module. This code works for both the
;;               first and second-order modulator topologies.
;;-----------------------------------------------------------------------------
;;  Copyright (c) Cypress Semiconductor 2011. All Rights Reserved.
;;*****************************************************************************
;;*****************************************************************************

include "m8c.inc"
include "memory.inc"
include "ADCINC.inc"


;-----------------------------------------------
;  Global Symbols
;-----------------------------------------------

export _ADCINC_ADConversion_ISR

export _ADCINC_iResult
export  ADCINC_iResult
export _ADCINC_fStatus
export  ADCINC_fStatus
export _ADCINC_bState
export  ADCINC_bState
export _ADCINC_fMode
export  ADCINC_fMode
export _ADCINC_bNumSamples
export  ADCINC_bNumSamples

;-----------------------------------------------
; Variable Allocation
;-----------------------------------------------
AREA InterruptRAM(RAM,REL)
 ADCINC_iResult:
_ADCINC_iResult:                           BLK  2 ;Calculated answer
  iTemp:                                   BLK  2 ;internal temp storage
 ADCINC_fStatus:
_ADCINC_fStatus:                           BLK  1 ;ADC Status
 ADCINC_bState:
_ADCINC_bState:                            BLK  1 ;State value of ADC count
 ADCINC_fMode:
_ADCINC_fMode:                             BLK  1 ;Integrate and reset mode.
 ADCINC_bNumSamples:
_ADCINC_bNumSamples:                       BLK  1 ;Number of samples to take.

;-----------------------------------------------
;  EQUATES
;-----------------------------------------------

;@PSoC_UserCode_INIT@ (Do not change this line.)
;---------------------------------------------------
; Insert your custom declarations below this banner
;---------------------------------------------------

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
;  FUNCTION NAME: _ADCINC_ADConversion_ISR
;
;  DESCRIPTION: Perform final filter operations to produce output samples.
;
;-----------------------------------------------------------------------------
;
;    The decimation rate is established by the PWM interrupt. Four timer
;    clocks elapse for each modulator output (decimator input) since the
;    phi1/phi2 generator divides by 4. This means the timer period and thus
;    it's interrupt must equal 4 times the actual decimation rate.  The
;    decimator is ru  for 2^(#bits-6).
;
_ADCINC_ADConversion_ISR:
    dec  [ADCINC_bState]
if1:
    jc endif1 ; no underflow
    reti
endif1:
    cmp [ADCINC_fMode],0
if2: 
    jnz endif2  ;leaving reset mode
    push A                            ;read decimator
    mov  A, reg[DEC_DL]
    mov  [iTemp + LowByte],A
    mov  A, reg[DEC_DH]
    mov  [iTemp + HighByte], A
    pop A
    mov [ADCINC_fMode],1
    mov [ADCINC_bState],((1<<(ADCINC_bNUMBITS- 6))-1)
    reti
endif2:
    ;This code runs at end of integrate
    ADCINC_RESET_INTEGRATOR_M
    push A
    mov  A, reg[DEC_DL]
    sub  A,[iTemp + LowByte]
    mov  [iTemp +LowByte],A
    mov  A, reg[DEC_DH]
    sbb  A,[iTemp + HighByte]
    asr  A
    rrc  [iTemp + LowByte]

       ;Covert to Unipolar
IF  ADCINC_9_OR_MORE_BITS
    add  A, (1<<(ADCINC_bNUMBITS - 9))
ELSE
    add [iTemp + LowByte], (1<<(ADCINC_bNUMBITS - 1)) ;work on lower Byte
    adc A,0 
ENDIF
       ;check for overflow
IF     ADCINC_8_OR_MORE_BITS
    cmp A,(1<<(ADCINC_bNUMBITS - 8))
if3: 
    jnz endif3 ;overflow
    dec A
    mov [iTemp + LowByte],ffh
endif3:
ELSE
    cmp [iTemp + LowByte],(1<<(ADCINC_bNUMBITS))
if4: 
    jnz endif4 ;overflow
    dec [iTemp + LowByte]
endif4:
ENDIF
IF ADCINC_SIGNED_DATA
IF ADCINC_9_OR_MORE_BITS
    sub A,(1<<(ADCINC_bNUMBITS - 9))
ELSE
    sub [iTemp +LowByte],(1<<(ADCINC_bNUMBITS - 1))
    sbb A,0
ENDIF
ENDIF
    mov  [ADCINC_iResult + LowByte],[iTemp +LowByte]
    mov  [ADCINC_iResult + HighByte],A
    mov  [ADCINC_fStatus],1
ConversionReady:
    ;@PSoC_UserCode_BODY@ (Do not change this line.)
    ;---------------------------------------------------
    ; Insert your custom code below this banner
    ;---------------------------------------------------
    ;  Sample data is now in iResult
    ;
    ;  NOTE: This interrupt service routine has already
    ;  preserved the values of the A CPU register. If
    ;  you need to use the X register you must preserve
    ;  its value and restore it before the return from
    ;  interrupt.
	
	mov [0+_s_to_m_mem], [ADCINC_iResult+LowByte]
	mov [1+_s_to_m_mem], A
	
    ;---------------------------------------------------
    ; Insert your custom code above this banner
    ;---------------------------------------------------
    ;@PSoC_UserCode_END@ (Do not change this line.)
    pop A
    cmp [ADCINC_bNumSamples],0
if5: 
    jnz endif5 ; Number of samples is zero
    mov [ADCINC_fMode],0
    mov [ADCINC_bState],0
    ADCINC_ENABLE_INTEGRATOR_M
    reti       
endif5:
    dec [ADCINC_bNumSamples]
if6:
    jz endif6  ; count not zero
    mov [ADCINC_fMode],0
    mov [ADCINC_bState],0
    ADCINC_ENABLE_INTEGRATOR_M
    reti       
endif6:
    ;All samples done
    ADCINC_STOPADC_M
 reti 
; end of file ADCINCINT.asm
