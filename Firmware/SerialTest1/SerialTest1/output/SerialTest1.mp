Project:      output/SerialTest1
Build Number: 0
Date:         Sat May 28 00:49:43 2011
Compiler:     ICCM8C
Version:      7.04

  ROM 17% full. 658 out of 4096 bytes used (does not include absolute areas).
  RAM 8% full. 20 bytes used (does not include stack usage).

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                           idata   0150   0001 =      1. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0150  __idata_start
       0151  __idata_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                     psoc_config   0151   00F6 =    246. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0151  LoadConfigTBL_serialtest1
       023D  LoadConfigInit
       023D  _LoadConfigInit
       0241  _LoadConfig_serialtest1
       0241  LoadConfig_serialtest1
       0247  __psoc_config_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                     UserModules   0247   0178 =    376. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       0247  _UART_TX_ISR
       0248  _UART_RX_ISR
       028B  _UART_EnableInt
       028B  UART_EnableInt
       0292  _UART_DisableInt
       0292  UART_DisableInt
       0299  _UART_SetTxIntMode
       0299  UART_SetTxIntMode
       02AB  _UART_Start
       02AB  UART_Start
       02B2  UART_Stop
       02B2  _UART_Stop
       02B9  UART_SendData
       02B9  _UART_SendData
       02BC  UART_bReadTxStatus
       02BC  bUART_ReadTxStatus
       02BC  _bUART_ReadTxStatus
       02BC  _UART_bReadTxStatus
       02BF  _bUART_ReadRxData
       02BF  _UART_bReadRxData
       02BF  UART_bReadRxData
       02BF  bUART_ReadRxData
       02C2  bUART_ReadRxStatus
       02C2  _bUART_ReadRxStatus
       02C2  _UART_bReadRxStatus
       02C2  UART_bReadRxStatus
       02C5  UART_TxIntMode
       02C5  _UART_TxIntMode
       02D8  UART_IntCntl
       02D8  _UART_IntCntl
       0303  UART_PutSHexByte
       0303  _UART_PutSHexByte
       0316  _UART_PutSHexInt
       0316  UART_PutSHexInt
       031D  UART_PutChar
       031D  _UART_PutChar
       0325  _UART_cGetChar
       0325  UART_cGetChar
       032D  UART_cReadChar
       032D  _UART_cReadChar
       0344  _UART_iReadChar
       0344  UART_iReadChar
       035A  UART_PutString
       035A  _UART_PutString
       0364  UART_Write
       0364  _UART_Write
       037C  _UART_CWrite
       037C  UART_CWrite
       03A4  _UART_CPutString
       03A4  UART_CPutString
       03B6  UART_PutCRLF
       03B6  _UART_PutCRLF
       03BF  __UserModules_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                            text   03BF   0023 =     35. bytes (rel,con,rom)

       Addr  Global Symbol
      -----  --------------------------------
       03BF  _fullPacketReceived
       03BF  __text_start
       03C0  _main
       03E2  __text_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                            data   0000   0001 =      1. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0000  _bytes_received
       0000  __data_start
       0001  __data_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
               virtual_registers   0001   0001 =      1. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0001  __r0
       0002  __virtual_registers_end

Area                               Addr   Size   Decimal Bytes (Attributes)
--------------------------------   ----   ----   ------- ----- ------------
                             bss   0002   0012 =     18. bytes (rel,con,ram)

       Addr  Global Symbol
      -----  --------------------------------
       0002  __bss_start
       0002  _received_data_buffer
       0012  _expected_bytes
       0013  _target_address
       0014  __bss_end
       0014  __ramareas_end

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

