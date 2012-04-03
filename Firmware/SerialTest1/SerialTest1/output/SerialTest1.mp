Project:      output/SerialTest1
Build Number: 0
Date:         Tue Apr  3 01:53:26 2012
Compiler:     ICCM8C
Version:      7.04

  ROM 28% full. 1130 out of 4096 bytes used (does not include absolute areas).
  RAM 31% full. 78 bytes used (does not include stack usage).

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                           idata   0150   0003 =      3. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0150  __idata_start
       0153  __idata_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                     psoc_config   0153   0132 =    306. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0153  LoadConfigTBL_serialtest1
       027B  LoadConfigInit
       027B  _LoadConfigInit
       027F  _LoadConfig_serialtest1
       027F  LoadConfig_serialtest1
       0285  __psoc_config_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                     UserModules   0285   02F7 =    759. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0285  _UART_TX_ISR
       0286  _UART_RX_ISR
       02EC  _UART_EnableInt
       02EC  UART_EnableInt
       02F3  _UART_DisableInt
       02F3  UART_DisableInt
       02FA  _UART_SetTxIntMode
       02FA  UART_SetTxIntMode
       030C  UART_Start
       030C  _UART_Start
       0313  UART_Stop
       0313  _UART_Stop
       031A  UART_SendData
       031A  _UART_SendData
       031D  UART_bReadTxStatus
       031D  _bUART_ReadTxStatus
       031D  _UART_bReadTxStatus
       031D  bUART_ReadTxStatus
       0320  bUART_ReadRxData
       0320  _UART_bReadRxData
       0320  UART_bReadRxData
       0320  _bUART_ReadRxData
       0323  UART_bReadRxStatus
       0323  _UART_bReadRxStatus
       0323  bUART_ReadRxStatus
       0323  _bUART_ReadRxStatus
       0326  _UART_TxIntMode
       0326  UART_TxIntMode
       0339  UART_IntCntl
       0339  _UART_IntCntl
       0364  _UART_PutSHexByte
       0364  UART_PutSHexByte
       0377  _UART_PutSHexInt
       0377  UART_PutSHexInt
       037E  _UART_PutChar
       037E  UART_PutChar
       0386  UART_cGetChar
       0386  _UART_cGetChar
       038E  UART_cReadChar
       038E  _UART_cReadChar
       03A5  UART_iReadChar
       03A5  _UART_iReadChar
       03BB  UART_PutString
       03BB  _UART_PutString
       03C5  _UART_Write
       03C5  UART_Write
       03DD  _UART_CWrite
       03DD  UART_CWrite
       0405  _UART_CPutString
       0405  UART_CPutString
       0417  UART_PutCRLF
       0417  _UART_PutCRLF
       0420  _PWM8_EnableInt
       0420  PWM8_EnableInt
       0424  PWM8_DisableInt
       0424  _PWM8_DisableInt
       0428  PWM8_Start
       0428  _PWM8_Start
       042C  PWM8_Stop
       042C  _PWM8_Stop
       0430  PWM8_WritePeriod
       0430  _PWM8_WritePeriod
       0433  PWM8_WritePulseWidth
       0433  _PWM8_WritePulseWidth
       0436  _bPWM8_ReadPulseWidth
       0436  _PWM8_bReadPulseWidth
       0436  bPWM8_ReadPulseWidth
       0436  PWM8_bReadPulseWidth
       0439  PWM8_bReadCounter
       0439  _bPWM8_ReadCounter
       0439  bPWM8_ReadCounter
       0439  _PWM8_bReadCounter
       0462  _PGA_1_Start
       0462  _PGA_1_SetPower
       0462  PGA_1_Start
       0462  PGA_1_SetPower
       0470  _PGA_1_SetGain
       0470  PGA_1_SetGain
       0492  _PGA_1_Stop
       0492  PGA_1_Stop
       0496  _ADCINC_ADConversion_ISR
       0505  ADCINC_Start
       0505  _ADCINC_Start
       0517  _ADCINC_SetPower
       0517  ADCINC_SetPower
       0525  _ADCINC_Stop
       0525  ADCINC_Stop
       052F  _ADCINC_GetSamples
       052F  ADCINC_GetSamples
       054B  _ADCINC_StopADC
       054B  ADCINC_StopADC
       0555  _ADCINC_fIsDataAvailable
       0555  ADCINC_fIsDataAvailable
       0558  ADCINC_iClearFlagGetData
       0558  _ADCINC_iClearFlagGetData
       0558  _ADCINC_wClearFlagGetData
       0558  ADCINC_wClearFlagGetData
       0565  ADCINC_bClearFlagGetData
       0565  ADCINC_cClearFlagGetData
       0565  _ADCINC_bClearFlagGetData
       0565  _ADCINC_cClearFlagGetData
       056B  _ADCINC_wGetData
       056B  ADCINC_wGetData
       056B  ADCINC_iGetData
       056B  _ADCINC_iGetData
       0570  ADCINC_cGetData
       0570  _ADCINC_bGetData
       0570  ADCINC_bGetData
       0570  _ADCINC_cGetData
       0573  ADCINC_fClearFlag
       0573  _ADCINC_fClearFlag
       0579  ADCINC_WritePulseWidth
       0579  _ADCINC_WritePulseWidth
       057C  __UserModules_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                            text   057C   003E =     62. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       057C  _main
       057C  __text_start
       05BA  __text_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                            data   0000   0003 =      3. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0000  _bytes_received
       0000  __data_start
       0001  _ext_mem_locked
       0002  _m_to_s_offset
       0003  __data_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
               virtual_registers   0003   0001 =      1. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0003  __r0
       0004  __virtual_registers_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                    InterruptRAM   0004   0008 =      8. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0004  NO_SHADOW
       0004  ADCINC_iResult
       0004  _NO_SHADOW
       0004  _ADCINC_iResult
       0008  ADCINC_fStatus
       0008  _ADCINC_fStatus
       0009  ADCINC_bState
       0009  _ADCINC_bState
       000A  _ADCINC_fMode
       000A  ADCINC_fMode
       000B  ADCINC_bNumSamples
       000B  _ADCINC_bNumSamples
       000C  __InterruptRAM_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                             bss   000C   0042 =     66. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       000C  _s_to_m_mem
       000C  __bss_start
       002C  _m_to_s_mem
       004C  _expected_bytes
       004D  _target_address
       004E  __bss_end
       004E  __ramareas_end

Area                               Start  End    Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                             TOP   0068   00D4 =    212. bytes (abs,ovr,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0068  __Start
       00D1  bGetPowerSetting
       00D1  _bGetPowerSetting

Files Linked      [ module(s) ]

./obj/boot.o	[ boot.asm ]
./obj/main.o	[ main.c ]
<library>	[ uartint.asm, uart.asm, pwm8.asm, psocconfigtbl.asm, psocconfig.asm, pga_1.asm, adcincint.asm ]
[ adcinc.asm, r0.asm ]

Area Definitions

-blit:0x150.0xfff
-bdata:0.0xff

