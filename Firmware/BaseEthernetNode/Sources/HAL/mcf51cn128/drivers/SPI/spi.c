/*
 * File:
 *
 * Notes:       
 *              
 */
#include "cf_board.h"
#include "spi.h"
#include "gpio.h"

//global variable containing callbacks for SPI:
static SPI_CallbackType spi_callback[NUMBER_OF_SPIs];

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
spi_init(uint8 port, uint16 baud, uint8 polarity, uint8 phase, uint8 master_slave_selector) 
{
	/*
	 * Initialize all three UARTs for serial communications
	 */
	DEMO_SELECTOR_OFF;/*startup line for reference design*/
	   
  switch(port)
  {
    case SPI1_PORT:
      //Enable pins:
      
      /*SPI function*/      
      SPI1_MOSI_MISO_CLK_INIT;

      /*starting SPI clock*/
      SCGC2_SPI1 = 1;

      /*master-slave SPI*/
      if(master_slave_selector)
      {
         SPI1C1_MSTR = 1;//master
         SPI1_SS_GPIO_INIT;
      }
      else
      {
         SPI1C1_MSTR = 0;//slave
         SPI1_SS_INIT;
      }

    	/*baudrate and SPI baudrate*/
    	spi_set_baudrate(SPI1_PORT,baud);
    	
    	/*polarity*/
    	if(polarity)
    	{
    	  SPI1C1_CPOL = 1;
    	}
    	else
    	{
    	  SPI1C1_CPOL = 0;
    	}
    	    	 
    	/*phase*/
    	if(phase)
    	{
    	  SPI1C1_CPHA = 1;
    	}
    	else
    	{
    	  SPI1C1_CPHA = 0;
    	}

    	break;
    case SPI2_PORT:
      //Enable pins:
            
      /*SPI function*/      
      SPI2_MOSI_MISO_CLK_INIT;

      /*starting SPI clock*/
      SCGC2_SPI2 = 1;
 
       /*master-slave SPI*/
      if(master_slave_selector)
      {
         SPI2C1_MSTR = 1;//master
         SPI2_SS_GPIO_INIT;         
      }
      else
      {
         SPI2C1_MSTR = 0;//slave
         SPI2_SS_INIT;
      }

    	/*baudrate & start SPI controller*/
    	spi_set_baudrate(SPI2_PORT,baud);  

    	/*polarity*/
    	if(polarity)
    	{
    	  SPI2C1_CPOL = 1;
    	}
    	else
    	{
    	  SPI2C1_CPOL = 0;
    	}
    	    	 
    	/*phase*/
    	if(phase)
    	{
    	  SPI2C1_CPHA = 1;
    	}
    	else
    	{
    	  SPI2C1_CPHA = 0;
    	}
    	         
      break;
  }
}

/**
 * Assign SPI callback function to ISR
 * @param port number  
 * @param callback function
 * @return none
 */
void 
spi_assign_call_back(uint8 number, void (*func)(char))
{
    spi_callback[number] = func;
}

/**
 * Enable SPI chip select
 * @param port number
 * @return none
 */
void
spi_enable_chip_select(uint8 channel) 
{
 switch(channel)
 {
    case SPI1_PORT:
       SPI1_SS_GPIO = 0;
       break;
    case SPI2_PORT:
       SPI2_SS_GPIO = 0;
       break; 
 }  
}

/**
 * Disable SPI chip select
 * @param port number
 * @return none
 */
void
spi_disable_chip_select(uint8 channel) 
{
 switch(channel)
 {
    case SPI1_PORT:
       SPI1_SS_GPIO = 1;
       break;
    case SPI2_PORT:
       SPI2_SS_GPIO = 1;
       break; 
 }  
}

/**
 * SPI set baudrate
 * @param port number
 * @param selected baudrate
 * @return zero for OK, one for error
 */
uint8 
spi_set_baudrate(uint8 channel, uint16 baud)
{
  uint8 i;
  /*
   * Assing baudrate: if not found, will be previous value or default :-S
   */  
  for(i=0;i<SPI_BAUD_ARRAY_LENGTH;i++)
  {
     if(baud == spi_array[i].baud_value)
     {
       switch(channel)
       {
          case SPI1_PORT:
             SPI1C1_SPE = 0;
             SPI1BR = (uint8)spi_array[i].baud_register;
             SPI1C1_SPE = 1;
             return 0;
             break;
          case SPI2_PORT:
             SPI2C1_SPE = 0;
             SPI2BR = (uint8)spi_array[i].baud_register;
             SPI2C1_SPE = 1;
             return 0;
             break; 
       }    	   
     }
  }
  return 1;
}

/**
 * SPI get baudrate
 * @param port number
 * @return assigned baudrate, zero if not was on baudrate list
 */
uint16
spi_get_baudrate(uint8 channel)
{
  uint16 get_baud;
  uint8 i;
  
  switch(channel)
  {
    case SPI1_PORT:
       get_baud = SPI1BR;
       break;
    case SPI2_PORT:
       get_baud = SPI2BR;
       break; 
  }  
  
  /*
   * Assing baudrate: if not found return 0 :-S
   */  
  for(i=0;i<SPI_BAUD_ARRAY_LENGTH;i++)
  {
     if(get_baud == spi_array[i].baud_register)
     {
       return spi_array[i].baud_value;    	   
     }
  }
  
  return 0;
  
}

/**
 * Get a character from SPI HW buffer without waiting
 * @param port number
 * @return read character
 */
int8 
spi_getchar (uint8 channel)
{
 switch(channel)
 {
    case SPI1_PORT:
       return SPI1D;
       break;
    case SPI2_PORT:
       return SPI2D;
       break; 
 }
}

/**
 * Put a character to SPI HW buffer without waiting
 * @param port number
 * @param character to send
 * @return none
 */
void 
spi_putchar (uint8 channel, uint8 ch)
{    
 switch(channel)
 {
    case SPI1_PORT: 
       SPI1D = (uint8)ch;               /* Send a character by SCI */
       break;
    case SPI2_PORT:
       SPI2D = (uint8)ch;               /* Send a character by SCI */
       break;  
 }    
}

/********************************************************************/

/**
 * Check if Tx buffer has a character
 * @param port number
 * @return zero if empty, one if there's something
 */
uint8
spi_is_tx_buffer_empty(uint8 channel)
{
 switch(channel)
 {
    case SPI1_PORT: 
       return (SPI1S_SPTEF/* && SPI1C1_SPIE*/);
       break;
    case SPI2_PORT:
       return (SPI2S_SPTEF/* && SPI2C1_SPIE*/);
       break;  
 }  
}

/**
 * Check if Rx buffer has a character
 * @param port number
 * @return zero if empty, one if there's something
 */
uint8
spi_is_rx_buffer_full(uint8 channel)
{
 switch(channel)
 {
    case SPI1_PORT: 
       return (SPI1S_SPRF);
       break;
    case SPI2_PORT:
       return (SPI2S_SPRF);
       break;  
 }  
}

/********************************************************************/

/**
 * Enable SPI Tx Interrupt
 * @param port number
 * @return none
 */
void 
spi_enable_tx_interrupt (uint8 channel)
{    
 switch(channel)
 {
    case SPI1_PORT:
       SPI1C1_SPTIE = 1;
       break;
    case SPI2_PORT:
       SPI2C1_SPTIE = 1;
       break; 
 } 
}

/**
 * Disable SPI Tx Interrupt
 * @param port number
 * @return none
 */
void 
spi_disable_tx_interrupt (uint8 channel)
{
 switch(channel)
 {
    case SPI1_PORT:
       SPI1C1_SPTIE = 0;
       break;
    case SPI2_PORT:
       SPI2C1_SPTIE = 0;
       break; 
 } 
}

/********************************************************************/

/**
 * Enable SPI Rx Interrupt
 * @param port number
 * @return none
 */
void 
spi_enable_rx_interrupt (uint8 channel)
{    
 switch(channel)
 {
    case SPI1_PORT:
       SPI1C1_SPIE = 1;
       break;
    case SPI2_PORT:
       SPI2C1_SPIE = 1;
       break; 
 } 
}

/**
 * Disable SPI Rx Interrupt
 * @param port number
 * @return none
 */
void 
spi_disable_rx_interrupt (uint8 channel)
{    
 switch(channel)
 {
    case SPI1_PORT:
       SPI1C1_SPIE = 0;
       break;
    case SPI2_PORT:
       SPI2C1_SPIE = 0;
       break; 
 }  
}

/**
 * SPI Send-Receive function
 * @param port number
 * @param character to xmit
 * @param received character
 * @return none
 */
void 
spi_send_receive_waiting(uint8 channel, uint8 pcTxedChar,uint8 *pcRxedChar)
{
 switch(channel)
 {
    case SPI1_PORT:
	     while(!SPI1S_SPTEF)
	     ;
	     (void)SPI1S;
 	     SPI1D=pcTxedChar;
	     while(!SPI1S_SPRF)
	     ;
	     *pcRxedChar = SPI1D;
       break; 
    case SPI2_PORT:
	     while(!SPI2S_SPTEF)
	     ;
	     (void)SPI2S;
 	     SPI2D=pcTxedChar;
	     while(!SPI2S_SPRF)
	     ;
	     *pcRxedChar = SPI2D;
       break; 
 }
  
}
 

/***************  ISRs for RTOS **************/
/**
 * SPI1 ISR
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vspi1 
spi1_irq( void )
{
    /* This ISR can cause a context switch, so the first statement must be
     * a call to the portENTER_SWITCHING_ISR() macro.
     */
    spi_callback[SPI1_PORT](SPI1_PORT);
}

/**
 * SPI2 ISR
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vspi2 
spi2_irq( void )
{
    /* This ISR can cause a context switch, so the first statement must be
     * a call to the portENTER_SWITCHING_ISR() macro.
     */
    spi_callback[SPI2_PORT](SPI2_PORT);
}