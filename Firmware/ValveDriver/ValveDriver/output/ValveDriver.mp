Project:      output/ValveDriver
Build Number: 0
Date:         Sun May  6 17:05:14 2012
Compiler:     ICCM8C
Version:      7.04

  ROM 19% full. 778 out of 4096 bytes used (does not include absolute areas).
  RAM 28% full. 71 bytes used (does not include stack usage).

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                           idata   0150   0003 =      3. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0150  __idata_start
       0153  __idata_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                     psoc_config   0153   00F6 =    246. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0153  LoadConfigTBL_ValveDriver
       023F  LoadConfigInit
       023F  _LoadConfigInit
       0243  _LoadConfig_ValveDriver
       0243  LoadConfig_ValveDriver
       0249  __psoc_config_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                     UserModules   0249   0192 =    402. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0249  _UART_TX_ISR
       024A  _UART_RX_ISR
       02A7  _UART_EnableInt
       02A7  UART_EnableInt
       02AE  _UART_DisableInt
       02AE  UART_DisableInt
       02B5  _UART_SetTxIntMode
       02B5  UART_SetTxIntMode
       02C7  _UART_Start
       02C7  UART_Start
       02CE  UART_Stop
       02CE  _UART_Stop
       02D5  UART_SendData
       02D5  _UART_SendData
       02D8  UART_bReadTxStatus
       02D8  bUART_ReadTxStatus
       02D8  _bUART_ReadTxStatus
       02D8  _UART_bReadTxStatus
       02DB  _bUART_ReadRxData
       02DB  _UART_bReadRxData
       02DB  UART_bReadRxData
       02DB  bUART_ReadRxData
       02DE  bUART_ReadRxStatus
       02DE  _bUART_ReadRxStatus
       02DE  _UART_bReadRxStatus
       02DE  UART_bReadRxStatus
       02E1  UART_TxIntMode
       02E1  _UART_TxIntMode
       02F4  UART_IntCntl
       02F4  _UART_IntCntl
       031F  UART_PutSHexByte
       031F  _UART_PutSHexByte
       0332  _UART_PutSHexInt
       0332  UART_PutSHexInt
       0339  UART_PutChar
       0339  _UART_PutChar
       0341  _UART_cGetChar
       0341  UART_cGetChar
       0349  UART_cReadChar
       0349  _UART_cReadChar
       0360  _UART_iReadChar
       0360  UART_iReadChar
       0376  UART_PutString
       0376  _UART_PutString
       0380  UART_Write
       0380  _UART_Write
       0398  _UART_CWrite
       0398  UART_CWrite
       03C0  _UART_CPutString
       03C0  UART_CPutString
       03D2  UART_PutCRLF
       03D2  _UART_PutCRLF
       03DB  __UserModules_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                            text   03DB   007F =    127. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       03DB  _main
       03DB  __text_start
       045A  __text_end

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
                             bss   0004   0043 =     67. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0004  _pwm_count
       0004  __bss_start
       0005  _s_to_m_mem
       0025  _m_to_s_mem
       0045  _expected_bytes
       0046  _target_address
       0047  __bss_end
       0047  __ramareas_end

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
<library>	[ uartint.asm, uart.asm, psocconfigtbl.asm, psocconfig.asm, r0.asm ]

Area Definitions

-blit:0x150.0xfff
-bdata:0.0xff

