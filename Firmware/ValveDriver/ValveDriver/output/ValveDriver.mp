Project:      output/ValveDriver
Build Number: 0
Date:         Sun May 20 20:16:31 2012
Compiler:     ICCM8C
Version:      7.05.00


Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                           idata   0150   0003 =      3. bytes (rel,con,rom,lit)

       Addr  Global Symbol
      -----  --------------------------------
       0150  __idata_start
       0153  __idata_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                     psoc_config   0153   011A =    282. bytes (rel,con,rom,code)

       Addr  Global Symbol
      -----  --------------------------------
       0153  LoadConfigTBL_ValveDriver
       0263  LoadConfigInit
       0263  _LoadConfigInit
       0267  _LoadConfig_ValveDriver
       0267  LoadConfig_ValveDriver
       026D  __psoc_config_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                     UserModules   026D   00E9 =    233. bytes (rel,con,rom,code)

       Addr  Global Symbol
      -----  --------------------------------
       026D  _UART_TX_ISR
       026E  _UART_RX_ISR
       02CF  _UART_EnableInt
       02CF  UART_EnableInt
       02D6  _UART_Start
       02D6  _UART_SetTxIntMode
       02D6  UART_Start
       02D6  _UART_DisableInt
       02DD  _bUART_ReadRxData
       02DD  _UART_TxIntMode
       02DD  bUART_ReadRxData
       02DD  bUART_ReadTxStatus
       02DD  bUART_ReadRxStatus
       02DD  _UART_bReadRxData
       02DD  _bUART_ReadTxStatus
       02DD  _UART_Stop
       02DD  _UART_IntCntl
       02DD  _UART_bReadTxStatus
       02DD  _UART_bReadRxStatus
       02DD  _bUART_ReadRxStatus
       02DD  _UART_SendData
       02ED  UART_PutSHexByte
       02ED  _UART_PutSHexByte
       0300  _UART_PutChar
       0300  UART_PutChar
       0300  _UART_PutSHexInt
       0308  _UART_cGetChar
       0308  UART_cGetChar
       0310  _UART_PutString
       0310  _UART_iReadChar
       0310  _UART_cReadChar
       0310  UART_PutString
       031A  UART_CPutString
       031A  _UART_Write
       031A  _UART_CPutString
       031A  _UART_CWrite
       032C  _UART_PutCRLF
       032C  _SleepTimer_1_ISR
       0340  PWM8_2_DisableInt
       0340  _PWM8_2_EnableInt
       0340  _PWM8_2_DisableInt
       0344  _PWM8_2_Start
       0344  PWM8_2_Start
       0348  _PWM8_2_WritePulseWidth
       0348  _PWM8_2_WritePeriod
       0348  PWM8_2_WritePulseWidth
       0348  _PWM8_2_Stop
       034B  _PWM8_1_EnableInt
       034B  bPWM8_2_ReadPulseWidth
       034B  _PWM8_1_DisableInt
       034B  bPWM8_2_ReadCounter
       034B  _bPWM8_2_ReadCounter
       034B  _PWM8_2_bReadCounter
       034B  _PWM8_2_bReadPulseWidth
       034B  PWM8_1_DisableInt
       034B  _bPWM8_2_ReadPulseWidth
       034F  PWM8_1_Start
       034F  _PWM8_1_Start
       0353  _PWM8_1_WritePulseWidth
       0353  _PWM8_1_Stop
       0353  PWM8_1_WritePulseWidth
       0353  _PWM8_1_WritePeriod
       0356  bPWM8_1_ReadCounter
       0356  _PWM8_1_bReadPulseWidth
       0356  _bPWM8_1_ReadPulseWidth
       0356  __UserModules_end
       0356  _bPWM8_1_ReadCounter
       0356  bPWM8_1_ReadPulseWidth
       0356  _PWM8_1_bReadCounter

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                            text   0356   002B =     43. bytes (rel,con,rom,code)

       Addr  Global Symbol
      -----  --------------------------------
       0356  __text_start
       0356  _main
       0381  __text_end

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
                    InterruptRAM   0004   0004 =      4. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0004  SleepTimer_1_fTick
       0004  _SleepTimer_1_fTick
       0005  SleepTimer_1_bTimerValue
       0005  _SleepTimer_1_bTimerValue
       0006  SleepTimer_1_bCountDown
       0006  _SleepTimer_1_bCountDown
       0007  SleepTimer_1_TickCount
       0007  _SleepTimer_1_TickCount
       0008  NO_SHADOW
       0008  __InterruptRAM_end
       0008  _NO_SHADOW

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                             bss   0008   0042 =     66. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0008  _s_to_m_mem
       0008  __bss_start
       0028  _m_to_s_mem
       0048  _expected_bytes
       0049  _target_address
       004A  __ramareas_end
       004A  __bss_end

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

