/*
 * File:		M51CN128EVB.h
 * Purpose:		Evaluation board definitions and memory map information
 *
 * Notes:
 */

#ifndef _M51CN128EVB_H
#define _M51CN128EVB_H

/********************************************************************/

#include "mcf5xxx.h"
#include "derivative.h" /* include peripheral declarations */

/********************************************************************/

/*
 * Debug prints ON (#undef) or OFF (#define)
 */
#undef DEBUG

/*****************************************************************************/

/*Warning: only define one of them*/
#define M51CN128RD            /*pins moved to reference design hardware*/
//#define V1_TOWER              /*pins moved to reference design hardware*/

#ifdef M51CN128RD /*only defined for reference design*/
/*FSL: using external clock*/
#define EXTERNAL_CLOCK
/*MCU feeds PHY clock*/
#ifndef MCU_FED_PHY_CLK
#define MCU_FED_PHY_CLK			  1
#endif
#define UART_PORT				      0/*First Port*/
#endif

#ifdef V1_TOWER
#undef EXTERNAL_CLOCK
#define UART_PORT				      1/*Second Port*/
#endif 

/*
 * System Bus Clock Info
 */
#ifndef EXTERNAL_CLOCK
#define	SYSTEM_CLOCK		      50331648UL/* system bus frequency in Hz */
#else
#define	SYSTEM_CLOCK		      50000000UL/* system bus frequency in Hz */
#endif

#define UART_BAUD				      115200 /* 19200 */
#define ADC_CHANNEL           3//ADP3
#define SPI_PORT              1/*Second Port*/

/*
 * ColdFire Port specific
 */
 
/*internal or external PHY*/
#ifndef PHY_ON_CHIP
#define PHY_ON_CHIP			      0
#endif

/*100Mbps configuration*/
#ifndef SPEED_10BASET
#define SPEED_10BASET         0
#endif	

/*MAC address for this device*/
#define COLDFIRE_MAC_ADDRESS	{0x00, 0xCF, 0x52, 0x35, 0x00, 0x07}
#define CF_IP_ADDRESS         {192,168,1,3}
#define CF_MASK_ADDRESS       {255,255,255,0}
#define CF_GATEWAY_ADDRESS    {192,168,1,1}
#define CF_SERVER_ADDRESS     {192,168,1,81}/*cant be the same as IP address!!*/

/*Default Port for Bridge*/
#define TCP_PORT              1234
                                                      
/*
 * Ethernet Port Info
 */
#define FEC_PHY0			      (0x01)


/*Byte Reversing*/
#define BYTE_REVERSE_ON_HARDWARE 1//0

/*****************************************************************************/

/*Handy*/

#define LED0_TOG    PTDD^=PTDD_PTDD1_MASK
#define LED1_TOG    PTDD^=PTDD_PTDD2_MASK
#define LED2_TOG    PTDD^=PTDD_PTDD3_MASK

#define LED0_ON     PTDD_PTDD1=0
#define LED0_OFF    PTDD_PTDD1=1

#define LED1_ON     PTDD_PTDD2=0
#define LED1_OFF    PTDD_PTDD2=1

#define LED2_ON     PTDD_PTDD3=0
#define LED2_OFF    PTDD_PTDD3=1

#endif /* _M51CN128EVB_H_ */
