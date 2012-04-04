;;*****************************************************************************
;;*****************************************************************************
;;  FILENAME: DELSIG8.inc
;;   Version: 3.2, Updated on 2011/6/28 at 6:9:4
;;
;;  DESCRIPTION: Assembler declarations for the 8-bit Delta-Sigma A/D Converter
;;               User Module with a 1st-order modulator.
;;-----------------------------------------------------------------------------
;;  Copyright (c) Cypress Semiconductor 2011. All Rights Reserved.
;;*****************************************************************************
;;*****************************************************************************

include "m8c.inc"


;--------------------------------------------------
; Constants for DELSIG8 API's.
;--------------------------------------------------

DELSIG8_INT_REG:                           equ  0e1h
DELSIG8_INT_MASK:                          equ  01h     ; Interrupt mask

DELSIG8_OFF:                   equ 00h
DELSIG8_LOWPOWER:              equ 01h
DELSIG8_MEDPOWER:              equ 02h
DELSIG8_HIGHPOWER:             equ 03h

DELSIG8_POLL_ENABLE:           equ 0
DELSIG8_DATA_READY_BIT:        equ 10h


;--------------------------------------------------
; Register Address Constants for DELSIG8
;--------------------------------------------------

DELSIG8_TimerDR0:              equ 0x20    ; Period reg
DELSIG8_TimerDR1:              equ 0x21    ; Down count reg
DELSIG8_TimerDR2:              equ 0x22    ; Compare reg
DELSIG8_TimerCR0:              equ 0x23    ; Control reg
DELSIG8_TimerFN:               equ 0x20    ; Function reg
DELSIG8_TimerSL:               equ 0x21    ; Input  select reg
DELSIG8_TimerOS:               equ 0x22    ; Output select reg

DELSIG8_AtoDcr0:               equ 0x80    ; SC Block Control Reg 0
DELSIG8_AtoDcr1:               equ 0x81    ; SC Block Control Reg 1
DELSIG8_AtoDcr2:               equ 0x82    ; SC Block Control Reg 2
DELSIG8_AtoDcr3:               equ 0x83    ; SC Block Control Reg 3


; end of file DELSIG8.inc
