Project:      output/ValveDriver
Build Number: 0
Date:         Mon May 21 03:53:22 2012
Compiler:     ICCM8C
Version:      7.05.00


Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                           idata   0150   0002 =      2. bytes (rel,con,rom,lit)

       Addr  Global Symbol
      -----  --------------------------------
       0150  __idata_start
       0152  __idata_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                     psoc_config   0152   011A =    282. bytes (rel,con,rom,code)

       Addr  Global Symbol
      -----  --------------------------------
       0152  LoadConfigTBL_ValveDriver
       0262  LoadConfigInit
       0262  _LoadConfigInit
       0266  _LoadConfig_ValveDriver
       0266  LoadConfig_ValveDriver
       026C  __psoc_config_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                     UserModules   026C   00D2 =    210. bytes (rel,con,rom,code)

       Addr  Global Symbol
      -----  --------------------------------
       026C  _UART_TX_ISR
       026D  _UART_RX_ISR
       02B7  _UART_EnableInt
       02B7  UART_EnableInt
       02BE  _UART_Start
       02BE  _UART_SetTxIntMode
       02BE  UART_Start
       02BE  _UART_DisableInt
       02C5  _bUART_ReadRxData
       02C5  _UART_TxIntMode
       02C5  bUART_ReadRxData
       02C5  bUART_ReadTxStatus
       02C5  bUART_ReadRxStatus
       02C5  _UART_bReadRxData
       02C5  _bUART_ReadTxStatus
       02C5  _UART_Stop
       02C5  _UART_IntCntl
       02C5  _UART_bReadTxStatus
       02C5  _UART_bReadRxStatus
       02C5  _bUART_ReadRxStatus
       02C5  _UART_SendData
       02D5  UART_PutSHexByte
       02D5  _UART_PutSHexByte
       02E8  _UART_PutChar
       02E8  UART_PutChar
       02E8  _UART_PutSHexInt
       02F0  _UART_cGetChar
       02F0  UART_cGetChar
       02F8  _UART_PutString
       02F8  _UART_iReadChar
       02F8  _UART_cReadChar
       02F8  UART_PutString
       0302  UART_CPutString
       0302  _UART_Write
       0302  _UART_CPutString
       0302  _UART_CWrite
       0314  _UART_PutCRLF
       0314  _SleepTimer_1_ISR
       0328  PWM8_2_DisableInt
       0328  _PWM8_2_EnableInt
       0328  _PWM8_2_DisableInt
       032C  _PWM8_2_Start
       032C  PWM8_2_Start
       0330  _PWM8_2_WritePulseWidth
       0330  _PWM8_2_WritePeriod
       0330  PWM8_2_WritePulseWidth
       0330  _PWM8_2_Stop
       0333  _PWM8_1_EnableInt
       0333  bPWM8_2_ReadPulseWidth
       0333  _PWM8_1_DisableInt
       0333  bPWM8_2_ReadCounter
       0333  _bPWM8_2_ReadCounter
       0333  _PWM8_2_bReadCounter
       0333  _PWM8_2_bReadPulseWidth
       0333  PWM8_1_DisableInt
       0333  _bPWM8_2_ReadPulseWidth
       0337  PWM8_1_Start
       0337  _PWM8_1_Start
       033B  _PWM8_1_WritePulseWidth
       033B  _PWM8_1_Stop
       033B  PWM8_1_WritePulseWidth
       033B  _PWM8_1_WritePeriod
       033E  bPWM8_1_ReadCounter
       033E  _PWM8_1_bReadPulseWidth
       033E  _bPWM8_1_ReadPulseWidth
       033E  __UserModules_end
       033E  _bPWM8_1_ReadCounter
       033E  bPWM8_1_ReadPulseWidth
       033E  _PWM8_1_bReadCounter

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                            text   033E   002E =     46. bytes (rel,con,rom,code)

       Addr  Global Symbol
      -----  --------------------------------
       033E  __text_start
       033E  _main
       036C  __text_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                            data   0000   0002 =      2. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0000  __data_start
       0000  _transfer_offset_valid
       0001  _ext_mem_locked
       0002  __data_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
               virtual_registers   0002   0001 =      1. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0002  __r0
       0003  __virtual_registers_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                    InterruptRAM   0003   0004 =      4. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0003  SleepTimer_1_fTick
       0003  _SleepTimer_1_fTick
       0004  SleepTimer_1_bTimerValue
       0004  _SleepTimer_1_bTimerValue
       0005  SleepTimer_1_bCountDown
       0005  _SleepTimer_1_bCountDown
       0006  SleepTimer_1_TickCount
       0006  _SleepTimer_1_TickCount
       0007  NO_SHADOW
       0007  __InterruptRAM_end
       0007  _NO_SHADOW

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                             bss   0007   0044 =     68. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0007  _s_to_m_mem
       0007  __bss_start
       0027  _m_to_s_mem
       0047  _transfer_offset
       0048  _transfer_flags
       0049  _expected_bytes
       004A  _target_address
       004B  __ramareas_end
       004B  __bss_end

Area                               Start  End    Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                             TOP   0000   00D4 =    212. bytes (abs,ovr,rom,code)

       Addr  Global Symbol
      -----  --------------------------------
       0068  __Start
       00D1  _bGetPowerSetting
       00D1  bGetPowerSetting

Files Linked      [ module(s) ]

./obj/boot.o	[ boot.asm ]
./obj/main.o	[ main.c ]
<library>	[ uartint.asm, uart.asm, sleeptimer_1int.asm, pwm8_2.asm, pwm8_1.asm, psocconfigtbl.asm, psocconfig.asm ]
[ r0.asm ]

Area Definitions

-blit:0x150.0xfff
-bdata:0.0xff
-rwh:SSCParmBlk:0xf7.0xff

