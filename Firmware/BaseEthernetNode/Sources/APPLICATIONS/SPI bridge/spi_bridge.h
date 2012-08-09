#ifndef _SPI_BRIGDE_H_
#define _SPI_BRIGDE_H_

#define SPI_BRIDGE_BUFFER_LIMIT       16/*HIL driver buffer length when using interrupts*/

#define SPI_BRIDGE_TASK_PRIORITY      ( tskIDLE_PRIORITY + 3 )

/**
 * Callback function called when an error is detected on connection
 *
 * @param bridge information
 * @param error information
 * @return none
 */
void 
BRIDGE_SPI_ETH_ERROR(void *arg, err_t err);

/**
 * Callback function called when a packet has been sent thru Ethernet
 *  Send more information as soon as last packet has been received by the other side
 *
 * @param bridge information
 * @param tcp connection descriptor
 * @param sent data length
 * @return error type on callback to be processed by lwIP
 */
err_t 
BRIDGE_SPI_ETH_SEND_CALLBACK(void *arg, struct tcp_pcb *pcb, u16_t len);

/**
 * Callback function called when Server (THIS) receives a valid connection from a client
 *  or a server connects to this client in CLIENT mode
 *
 * @param argument sent by lwIP
 * @param tcp connection descriptor
 * @param reception error flag
 * @return error type on callback to be processed by lwIP
 */
static err_t
BRIDGE_SPI_Accept(void *arg, struct tcp_pcb *pcb, err_t err);

/*****************************************************************************/

/**
 * Callback function called from lwIP when data is received from Ethernet
 *
 * @param bridge actual information
 * @param tcp connection descriptor
 * @param received network buffer
 * @param reception error flag
 * @return error type on callback to be processed by lwIP
 */
static err_t
BRIDGE_SPI_ETH_RX(void *arg, struct tcp_pcb *pcb, struct pbuf *p, err_t err);

/**
 * Send to Ethernet as soon as there are available characters on SPI queue
 *
 * @param none  
 * @return zero if everything's fine, otherwise 1
 */
static err_t 
BRIDGE_SPI_ETH_TX( void );

/**
 * Ethernet to SPI task
 *
 * @param none  
 * @return none
 */
void
BRIDGE_SPI_Task( void *pvParameters );

#endif