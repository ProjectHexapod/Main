Project:      output/SerialTest1
Build Number: 0
Date:         Wed Apr  4 00:02:14 2012
Compiler:     ICCM8C
Version:      7.04

  ROM 28% full. 1120 out of 4096 bytes used (does not include absolute areas).
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
                     UserModules   0285   02ED =    749. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0285  _UART_TX_ISR
       0286  _UART_RX_ISR
       02E3  _UART_EnableInt
       02E3  UART_EnableInt
       02EA  _UART_DisableInt
       02EA  UART_DisableInt
       02F1  _UART_SetTxIntMode
       02F1  UART_SetTxIntMode
       0303  UART_Start
       0303  _UART_Start
       030A  UART_Stop
       030A  _UART_Stop
       0311  UART_SendData
       0311  _UART_SendData
       0314  UART_bReadTxStatus
       0314  _bUART_ReadTxStatus
       0314  _UART_bReadTxStatus
       0314  bUART_ReadTxStatus
       0317  bUART_ReadRxData
       0317  _UART_bReadRxData
       0317  UART_bReadRxData
       0317  _bUART_ReadRxData
       031A  UART_bReadRxStatus
       031A  _UART_bReadRxStatus
       031A  bUART_ReadRxStatus
       031A  _bUART_ReadRxStatus
       031D  _UART_TxIntMode
       031D  UART_TxIntMode
       0330  UART_IntCntl
       0330  _UART_IntCntl
       035B  _UART_PutSHexByte
       035B  UART_PutSHexByte
       036E  _UART_PutSHexInt
       036E  UART_PutSHexInt
       0375  _UART_PutChar
       0375  UART_PutChar
       037D  UART_cGetChar
       037D  _UART_cGetChar
       0385  UART_cReadChar
       0385  _UART_cReadChar
       039C  UART_iReadChar
       039C  _UART_iReadChar
       03B2  UART_PutString
       03B2  _UART_PutString
       03BC  _UART_Write
       03BC  UART_Write
       03D4  _UART_CWrite
       03D4  UART_CWrite
       03FC  _UART_CPutString
       03FC  UART_CPutString
       040E  UART_PutCRLF
       040E  _UART_PutCRLF
       0417  _PWM8_EnableInt
       0417  PWM8_EnableInt
       041B  PWM8_DisableInt
       041B  _PWM8_DisableInt
       041F  PWM8_Start
       041F  _PWM8_Start
       0423  PWM8_Stop
       0423  _PWM8_Stop
       0427  PWM8_WritePeriod
       0427  _PWM8_WritePeriod
       042A  PWM8_WritePulseWidth
       042A  _PWM8_WritePulseWidth
       042D  _bPWM8_ReadPulseWidth
       042D  _PWM8_bReadPulseWidth
       042D  bPWM8_ReadPulseWidth
       042D  PWM8_bReadPulseWidth
       0430  PWM8_bReadCounter
       0430  _bPWM8_ReadCounter
       0430  bPWM8_ReadCounter
       0430  _PWM8_bReadCounter
       0459  _PGA_1_Start
       0459  _PGA_1_SetPower
       0459  PGA_1_Start
       0459  PGA_1_SetPower
       0467  _PGA_1_SetGain
       0467  PGA_1_SetGain
       0489  _PGA_1_Stop
       0489  PGA_1_Stop
       048D  _ADCINC_ADConversion_ISR
       04FB  ADCINC_Start
       04FB  _ADCINC_Start
       050D  _ADCINC_SetPower
       050D  ADCINC_SetPower
       051B  _ADCINC_Stop
       051B  ADCINC_Stop
       0525  _ADCINC_GetSamples
       0525  ADCINC_GetSamples
       0541  _ADCINC_StopADC
       0541  ADCINC_StopADC
       054B  _ADCINC_fIsDataAvailable
       054B  ADCINC_fIsDataAvailable
       054E  ADCINC_iClearFlagGetData
       054E  _ADCINC_iClearFlagGetData
       054E  _ADCINC_wClearFlagGetData
       054E  ADCINC_wClearFlagGetData
       055B  ADCINC_bClearFlagGetData
       055B  ADCINC_cClearFlagGetData
       055B  _ADCINC_bClearFlagGetData
       055B  _ADCINC_cClearFlagGetData
       0561  _ADCINC_wGetData
       0561  ADCINC_wGetData
       0561  ADCINC_iGetData
       0561  _ADCINC_iGetData
       0566  ADCINC_cGetData
       0566  _ADCINC_bGetData
       0566  ADCINC_bGetData
       0566  _ADCINC_cGetData
       0569  ADCINC_fClearFlag
       0569  _ADCINC_fClearFlag
       056F  ADCINC_WritePulseWidth
       056F  _ADCINC_WritePulseWidth
       0572  __UserModules_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                            text   0572   003E =     62. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0572  _main
       0572  __text_start
       05B0  __text_end

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

