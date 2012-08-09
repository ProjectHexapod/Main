/*
 * File:        custom_data.c
 * Purpose:     Initial values for parameters stored in Flash
 *
 * Notes:
 *
 */

#include "cf_board.h"
#include "setget.h"

//#include "uart.h"
#include "spi.h"

    /************Smtp servers****/
    /*"remotesmtp.freescale.net"*/
    /*"rolex.freescale.net"*/
    /*"smtp.gmail.com"*/
    /*"smtp.mail.yahoo.com"*/
    /*"smtp.live.com"*/

/********************************************************************/
/* 
 * Default Settings 
 */ROM_OPTIONS
const  params = 
{
    /*FSL:Ethernet options*/
    COLDFIRE_MAC_ADDRESS,                     /*mac address*/
    CF_IP_ADDRESS,                            /*ip add*/
    CF_MASK_ADDRESS,                          /*subnet mask*/
    CF_GATEWAY_ADDRESS,                       /*gateway add*/
    CF_SERVER_ADDRESS,                        /*server add*/
    0,                                        /*dhcp client off*/
    0,                                        /*don't care*/
    
    /*FSL:bridge options*/
    1,                                        /*Configuration: OFF*/
    0,                                        /*Bridge: UART bridge*/
    0,                                        /*Server: YES*/    
    TCP_PORT,                                 /*TCP port*/
    0,                                        /*don't care*/
    
    /*FSL:UART options*/
    UART_PORT,                                /*uart port*/
    UART_BAUD,                                /*baudrate*/
    0,                                        /*no parity*/
    3,                                        /*8 bits*/
    0,                                        /*stop bits*/
    2,                                        /*xon/xoff*/
    0,                                        /*don't care*/

    /*FSL:SPI options*/
    SPI_PORT,                                 /*spi port*/
    BAUD_1000,                                /*spi baudrate*/
    0,                                        /*idle high*/
    0,                                        /*middle sample*/
    1,                                        /*spi master mode*/
    0,                                        /*polling*/
    0,                                        /*don't care*/
    
    /*FSL:Email options*/
    /*"MCF51CN128@freescale.com"*/"lasko.coldfire@yahoo.com",               /*username*/
    "Freescale123",                           /*password*/
    /*"remotesmtp.freescale.net"*/"smtp113.plus.mail.mud.yahoo.com",        /*smtp server address*/
    1/*0*/                                         /*authentication: ON*/
};
/********************************************************************/