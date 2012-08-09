/*
 * File:        spi.h
 *
 * Notes:       
 *              
 */

#ifndef __SPI_H__
#define __SPI_H__

/*SPI ports*/
#define SPI1_PORT              0
#define SPI2_PORT              1

#define NUMBER_OF_SPIs         2



//////////////////////////////////////////////////////////////

/*Allowed baudrates*/
#define BAUD_12500    12500   //12.5MHz
#define BAUD_6250      6250   //6.25MHz
#define BAUD_4200      4200   //4.166MHz
#define BAUD_2000      2000   //2.083MHz
#define BAUD_1000      1000   //1.042Mhz
#define BAUD_500        500   //520KHz
#define BAUD_300        300   //312KHz
#define BAUD_100        100   //97KHz
#define BAUD_50          50   //49KHz
#define BAUD_12          12   //12.2KHz

struct spi_baudrate 
{
  uint16 baud_value;
  uint8 baud_register;
};
   
/*constant containing baudrate variables for SPI controller*/
const static struct spi_baudrate spi_array[] =
{
  {BAUD_12500,0x00},
  { BAUD_6250,0x10},
  { BAUD_4200,0x20},
  { BAUD_2000,0x50},
  { BAUD_1000,0x51},
  {  BAUD_500,0x52},
  {  BAUD_300,0x43},
  {  BAUD_100,0x35},
  {   BAUD_50,0x17},
  {   BAUD_12,0x77},
};

#define SPI_BAUD_ARRAY_LENGTH sizeof(spi_array)/sizeof(spi_array[0])

typedef void(*SPI_CallbackType)(char);

/********************************************************************/

/**
 * Start SCI controller in UART mode
 * @param port number  
 * @param baud
 * @param polarity
 * @param phase
 * @param master or slave
 * @return none
 */
void 
spi_init(uint8 port, uint16 baud, uint8 polarity, uint8 phase, uint8 master_slave_selector);

/**
 * Assign SPI callback function to ISR
 * @param port number  
 * @param callback function
 * @return none
 */
void 
spi_assign_call_back(uint8 number, void (*func)(char));

/**
 * Enable SPI chip select
 * @param port number
 * @return none
 */
void
spi_enable_chip_select(uint8 channel);

/**
 * Disable SPI chip select
 * @param port number
 * @return none
 */
void
spi_disable_chip_select(uint8 channel);

/**
 * SPI set baudrate
 * @param port number
 * @param selected baudrate
 * @return zero for OK, one for error
 */
uint8 
spi_set_baudrate(uint8 channel, uint16 baud);

/**
 * SPI get baudrate
 * @param port number
 * @return assigned baudrate, zero if not was on baudrate list
 */
uint16
spi_get_baudrate(uint8 channel);

/**
 * Get a character from SPI HW buffer without waiting
 * @param port number
 * @return read character
 */
int8 
spi_getchar (uint8 channel);

/**
 * Put a character to SPI HW buffer without waiting
 * @param port number
 * @param character to send
 * @return none
 */
void 
spi_putchar (uint8 channel, uint8 ch);

/********************************************************************/

/**
 * Check if Tx buffer has a character
 * @param port number
 * @return zero if empty, one if there's something
 */
uint8
spi_is_tx_buffer_empty(uint8 channel);

/**
 * Check if Rx buffer has a character
 * @param port number
 * @return zero if empty, one if there's something
 */
uint8
spi_is_rx_buffer_full(uint8 channel);

/********************************************************************/

/**
 * Enable SPI Tx Interrupt
 * @param port number
 * @return none
 */
void 
spi_enable_tx_interrupt (uint8 channel);

/**
 * Disable SPI Tx Interrupt
 * @param port number
 * @return none
 */
void 
spi_disable_tx_interrupt (uint8 channel);

/********************************************************************/

/**
 * Enable SPI Rx Interrupt
 * @param port number
 * @return none
 */
void 
spi_enable_rx_interrupt (uint8 channel);

/**
 * Disable SPI Rx Interrupt
 * @param port number
 * @return none
 */
void 
spi_disable_rx_interrupt (uint8 channel);

/**
 * SPI Send-Receive function
 * @param port number
 * @param character to xmit
 * @param received character
 * @return none
 */
void 
spi_send_receive_waiting(uint8 channel, uint8 pcTxedChar,uint8 *pcRxedChar);

/***************  ISRs for RTOS **************/
/**
 * SPI1 ISR
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vspi1 
spi1_irq( void );

/**
 * SPI2 ISR
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vspi2 
spi2_irq( void );

#endif /* __SPI_H__ */