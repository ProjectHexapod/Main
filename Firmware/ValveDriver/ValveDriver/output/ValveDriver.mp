Project:      output/ValveDriver
Build Number: 0
Date:         Mon May 14 21:54:33 2012
Compiler:     ICCM8C
Version:      7.04

  ROM 22% full. 867 out of 4096 bytes used (does not include absolute areas).
  RAM 28% full. 70 bytes used (does not include stack usage).

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                           idata   0150   0003 =      3. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0150  __idata_start
       0153  __idata_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                     psoc_config   0153   011A =    282. bytes (rel,con,rom)

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
                     UserModules   026D   0218 =    536. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       026D  _UART_TX_ISR
       026E  _UART_RX_ISR
       02CB  UART_EnableInt
       02CB  _UART_EnableInt
       02D2  UART_DisableInt
       02D2  _UART_DisableInt
       02D9  _UART_SetTxIntMode
       02D9  UART_SetTxIntMode
       02EB  _UART_Start
       02EB  UART_Start
       02F2  UART_Stop
       02F2  _UART_Stop
       02F9  _UART_SendData
       02F9  UART_SendData
       02FC  _bUART_ReadTxStatus
       02FC  bUART_ReadTxStatus
       02FC  UART_bReadTxStatus
       02FC  _UART_bReadTxStatus
       02FF  _UART_bReadRxData
       02FF  _bUART_ReadRxData
       02FF  bUART_ReadRxData
       02FF  UART_bReadRxData
       0302  _UART_bReadRxStatus
       0302  _bUART_ReadRxStatus
       0302  bUART_ReadRxStatus
       0302  UART_bReadRxStatus
       0305  UART_TxIntMode
       0305  _UART_TxIntMode
       0318  _UART_IntCntl
       0318  UART_IntCntl
       0343  UART_PutSHexByte
       0343  _UART_PutSHexByte
       0356  _UART_PutSHexInt
       0356  UART_PutSHexInt
       035D  UART_PutChar
       035D  _UART_PutChar
       0365  _UART_cGetChar
       0365  UART_cGetChar
       036D  UART_cReadChar
       036D  _UART_cReadChar
       0384  _UART_iReadChar
       0384  UART_iReadChar
       039A  UART_PutString
       039A  _UART_PutString
       03A4  _UART_Write
       03A4  UART_Write
       03BC  _UART_CWrite
       03BC  UART_CWrite
       03E4  UART_CPutString
       03E4  _UART_CPutString
       03F6  _UART_PutCRLF
       03F6  UART_PutCRLF
       03FF  _PWM8_2_ISR
       0400  _PWM8_2_EnableInt
       0400  PWM8_2_EnableInt
       0404  PWM8_2_DisableInt
       0404  _PWM8_2_DisableInt
       0408  PWM8_2_Start
       0408  _PWM8_2_Start
       040C  PWM8_2_Stop
       040C  _PWM8_2_Stop
       0410  _PWM8_2_WritePeriod
       0410  PWM8_2_WritePeriod
       0413  _PWM8_2_WritePulseWidth
       0413  PWM8_2_WritePulseWidth
       0416  bPWM8_2_ReadPulseWidth
       0416  _bPWM8_2_ReadPulseWidth
       0416  PWM8_2_bReadPulseWidth
       0416  _PWM8_2_bReadPulseWidth
       0419  PWM8_2_bReadCounter
       0419  bPWM8_2_ReadCounter
       0419  _PWM8_2_bReadCounter
       0419  _bPWM8_2_ReadCounter
       0442  _PWM8_1_ISR
       0443  PWM8_1_EnableInt
       0443  _PWM8_1_EnableInt
       0447  PWM8_1_DisableInt
       0447  _PWM8_1_DisableInt
       044B  PWM8_1_Start
       044B  _PWM8_1_Start
       044F  PWM8_1_Stop
       044F  _PWM8_1_Stop
       0453  PWM8_1_WritePeriod
       0453  _PWM8_1_WritePeriod
       0456  PWM8_1_WritePulseWidth
       0456  _PWM8_1_WritePulseWidth
       0459  PWM8_1_bReadPulseWidth
       0459  _bPWM8_1_ReadPulseWidth
       0459  _PWM8_1_bReadPulseWidth
       0459  bPWM8_1_ReadPulseWidth
       045C  _bPWM8_1_ReadCounter
       045C  PWM8_1_bReadCounter
       045C  bPWM8_1_ReadCounter
       045C  _PWM8_1_bReadCounter
       0485  __UserModules_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                            text   0485   002E =     46. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0485  _main
       0485  __text_start
       04B3  __text_end

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
                             bss   0004   0042 =     66. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0004  _s_to_m_mem
       0004  __bss_start
       0024  _m_to_s_mem
       0044  _expected_bytes
       0045  _target_address
       0046  __bss_end
       0046  __ramareas_end

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
<library>	[ uartint.asm, uart.asm, pwm8_2int.asm, pwm8_2.asm, pwm8_1int.asm, pwm8_1.asm, psocconfigtbl.asm ]
[ psocconfig.asm, r0.asm ]

Area Definitions

-blit:0x150.0xfff
-bdata:0.0xff

