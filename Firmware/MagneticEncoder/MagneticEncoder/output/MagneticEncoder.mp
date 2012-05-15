Project:      output/MagneticEncoder
Build Number: 0
Date:         Tue May 15 00:24:10 2012
Compiler:     ICCM8C
Version:      7.04

  ROM 36% full. 1438 out of 4096 bytes used (does not include absolute areas).
  RAM 34% full. 86 bytes used (does not include stack usage).

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                           idata   0150   0009 =      9. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0150  __idata_start
       0159  __idata_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                     psoc_config   0159   012C =    300. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0159  LoadConfigTBL_MagneticEncoder
       027B  LoadConfigInit
       027B  _LoadConfigInit
       027F  _LoadConfig_MagneticEncoder
       027F  LoadConfig_MagneticEncoder
       0285  __psoc_config_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                     UserModules   0285   02D7 =    727. bytes (rel,con,rom)

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
       0303  _UART_Start
       0303  UART_Start
       030A  _UART_Stop
       030A  UART_Stop
       0311  UART_SendData
       0311  _UART_SendData
       0314  _bUART_ReadTxStatus
       0314  _UART_bReadTxStatus
       0314  UART_bReadTxStatus
       0314  bUART_ReadTxStatus
       0317  bUART_ReadRxData
       0317  UART_bReadRxData
       0317  _UART_bReadRxData
       0317  _bUART_ReadRxData
       031A  _bUART_ReadRxStatus
       031A  _UART_bReadRxStatus
       031A  bUART_ReadRxStatus
       031A  UART_bReadRxStatus
       031D  UART_TxIntMode
       031D  _UART_TxIntMode
       0330  UART_IntCntl
       0330  _UART_IntCntl
       035B  _UART_PutSHexByte
       035B  UART_PutSHexByte
       036E  _UART_PutSHexInt
       036E  UART_PutSHexInt
       0375  UART_PutChar
       0375  _UART_PutChar
       037D  _UART_cGetChar
       037D  UART_cGetChar
       0385  UART_cReadChar
       0385  _UART_cReadChar
       039C  _UART_iReadChar
       039C  UART_iReadChar
       03B2  _UART_PutString
       03B2  UART_PutString
       03BC  UART_Write
       03BC  _UART_Write
       03D4  _UART_CWrite
       03D4  UART_CWrite
       03FC  UART_CPutString
       03FC  _UART_CPutString
       040E  _UART_PutCRLF
       040E  UART_PutCRLF
       0417  PGA_1_SetPower
       0417  _PGA_1_Start
       0417  PGA_1_Start
       0417  _PGA_1_SetPower
       0425  _PGA_1_SetGain
       0425  PGA_1_SetGain
       0447  PGA_1_Stop
       0447  _PGA_1_Stop
       044B  _ADCINC_1_ADConversion_ISR
       04C6  ADCINC_1_Start
       04C6  _ADCINC_1_Start
       04DE  _ADCINC_1_SetPower
       04DE  ADCINC_1_SetPower
       04F6  _ADCINC_1_Stop
       04F6  ADCINC_1_Stop
       0503  ADCINC_1_GetSamples
       0503  _ADCINC_1_GetSamples
       0525  _ADCINC_1_StopADC
       0525  ADCINC_1_StopADC
       0535  _ADCINC_1_fIsDataAvailable
       0535  ADCINC_1_fIsDataAvailable
       0538  ADCINC_1_iClearFlagGetData
       0538  ADCINC_1_wClearFlagGetData
       0538  _ADCINC_1_wClearFlagGetData
       0538  _ADCINC_1_iClearFlagGetData
       0545  ADCINC_1_cClearFlagGetData
       0545  _ADCINC_1_bClearFlagGetData
       0545  _ADCINC_1_cClearFlagGetData
       0545  ADCINC_1_bClearFlagGetData
       054B  ADCINC_1_iGetData
       054B  ADCINC_1_wGetData
       054B  _ADCINC_1_wGetData
       054B  _ADCINC_1_iGetData
       0550  ADCINC_1_bGetData
       0550  ADCINC_1_cGetData
       0550  _ADCINC_1_bGetData
       0550  _ADCINC_1_cGetData
       0553  _ADCINC_1_fClearFlag
       0553  ADCINC_1_fClearFlag
       0559  _ADCINC_1_WritePulseWidth
       0559  ADCINC_1_WritePulseWidth
       055C  __UserModules_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                            text   055C   0192 =    402. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       055C  _main
       055C  __text_start
       0609  _readMagEncConfig
       06EE  __text_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                            data   0000   0009 =      9. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0000  _bytes_received
       0000  __data_start
       0001  _ext_mem_locked
       0002  _m_to_s_offset
       0003  _sin_value
       0005  _cos_value
       0007  _wait_cycle
       0009  __data_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
               virtual_registers   0009   0002 =      2. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0009  __r1
       000A  __r0
       000B  __virtual_registers_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                    InterruptRAM   000B   0008 =      8. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       000B  _NO_SHADOW
       000B  NO_SHADOW
       000B  ADCINC_1_iResult
       000B  _ADCINC_1_iResult
       000F  _ADCINC_1_fStatus
       000F  ADCINC_1_fStatus
       0010  _ADCINC_1_bState
       0010  ADCINC_1_bState
       0011  _ADCINC_1_fMode
       0011  ADCINC_1_fMode
       0012  ADCINC_1_bNumSamples
       0012  _ADCINC_1_bNumSamples
       0013  __InterruptRAM_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                             bss   0013   0043 =     67. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0013  _pwm_count
       0013  __bss_start
       0014  _s_to_m_mem
       0034  _m_to_s_mem
       0054  _expected_bytes
       0055  _target_address
       0056  __bss_end
       0056  __ramareas_end

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
<library>	[ uartint.asm, uart.asm, psocconfigtbl.asm, psocconfig.asm, pga_1.asm, adcinc_1int.asm, adcinc_1.asm ]
[ r1.asm, r0.asm ]

Area Definitions

-blit:0x150.0xfff
-bdata:0.0xff

