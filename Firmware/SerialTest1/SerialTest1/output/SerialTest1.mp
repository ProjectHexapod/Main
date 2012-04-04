Project:      output/SerialTest1
Build Number: 0
Date:         Tue Apr  3 20:48:42 2012
Compiler:     ICCM8C
Version:      7.04

  ROM 25% full. 1006 out of 4096 bytes used (does not include absolute areas).
  RAM 30% full. 76 bytes used (does not include stack usage).

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
                     UserModules   0285   027F =    639. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0285  _UART_TX_ISR
       0286  _UART_RX_ISR
       02E4  UART_EnableInt
       02E4  _UART_EnableInt
       02EB  _UART_DisableInt
       02EB  UART_DisableInt
       02F2  UART_SetTxIntMode
       02F2  _UART_SetTxIntMode
       0304  _UART_Start
       0304  UART_Start
       030B  UART_Stop
       030B  _UART_Stop
       0312  UART_SendData
       0312  _UART_SendData
       0315  _bUART_ReadTxStatus
       0315  _UART_bReadTxStatus
       0315  bUART_ReadTxStatus
       0315  UART_bReadTxStatus
       0318  UART_bReadRxData
       0318  _bUART_ReadRxData
       0318  _UART_bReadRxData
       0318  bUART_ReadRxData
       031B  UART_bReadRxStatus
       031B  _UART_bReadRxStatus
       031B  bUART_ReadRxStatus
       031B  _bUART_ReadRxStatus
       031E  _UART_TxIntMode
       031E  UART_TxIntMode
       0331  UART_IntCntl
       0331  _UART_IntCntl
       035C  UART_PutSHexByte
       035C  _UART_PutSHexByte
       036F  _UART_PutSHexInt
       036F  UART_PutSHexInt
       0376  UART_PutChar
       0376  _UART_PutChar
       037E  _UART_cGetChar
       037E  UART_cGetChar
       0386  UART_cReadChar
       0386  _UART_cReadChar
       039D  _UART_iReadChar
       039D  UART_iReadChar
       03B3  UART_PutString
       03B3  _UART_PutString
       03BD  _UART_Write
       03BD  UART_Write
       03D5  UART_CWrite
       03D5  _UART_CWrite
       03FD  _UART_CPutString
       03FD  UART_CPutString
       040F  _UART_PutCRLF
       040F  UART_PutCRLF
       0418  PWM8_EnableInt
       0418  _PWM8_EnableInt
       041C  PWM8_DisableInt
       041C  _PWM8_DisableInt
       0420  _PWM8_Start
       0420  PWM8_Start
       0424  PWM8_Stop
       0424  _PWM8_Stop
       0428  PWM8_WritePeriod
       0428  _PWM8_WritePeriod
       042B  PWM8_WritePulseWidth
       042B  _PWM8_WritePulseWidth
       042E  _PWM8_bReadPulseWidth
       042E  PWM8_bReadPulseWidth
       042E  _bPWM8_ReadPulseWidth
       042E  bPWM8_ReadPulseWidth
       0431  _PWM8_bReadCounter
       0431  PWM8_bReadCounter
       0431  bPWM8_ReadCounter
       0431  _bPWM8_ReadCounter
       045A  _PGA_1_SetPower
       045A  PGA_1_SetPower
       045A  PGA_1_Start
       045A  _PGA_1_Start
       0468  PGA_1_SetGain
       0468  _PGA_1_SetGain
       048A  PGA_1_Stop
       048A  _PGA_1_Stop
       048E  _DELSIG8_ADConversion_ISR
       04C7  _DELSIG8_Start
       04C7  DELSIG8_SetPower
       04C7  _DELSIG8_SetPower
       04C7  DELSIG8_Start
       04D5  DELSIG8_Stop
       04D5  _DELSIG8_Stop
       04D9  DELSIG8_StartAD
       04D9  _DELSIG8_StartAD
       04F0  DELSIG8_StopAD
       04F0  _DELSIG8_StopAD
       0504  __UserModules_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                            text   0504   003A =     58. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0504  _main
       0504  __text_start
       053E  __text_end

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
                    InterruptRAM   0004   0006 =      6. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0004  NO_SHADOW
       0004  _NO_SHADOW
       000A  __InterruptRAM_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                             bss   000A   0042 =     66. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       000A  _s_to_m_mem
       000A  __bss_start
       002A  _m_to_s_mem
       004A  _expected_bytes
       004B  _target_address
       004C  __bss_end
       004C  __ramareas_end

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
<library>	[ uartint.asm, uart.asm, pwm8.asm, psocconfigtbl.asm, psocconfig.asm, pga_1.asm, delsig8int.asm ]
[ delsig8.asm, r0.asm ]

Area Definitions

-blit:0x150.0xfff
-bdata:0.0xff

