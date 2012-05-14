;;*****************************************************************************
;;*****************************************************************************
;;  FILENAME: DAC6.inc
;;   Version: 4.3, Updated on 2011/6/28 at 6:9:3
;;  Generated by PSoC Designer 5.1.2306
;;
;;  DESCRIPTION: Assembler declarations for the DAC6 user module interface.
;;
;;-----------------------------------------------------------------------------
;;  Copyright (c) Cypress Semiconductor 2011. All Rights Reserved.
;;*****************************************************************************
;;*****************************************************************************

;--------------------------------------------------
; Constants for DAC6 API's
;--------------------------------------------------
DAC6_OFF:              equ 00h
DAC6_LOWPOWER:         equ 01h
DAC6_MEDPOWER:         equ 02h
DAC6_HIGHPOWER:        equ 03h

DAC6_OffsetBinary:     equ 04h
DAC6_TwosComplement:   equ 02h
DAC6_SignAndMagnitude: equ 01h
DAC6_RawRegister:      equ 00h

DAC6_DATAFORMAT:       equ 7h
DAC6_OFFSETBINARY:     equ DAC6_DATAFORMAT & DAC6_OffsetBinary
DAC6_TWOSCOMPLEMENT:   equ DAC6_DATAFORMAT & DAC6_TwosComplement
DAC6_SIGNANDMAGNITUDE: equ DAC6_DATAFORMAT & DAC6_SignAndMagnitude

DAC6_PHASE_Normal:     equ 0
DAC6_PHASE_Swapped:    equ 1
DAC6_PHASE_SWAP:       equ DAC6_PHASE_Normal

IF DAC6_PHASE_SWAP
    DAC6_CR0_HIBITS:   equ C0h
ELSE
    DAC6_CR0_HIBITS:   equ 80h
ENDIF


;--------------------------------------------------
; Register Address Constants for DAC6
;--------------------------------------------------
DAC6_CR0:              equ 84h
DAC6_CR1:              equ 85h
DAC6_CR2:              equ 86h
DAC6_CR3:              equ 87h