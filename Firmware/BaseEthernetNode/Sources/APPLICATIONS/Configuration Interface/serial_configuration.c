/*
 * COnfigurate selected serial interface
 */

/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

/* ------------------------ lwIP includes --------------------------------- */
#include "tcp.h"

/* ------------------------ Project includes ------------------------------ */
#include "uart_rtos.h"
#include "spi_rtos.h"
#include "serial_configuration.h"
#include "setget.h"
#include "mcu_init.h"

/*uart/spi/iic selector*/
static uint8 serial_interface;

/*Handle for UART capabilities*/
xComPortHandle UARTConfigHandle;

/*Semaphore to wake up task: comes from uart_rtos.c*/
extern xSemaphoreHandle xUARTSemaphore;

/*Handle for SPI capabilities*/
xSPIPortHandle SPIConfigHandle;   

/*FSL: function arrays for set/get parameters*/
extern SIX_BYTES six_bytes_array[];
extern FOUR_BYTES four_bytes_array[];
extern TWO_BYTES two_bytes_array[];
extern ONE_BYTE one_byte_array[];

/*****************************Functions***************************************/

/**
 * Get a Character from default serial interface
 *
 * @param none
 * @return received character
 */
static int8
SerialGetChar(void)
{
    int8 rx_character;
    
    switch( serial_interface )
    {
      case SCI_MODE:
       /*Block task until UART first character arrives*/
       xSemaphoreTake( xUARTSemaphore, portMAX_DELAY );
       xUARTGetCharWithFlowControl(UARTConfigHandle,&rx_character);
       break;
      case SPI_MODE:
       xSPISlaveReceiveChar(SPIConfigHandle,&rx_character,portMAX_DELAY);
       break;
      
      case IIC_MODE:
      
       break;
    }
    
    return rx_character;  
}

/**
 * Character to transmit to default serial interface
 *
 * @param char to transmit 
 * @return none
 */
static void 
SerialSetChar(int8 xmit_character)
{        
    switch( serial_interface )
    {
      case SCI_MODE:
       xUARTPutChar(UARTConfigHandle, xmit_character, portMAX_DELAY);
       break;
      case SPI_MODE:
       /*if buffer full, character is dropped*/
       xSPISlaveSendChar(SPIConfigHandle,xmit_character,0);
       break;
      
      case IIC_MODE:
      
       break;
    }  
}

/**
 * Number of bytes to send from 4-byte length variable
 *
 * @param 4-byte length variable containing data for serial interface
 * @param number of bytes from 4-byte length variable
 * @return none
 */
static void
set_command_pamameter_four_bytes(uint32 number,int8 bytes)
{
  T32_8 var;
  uint8 i;
  
  var.lword = number;
  
  for(i=0;i<bytes;i++)
  {
    SerialSetChar(var.bytes[i]);//n-th write: parameters
  }  
}

/**
 * Number of bytes to receive from serial interface to a 4-byte length variable
 *
 * @param number of bytes from 4-byte length variable
 * @return 4-byte length variable containing data for serial interface
 */
static uint32 
get_command_parameter_four_bytes(int8 bytes)
{
  T32_8 var;
  uint8 i;
  
  for(i=0;i<bytes;i++)
  {
    var.bytes[i] = SerialGetChar();//n-th read: parameters
  }
  
  return var.lword;
}

/**
 * Number of bytes to send from nth-byte length variable
 *
 * @param nth-byte length variable containing data for serial interface
 * @param number of bytes from nth-byte length variable
 * @return none
 */
static void
set_command_parameter_nth_bytes(uint8 *var, int8 bytes)
{
  uint8 i;
  
  for(i=0;i<bytes;i++)
  {
     SerialSetChar(var[i]);//n-th write: parameters
  }  
}

/**
 * Number of bytes to receive from serial interface to a nth-byte length variable
 *
 * @param number of bytes from nth-byte length variable
 * @param nth-byte length variable containing data rx from serial interface
 * @return none
 */
static void 
get_command_parameters_nth_bytes(uint8 *var, int8 bytes)
{
  uint8 i;
  
  for(i=0;i<bytes;i++)
  {
     var[i] = SerialGetChar();//n-th read: parameters
  }
}                                                      

/**
 * Serial Parser to get command to execute 
 *
 * @param none 
 * @return none
 */
static void
SerialParser(void)
{
    /*variable holding reads*/
    int8 ch, func;    
    
    /*variable holding six bytes parameter*/
    uint8 six_parameter[6];
    
    do
    {
       ch = SerialGetChar();//1st read: command
    }/*FSL: stay here until receive a valid command*/
    while( (ch != SERIAL_CMD_GET) && (ch != SERIAL_CMD_SET) && (ch != SERIAL_CMD_RST) );

    ch = SerialGetChar();//2nd read: number of parameters

    /*start sending number of bytes to send*/
    if( (ch == ONE_PARAMETER) || (ch == TWO_PARAMETER) || (ch == FOUR_PARAMETER) || (ch == SIX_PARAMETER) )
    {
       SerialSetChar(ch);
    }
    else
    {
       /*error condition*/
       SerialSetChar(0xFF);
       return;/*exit*/
    }
    func = SerialGetChar();//3rd read: function
    
    switch(ch)
    {
      case SERIAL_CMD_GET:        
        /*FSL: run the get command*/
        switch(ch)
        {
          case ONE_PARAMETER:
            if(!(get_one_byte_elements()>func)){goto wrong_read;}
            set_command_pamameter_four_bytes((uint8)one_byte_array[func].get(),ONE_PARAMETER);
            break;
          case TWO_PARAMETER:
            if(!(get_two_bytes_elements()>func)){goto wrong_read;}
            set_command_pamameter_four_bytes((uint16)two_bytes_array[func].get(),TWO_PARAMETER);
            break;
          case FOUR_PARAMETER:
            if(!(get_four_bytes_elements()>func)){goto wrong_read;}
            set_command_pamameter_four_bytes((uint32)four_bytes_array[func].get(),FOUR_PARAMETER);
            break;
          case SIX_PARAMETER:
            if(!(get_six_bytes_elements()>func)){goto wrong_read;}
            six_bytes_array[func].get(&six_parameter[0]);
            set_command_parameter_nth_bytes(&six_parameter[0],SIX_PARAMETER);
          default:
          wrong_read:
            /*error condition*/
            SerialSetChar(0xFF);
            return;
            //break;
        }
        break;
      case SERIAL_CMD_SET:      
        /*FSL: run the set command*/
        switch(ch)
        {
          case ONE_PARAMETER:
            if(!(get_one_byte_elements()>func)){goto wrong_write;}            
            one_byte_array[func].set((uint8)get_command_parameter_four_bytes(ONE_PARAMETER));            
            break;
          case TWO_PARAMETER:
            if(!(get_two_bytes_elements()>func)){goto wrong_write;}            
            two_bytes_array[func].set((uint16)get_command_parameter_four_bytes(TWO_PARAMETER));
            break;
          case FOUR_PARAMETER:
            if(!(get_four_bytes_elements()>func)){goto wrong_write;}            
            four_bytes_array[func].set((uint32)get_command_parameter_four_bytes(FOUR_PARAMETER));
            break;
          case SIX_PARAMETER:            
            if(!(get_six_bytes_elements()>func)){goto wrong_write;}            
            get_command_parameters_nth_bytes(&six_parameter[0],SIX_PARAMETER);
            six_bytes_array[func].set( &six_parameter[0] );
          default:
          wrong_write:
            /*error condition*/
            SerialSetChar(0xFF);
            return;
            //break;
        }      
      
        /*send ACK: OK*/
        SerialSetChar(0x00);
        break;
      case SERIAL_CMD_RST:        
        /*send ACK: OK*/
        SerialSetChar(0x00);
        
        /*reset the uC*/
        MCU_reset();
      default:  
        break;
    }
    
    return;
}

/**
 * Serial Configuration Task
 *
 * @param none 
 * @return none
 */
void
vSerialBridgeConfiguration( void *pvParameters )
{    
    /* Parameters are not used - suppress compiler error */
    ( void )pvParameters;

    /**********************FSL: serial start-up*******************************/
    
    /*get default configuration mode*/
    serial_interface = board_get_bridge_tcp_mode();
    
    /*FSL: init selected interface*/
    switch( serial_interface )
    {
      case SCI_MODE:
        /*FSL: create semaphore that will allow to sleep process*/
        vSemaphoreCreateBinary(xUARTSemaphore);
        /*Block task until UART first character arrives*/
        xSemaphoreTake( xUARTSemaphore, portMAX_DELAY );
        
        //if handle is NULL, serial cannot be used!!!
        UARTConfigHandle = xUARTinit((eCOMPort)board_get_uart_port()/*serCOM1*/, 
                                 (eBaud)board_get_uart_baud()/*ser19200*/, 
                                 (eParity)board_get_uart_parity()/*serNO_PARITY*/, 
                                 (eDataBits)board_get_uart_number_of_bits()/*serBITS_8*/, 
                                 (eStopBits)board_get_uart_stop_bits()/*serSTOP_1*/,
                                 (eFlowControl)board_get_uart_flow_control()/*serFlowControlXONXOFF*/,
                                 (eCOMsemaphore)serSemaphoreON,/*Turn on semaphore ON activity*/  
                                 SERIAL_BUFFER_LIMIT/*defined at header file*/);
        if( UARTConfigHandle == NULL )                         
        {
          /*delete task*/
          vTaskDelete(NULL);
        }
       break;
      case SPI_MODE:
        /**********************FSL: spi start-up*******************************/
        //if handle is NULL, serial cannot be used!!!
        SPIConfigHandle = xSPIinit((eSPIPort)board_get_spi_port()/*serSPI2*/, 
                                 (spiBaud)board_get_spi_baud()/*ser1000*/, 
                                 (spiPolarity)board_get_spi_polarity()/*serIDLEslow*/, 
                                 (spiPhase)board_get_spi_phase()/*serMiddleSample*/, 
                                 serSlave/*must be in slave mode during configuration*/,
                                 (spiInterrupt)board_get_spi_interrupt()/*serPolling*/,  
                                 SERIAL_BUFFER_LIMIT/*defined at header file*/);
        if( SPIConfigHandle == NULL )
        {
          /*delete task*/
          vTaskDelete(NULL);
        }
       break;
      
      case IIC_MODE:
      
       break;
    }

    /* Loop forever */
    for( ;; )
    {	       
       /*check for available data for configuration*/
       SerialParser();
    }
    return;/*FSL:never get here!!*/
}