/*
 * File:        uart.h
 *
 * Notes:       
 *              
 */

#ifndef __UART_H__
#define __UART_H__

/*SCI ports*/
#define SCI1_PORT              0
#define SCI2_PORT              1
#define SCI3_PORT              2

#define SCI_TX                 1
#define SCI_RX                 0

#define NUMBER_OF_SCIs         3

#if 0
#define BAUDRATE_110           ((SYSTEM_CLOCK)/(110 * 32))
#define BAUDRATE_134           ((SYSTEM_CLOCK)/(134 * 32))
#define BAUDRATE_150           ((SYSTEM_CLOCK)/(150 * 32))
#define BAUDRATE_200           ((SYSTEM_CLOCK)/(200 * 32))
#define BAUDRATE_300           ((SYSTEM_CLOCK)/(300 * 32))
#define BAUDRATE_600           ((SYSTEM_CLOCK)/(600 * 32))
#define BAUDRATE_1200          ((SYSTEM_CLOCK)/(1200 * 32))
#define BAUDRATE_1800          ((SYSTEM_CLOCK)/(1800 * 32))
#define BAUDRATE_2400          ((SYSTEM_CLOCK)/(2400 * 32))
#define BAUDRATE_4800          ((SYSTEM_CLOCK)/(4800 * 32))
#define BAUDRATE_9600          ((SYSTEM_CLOCK)/(9600 * 32))
#define BAUDRATE_19200         ((SYSTEM_CLOCK)/(19200 * 32))
#define BAUDRATE_38400         ((SYSTEM_CLOCK)/(38400 * 32))
#define BAUDRATE_57600         ((SYSTEM_CLOCK)/(57600 * 32))
#define BAUDRATE_115200        ((SYSTEM_CLOCK)/(115200 * 32))
#endif

/*FSL:software flow control*/
#define UART_XON               0x11
#define UART_XOFF              0x13

#define FLOW_CONTROL_NONE      0
#define FLOW_CONTROL_HARDWARE  1
#define FLOW_CONTROL_SOFTWARE  2

typedef void(*SCI_CallbackType)(CHAR);

/********************************************************************/

/**
 * Start SCI controller in UART mode
 * @param port number  
 * @param baudrate
 * @param parity
 * @param number of bits
 * @param number of stop bits
 * @param flow control: hw, sw or none 
 * @return none
 */
void 
uart_init(uint8 port, uint32 baud, uint8 parity, uint8 bits, uint8 stop_bit, uint8 flow_control);

/**
 * Assign ISR Callback
 * @param port number  
 * @param callback function
 * @return none
 */
void 
uart_assign_call_back(uint8 number, void (*func)(CHAR));

/**
 * Get character in while mode with timeout support
 * @param port number  
 * @param returned character
 * @return zero for OK, 1 for timeout return
 */
uint8 
uart_getchar_wait (uint8 channel, int8 *character);

/**
 * Get character directly from HW buffer without waiting
 * @param port number  
 * @return returned character
 */
int8 
uart_getchar (uint8 channel);

/**
 * Put a character directly to HW buffer without waiting
 * @param port number
 * @param character to send   
 * @return none
 */ 
void 
uart_putchar (uint8 channel, CHAR ch);

/********************************************************************/

/**
 * Enable SCI TX interrupts
 * @param port number   
 * @return none
 */ 
void 
uart_enable_tx_interrupt (uint8 channel);

/**
 * Disable SCI TX interrupts
 * @param port number   
 * @return none
 */ 
void 
uart_disable_tx_interrupt (uint8 channel);

/********************************************************************/

/**
 * Enable SCI RX interrupts
 * @param port number   
 * @return none
 */
void 
uart_enable_rx_interrupt (uint8 channel);

/**
 * Disable SCI RX interrupts
 * @param port number   
 * @return none
 */
void 
uart_disable_rx_interrupt (uint8 channel);

/*********************************************************************/

/**
 * Get CTS signal state
 * @param port number   
 * @return none
 */
uint8
uart_get_CTS_state(uint8 port);

/**
 * Send stop signal (XOFF or RTS) to stop communication
 * @param port number
 * @param flow control: hw or sw 
 * @return none
 */
void
uart_send_tx_stop(uint8 port, uint8 flow_control);

/**
 * Send go signal (XON or RTS) to start communication
 * @param port number
 * @param flow control: hw or sw 
 * @return none
 */
void
uart_send_tx_go(uint8 port, uint8 flow_control);

/*********************************************************************/

#if 0

/**
 * SCI1 ISR Error Processing
 * @param none
 * @return none
 */
static void 
sci_error1_processing(void);
/**
 * SCI2 ISR Error Processing
 * @param none
 * @return none
 */
static void 
sci_error2_processing(void);

/**
 * SCI3 ISR Error Processing
 * @param none
 * @return none
 */
static void 
sci_error3_processing(void);

#endif

/***************  ISRs for RTOS **************/

/**
 * SCI1 ISR TX
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci1tx 
uart1_tx_irq( void );

/**
 * SCI2 ISR TX
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci2tx 
uart2_tx_irq( void );

/**
 * SCI3 ISR TX
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci3tx 
uart3_tx_irq( void );

/***************************** RX ************************************/
/**
 * SCI1 ISR RX
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci1rx
uart1_rx_irq( void );

/**
 * SCI2 ISR RX
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci2rx
uart2_rx_irq( void );

/**
 * SCI3 ISR RX
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci3rx 
uart3_rx_irq( void );

#if 0

/***************************** Error *********************************/
/**
 * SCI1 ISR Error
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci1err 
uart1_error_irq( void );

/**
 * SCI2 ISR Error
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci2err 
uart2_error_irq( void );

/**
 * SCI3 ISR Error
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci3err 
uart3_error_irq( void );
#endif

#endif