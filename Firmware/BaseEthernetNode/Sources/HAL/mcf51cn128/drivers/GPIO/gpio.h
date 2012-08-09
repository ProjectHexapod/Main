#ifndef _GPIO_H_
#define _GPIO_H_

#include "m51cn128evb.h"

/*****************************************************************************/
/*****************************************************************************/
/*********************************************** TOWER ***********************/
/*****************************************************************************/
/*****************************************************************************/

/*FSL: signal file to get GPIO functionality*/
#ifdef V1_TOWER 

//******DEMO SELECTOR

#define DEMO_SELECTOR                   /*dont care*/
#define DEMO_SELECTOR_INIT              /*dont care*/

#define DEMO_SELECTOR_ON                /*dont care*/
#define DEMO_SELECTOR_OFF               /*dont care*/

//******DEBUG

#define BKGD_WORKAROUND                 PTDDS_PTDDS6=1; //full drive on BKGD

//******CLOCK

#define CLOCK_OSC_OUT_INIT              SOPT3_CS  = 0b010;/*select MCGOUT on clkout pin*/PTEPF1_E4 = 0b10;/*clkout pin  ON*/
#define EXTAL_PIN_INIT                  PTDPF1_D4 = 0b11;   // extal pin ON
#define XTAL_PIN_INIT                   PTDPF1_D5 = 0b11;   // xtal pin ON

//******SPI1

#define SPI1_SS_GPIO                    PTCD_PTCD4
#define SPI1_SS_GPIO_INIT               PTCPF1_C4 = 0;/*GPIO for SS*/PTCDD_PTCDD4 = 1;/*SS1:output pin*/PTCD_PTCD4 = 1;/*high state*/
#define SPI1_SS_INIT                    PTCPF1_C4 = 2;//SS1
#define SPI1_MOSI_MISO_CLK_INIT         PTCPF1_C5 = 2;/*MOSI1*/PTCPF1_C6 = 2;/*MISO1*/PTCPF1_C7 = 2;/*SPSCK1*/

//******SPI2

#define SPI2_SS_GPIO                    PTED_PTED2
#define SPI2_SS_GPIO_INIT               PTEPF2_E2 = 0;/*GPIO for SS*/PTEDD_PTEDD2 = 1;/*SS2:output pin*/PTED_PTED2 = 1;/*high state*/
#define SPI2_SS_INIT                    PTEPF2_E2 = 2;//SS2
#define SPI2_MOSI_MISO_CLK_INIT         PTEPF2_E1 = 2;/*MOSI2*/PTEPF2_E0 = 2;/*MISO2*/PTDPF1_D7 = 2;/*SPSCK2*/

//******SDCARD

#define SD_CARD_SPI_PORT                1/*Second Port*/

/* SD card Inserted detection Pin */
#define SD_PRESENT                      PTED_PTED6
#define SD_PRESENT_INIT                 PTEDD_PTEDD6=0/*input*/
/* SD Card Write Protect Pin */
#define SD_PROTECTED                    PTGD_PTGD7
#define SD_PROTECTED_INIT               PTGDD_PTGDD7=0/*input*/

#define SD_SPI_MAX_BAUDRATE             BAUD_6250

/* SD Card Chip Select assignment */
#define SPI_SS                          SPI2_SS_GPIO

//******UARTS

#define UART1_TX_RX_INIT                PTDPF2_D0 = 2;PTDPF2_D1 = 2;
#define UART2_TX_RX_INIT                PTDPF2_D2 = 2;PTDPF2_D3 = 2;
#define UART3_TX_RX_INIT                PTEPF1_E6 = 3;PTEPF1_E7 = 3;
//SC11
#define UART1_CTS                       PTED_PTED1
#define UART1_CTS_INIT                  PTEPF2_E1 = 0;/*GPIO function*/PTEDD_PTEDD1=0;/*input*/
#define UART1_RTS                       PTED_PTED2
#define UART1_RTS_INIT                  PTEPF2_E2 = 0;/*GPIO function*/PTEDD_PTEDD2=1;/*output*/PTED_PTED2=0;/*enabling UART communication at other side*/
//SCI2
#define UART2_CTS                       /*dont care*/
#define UART2_CTS_INIT                  /*dont care*/                                        
#define UART2_RTS                       /*dont care*/
#define UART2_RTS_INIT                  /*dont care*/
//SCI3
#define UART3_CTS                       /*dont care*/
#define UART3_CTS_INIT                  /*dont care*/                                        
#define UART3_RTS                       /*dont care*/
#define UART3_RTS_INIT                  /*dont care*/

//******I2C1
#define I2C1_SDA_SCL_INIT               /*dont care*/

//******I2C2
#define I2C2_SDA_SCL_INIT               /*dont care*/

//******LED
#define LED_VALUE                       PTED_PTED3
#define LED_VALUE_INIT                  PTEPF2_E3 = 0;/*gpio*/PTEDD_PTEDD3=1/*output*/

//******Buttons
//Button 1:
#define RST_GPIO                        PTCD_PTCD3
#define RST_GPIO_INIT                   PTCPF2_C3 = 0b01;

//Button 2
#define BUTTON_GPIO_SW2                 /*dont care*/
#define BUTTON_GPIO_SW2_INIT            /*dont care*/
#define BUTTON_KBI_SW2_INIT             /*dont care*/
#define BUTTON_IRQ_SW2_INIT             /*dont care*/

//Button 3
#define BUTTON_GPIO_SW3                 /*dont care*/
#define BUTTON_GPIO_SW3_INIT            /*dont care*/
#define BUTTON_KBI_SW3_INIT             /*dont care*/

#endif/*V1_TOWER end*/

/*****************************************************************************/
/*****************************************************************************/
/*********************************************** COPACABANA ******************/
/*****************************************************************************/
/*****************************************************************************/

#ifdef M51CN128RD

//******DEMO SELECTOR

#define DEMO_SELECTOR                   PTED_PTED3
#define DEMO_SELECTOR_INIT              PTEPF2_E3 = 0b00;/*gpio*/PTEDD_PTEDD3=1;/*output*/PTEPE_PTEPE3=1;/*pull-up on*/PTED_PTED3=0;/*low level*/

#define DEMO_SELECTOR_ON                DEMO_SELECTOR=1;
#define DEMO_SELECTOR_OFF               DEMO_SELECTOR=0;

//******DEBUG

#define BKGD_WORKAROUND                 PTDDS_PTDDS6=1; //full drive on BKGD

//******CLOCK

#define CLOCK_OSC_OUT_INIT              SOPT3_CS  = 0b010;/*select MCGOUT on clkout pin*/PTEPF1_E4 = 0b10;/*clkout pin  ON*/
#define EXTAL_PIN_INIT                  PTDPF1_D4 = 0b11;   // extal pin ON
#define XTAL_PIN_INIT                   PTDPF1_D5 = 0b11;   // xtal pin ON

//******SPI1

#define SPI1_SS_GPIO                    PTBD_PTBD2
#define SPI1_SS_GPIO_INIT               PTBPF2_B2 = 0;/*GPIO for SS*/PTBDD_PTBDD2 = 1;/*SS1:output pin*/PTBD_PTBD2 = 1;/*high state*/
#define SPI1_SS_INIT                    PTBPF2_B2 = 2;//SS1
#define SPI1_MOSI_MISO_CLK_INIT         PTCPF1_C5 = 2;/*MOSI1*/PTCPF1_C6 = 2;/*MISO1*/PTCPF1_C7 = 2;/*SPSCK1*/

//******SPI2

#define SPI2_SS_GPIO                    PTED_PTED2
#define SPI2_SS_GPIO_INIT               PTEPF2_E2 = 0;/*GPIO for SS*/PTEDD_PTEDD2 = 1;/*SS2:output pin*/PTED_PTED2 = 1;/*high state*/
#define SPI2_SS_INIT                    PTEPF2_E2 = 2;//SS2
#define SPI2_MOSI_MISO_CLK_INIT         PTEPF2_E1 = 2;/*MOSI2*/PTEPF2_E0 = 2;/*MISO2*/PTDPF1_D7 = 2;/*SPSCK2*/

//******SDCARD

#define SD_CARD_SPI_PORT                0/*First Port*/

/* SD card Inserted detection Pin */
#define SD_PRESENT                      PTED_PTED0
#define SD_PRESENT_INIT                 PTEPF2_E0=0;/*gpio*/PTEDD_PTEDD0=0;/*input*/PTEPE_PTEPE0=1;/*pull-up*/
/* SD Card Write Protect Pin */
#define SD_PROTECTED                    0/*dont care*/
#define SD_PROTECTED_INIT               /*dont care*/

#define SD_SPI_MAX_BAUDRATE             BAUD_12500

/* SD Card Chip Select assignment */
#define SPI_SS                          SPI1_SS_GPIO

//******UARTS

#define UART1_TX_RX_INIT                PTDPF2_D0 = 2;PTDPF2_D1 = 2;
#define UART2_TX_RX_INIT                PTDPF2_D2 = 2;PTDPF2_D3 = 2;
#define UART3_TX_RX_INIT                /*dont care*/
//SC11
#define UART1_CTS                       PTCD_PTCD5
#define UART1_CTS_INIT                  PTCPF1_C5 = 0;/*GPIO function*/PTCDD_PTCDD5=0;/*input*/
#define UART1_RTS                       PTCD_PTCD4
#define UART1_RTS_INIT                  PTCPF1_C4 = 0;/*GPIO function*/PTCDD_PTCDD4=1;/*output*/PTCD_PTCD4=0;/*enabling UART communication at other side*/
//SCI2
#define UART2_CTS                       /*dont care*/
#define UART2_CTS_INIT                  /*dont care*/                                        
#define UART2_RTS                       /*dont care*/
#define UART2_RTS_INIT                  /*dont care*/
//SCI3
#define UART3_CTS                       /*dont care*/
#define UART3_CTS_INIT                  /*dont care*/                                        
#define UART3_RTS                       /*dont care*/
#define UART3_RTS_INIT                  /*dont care*/

//******I2C1
#define I2C1_SDA_SCL_INIT               /*dont care*/

//******I2C2
#define I2C2_SDA_SCL_INIT               PTCPF1_C7 = 0b01;/*SDA*/PTCPF1_C6 = 0b01;/*SCL*/

//******LED
#define LED_VALUE                       PTED_PTED2
#define LED_VALUE_INIT                  PTEPF2_E2 = 0;/*gpio*/PTEDD_PTEDD2=1/*output*/

//******Buttons
//Button 1:
#define RST_GPIO                        PTCD_PTCD3
#define RST_GPIO_INIT                   PTCPF2_C3 = 0b01;

//Button 2
#define BUTTON_GPIO_SW2                 PTED_PTED5
#define BUTTON_GPIO_SW2_INIT            PTEPF1_E5 = 0b00;
#define BUTTON_KBI_SW2_INIT             PTEPF1_E5 = 0b01;
#define BUTTON_IRQ_SW2_INIT             PTEPF1_E5 = 0b10;

//Button 3
#define BUTTON_GPIO_SW3                 PTED_PTED4
#define BUTTON_GPIO_SW3_INIT            PTEPF1_E4 = 0b00;
#define BUTTON_KBI_SW3_INIT             PTEPF1_E4 = 0b01;

#endif/*M51CN128RD end*/

/*****************************************************************************/
/*****************************************************************************/
/*********************************************** SHARED **********************/
/*****************************************************************************/
/*****************************************************************************/


/*****************************************************************************/

/*prototypes*/

/**
 * Configure FEC pins to selected pins
 * @param none  
 * @return none
 */
void 
GPIO_FECPinsInit(void);

/**
 * Configure ADC pins to selected pin
 * @param adc channel 
 * @return none
 */
void
GPIO_ADCPinsInit(uint8 adc_channel);

/**
 * Configure MCU pins to low power mode
 * @param none  
 * @return none
 */
void 
GPIO_MCUPinsInit();

#endif