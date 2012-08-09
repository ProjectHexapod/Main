#ifndef _SERIAL_BRIGDE_H_
#define _SERIAL_BRIGDE_H_

#define SCI_MODE          0
#define SPI_MODE          1
#define IIC_MODE          2

#define SERIAL_BUFFER_LIMIT       16

/**/
#define SERIAL_CMD_GET    0x50// '1'
#define SERIAL_CMD_SET    0xA0// '2'
#define SERIAL_CMD_RST    0x88// '3'

/**/
#define ONE_PARAMETER     1
#define TWO_PARAMETER     2
#define FOUR_PARAMETER    4
#define SIX_PARAMETER     6


#define SERIAL_BRIDGE_TASK_PRIORITY      ( tskIDLE_PRIORITY + 2 )

/*Prototypes*/

/**
 * Get a Character from default serial interface
 *
 * @param none
 * @return received character
 */
static int8
SerialGetChar(void);

/**
 * Character to transmit to default serial interface
 *
 * @param char to transmit 
 * @return none
 */
static void 
SerialSetChar(int8 xmit_character);

/**
 * Number of bytes to send from 4-byte length variable
 *
 * @param 4-byte length variable containing data for serial interface
 * @param number of bytes from 4-byte length variable
 * @return none
 */
static void
set_command_pamameter_four_bytes(uint32 number,int8 bytes);

/**
 * Number of bytes to receive from serial interface to a 4-byte length variable
 *
 * @param number of bytes from 4-byte length variable
 * @return 4-byte length variable containing data for serial interface
 */
static uint32 
get_command_parameter_four_bytes(int8 bytes);

/**
 * Number of bytes to send from nth-byte length variable
 *
 * @param nth-byte length variable containing data for serial interface
 * @param number of bytes from nth-byte length variable
 * @return none
 */
static void
set_command_parameter_nth_bytes(uint8 *var, int8 bytes);

/**
 * Number of bytes to receive from serial interface to a nth-byte length variable
 *
 * @param number of bytes from nth-byte length variable
 * @param nth-byte length variable containing data rx from serial interface
 * @return none
 */
static void 
get_command_parameters_nth_bytes(uint8 *var, int8 bytes);                                                      

/**
 * Serial Parser to get command to execute 
 *
 * @param none 
 * @return none
 */
static void
SerialParser(void);

/**
 * Serial Configuration Task
 *
 * @param none 
 * @return none
 */
void
vSerialBridgeConfiguration( void *pvParameters );

#endif