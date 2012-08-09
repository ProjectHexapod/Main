/*
 * A simple server/client socket interfacing the tcp/ip stack directly:
 * b06862
 *
 * Features:
 *   session is not closed until client does it first: TODO: automatic close
 *   SERIAL side sends if: at least a character is ready AND a 1/2 second has occurred.
 *   default serial working at 115.2Kbps 8-N-1
 *   tcp packet length sent from the client only depends on client
 *   serial buffers lengths were selected according to performance and limits in memory
 *   SW and HW flow control implemented to avoid dropping a character
 *   None flow control will drop characters if internal queue is full
 */

/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

/* ------------------------ lwIP includes --------------------------------- */
#include "tcp.h"

/* ------------------------ Project includes ------------------------------ */
#include "uart_bridge.h"
#include "uart_rtos.h"
#include "setget.h"

/*****************************************************************************/

/*MAC Data descriptor to be sent*/
struct bridge_state 
{
  s8_t *data;
  u32_t left;
  u8_t retries;
};

/*MAC buffer descriptor*/
struct uart_tx_state
{
  struct tcp_pcb *tx_pcb;
  struct bridge_state *p_bridge_state;
};

/*FSL: variable holding usefull UART/MAC information*/
struct uart_tx_state p_uart_tx_state;

/*Handle for UART capabilities*/
xComPortHandle UARThandle;

/*Mutex to MAC buffers*/
xSemaphoreHandle UARTmutex;

/*Semaphore to wake up task: comes from uart_rtos.c*/
extern xSemaphoreHandle xUARTSemaphore;

/*****************************Prototypes**************************************/

/**
 * Function called when a connection needs to be closed
 *  Close all connection callbacks
 *
 * @param tcp connection descriptor
 * @param bridge information
 * @return none
 */
static void
BRIDGE_UART_ETH_CLOSE(struct tcp_pcb *pcb, struct bridge_state *hs);

/**
 * Function called when a packet needs to be sent thru Ethernet
 *  Automatically split packet lenght to fit on packet max size
 *
 * @param tcp connection descriptor
 * @param bridge information
 * @return none
 */
static void
BRIDGE_UART_ETH_SEND(struct tcp_pcb *pcb, struct bridge_state *hs);

/*****************************Functions***************************************/

/**
 * Function called when a connection needs to be closed
 *  Close all connection callbacks
 *
 * @param tcp connection descriptor
 * @param bridge information
 * @return none
 */
static void
BRIDGE_UART_ETH_CLOSE(struct tcp_pcb *pcb, struct bridge_state *hs)
{
  tcp_arg(pcb, NULL);
  tcp_sent(pcb, NULL);
  tcp_recv(pcb, NULL);
  mem_free(hs);
  tcp_close(pcb);
}

/**
 * Function called when a packet needs to be sent thru Ethernet
 *  Automatically split packet lenght to fit on packet max size
 *
 * @param tcp connection descriptor
 * @param bridge information
 * @return none
 */
static void
BRIDGE_UART_ETH_SEND(struct tcp_pcb *pcb, struct bridge_state *hs)
{
  err_t err;
  u16_t len;

  /* We cannot send more data than space available in the send buffer */
  if (tcp_sndbuf(pcb) < hs->left) 
  {
    len = tcp_sndbuf(pcb);
  } 
  else 
  {
    len = hs->left;
  }

  do {
    err = tcp_write(pcb, hs->data, len, TCP_WRITE_FLAG_COPY);
    if (err == ERR_MEM) 
    {
      len /= 2;
    }
  } while (err == ERR_MEM && len > 1);

  if (err == ERR_OK) 
  {
    hs->data += len;
    hs->left -= len;
    /*send it right now for performance*/
    tcp_output(pcb);   
  }
}

/**
 * Callback function called when an error is detected on connection
 *
 * @param bridge information
 * @param error information
 * @return none
 */
void 
BRIDGE_UART_ETH_ERROR(void *arg, err_t err)
{
  struct bridge_state *hs;

  hs = arg;
  mem_free(hs);
}

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
BRIDGE_UART_ETH_SEND_CALLBACK(void *arg, struct tcp_pcb *pcb, u16_t len)
{
  struct bridge_state *hs;

  hs = arg;
  
  if (hs->left > 0) 
  {
    BRIDGE_UART_ETH_SEND(pcb, hs);
  } 
  else 
  {
    /*FSL: tcp transaction is over: release simple internal flag*/
    xSemaphoreGive(UARTmutex);
    
    tcp_sent(pcb, NULL);    
  }

  return ERR_OK;
}

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
BRIDGE_UART_Accept(void *arg, struct tcp_pcb *pcb, err_t err)
{
  struct bridge_state *hs;
  
  /* Allocate memory for the structure that holds the state of the connection */
  hs = mem_malloc(sizeof(struct bridge_state));  

  if (hs == NULL) 
  {
    return ERR_MEM;
  }

  /* Initialize the structure. */
  hs->data = NULL;
  hs->left = 0;
  hs->retries = 0;

  /*uart structure*/
  p_uart_tx_state.tx_pcb = pcb;
  p_uart_tx_state.p_bridge_state = hs;

  /* Tell TCP that this is the structure we wish to be passed for our callbacks */
  tcp_arg(pcb, hs);

  /*called function when RX*/
  tcp_recv(pcb, BRIDGE_UART_ETH_RX);

  tcp_err(pcb, BRIDGE_UART_ETH_ERROR);

  tcp_setprio(pcb,TCP_PRIO_MAX);
  
  return ERR_OK;
}

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
BRIDGE_UART_ETH_RX(void *arg, struct tcp_pcb *pcb, struct pbuf *p, err_t err)
{
    struct bridge_state *hs;
    CHAR *rq;
    uint16 length;
    struct pbuf *q; 

    hs = arg;
    
    /* If we got a NULL pbuf in p, the remote end has closed the connection. */
    if(p != NULL) 
    {                
        /*FSL:send as many pbuf availables*/
        for(q = p; q != NULL; q = q->next)
        {
            /*payload pointer in the pbuf contains the data in the TCP segment*/
            rq = q->payload;
            length = q->len;
            
            /*send to UART*/
            while(length--)
            {
                /*FSL: blocking push to uart buffer*/
                xUARTPutChar(UARThandle, *(rq++), portMAX_DELAY);
            }
        }
        /* Inform TCP that we have taken the data. */
        tcp_recved(pcb, p->tot_len);
        
        /* Free the pbuf */
        pbuf_free(p);
    }
    else
    {
    	/*close session if CLIENT did it first*/
      BRIDGE_UART_ETH_CLOSE(pcb, hs);
    }      
    return ERR_OK;
}

/**
 * Send to Ethernet as soon as there are available characters on UART queue
 *
 * @param array to get data  
 * @return zero if everything's fine, otherwise 1
 */
static err_t 
BRIDGE_UART_ETH_TX( int8 *array )
{
  uint16 i=0;

  /*Only transmit if socket is already opened*/
  if( p_uart_tx_state.tx_pcb->state == ESTABLISHED )
  {
    /*wait for a continuos transfer and must be lower than buffer size*/
    while( ( i < (UART_BUFFER_LIMIT) ) && (xUARTGetCharWithFlowControl(UARThandle,&array[i])) )
    {
      i++;
    }

  	/*only send if there are available characters*/
    if(i)
    {                   
      /*FSL: do not start a new one until this is over*/
      xSemaphoreTake(UARTmutex, portMAX_DELAY);

      p_uart_tx_state.p_bridge_state->data = array;
      p_uart_tx_state.p_bridge_state->left = i;
      
      /* Tell TCP that we wish be to informed of data that has been
      successfully sent by a call to the BRIDGE_UART_ETH_SEND_CALLBACK() function. */
      tcp_sent(p_uart_tx_state.tx_pcb, BRIDGE_UART_ETH_SEND_CALLBACK);

    	/*build packet to send*/
    	BRIDGE_UART_ETH_SEND(p_uart_tx_state.tx_pcb, p_uart_tx_state.p_bridge_state);
    }    
  }  
  return ERR_OK;
}

/**
 * Ethernet to UART task
 *
 * @param none  
 * @return none
 */
void
BRIDGE_UART_Task( void *pvParameters )
{
    /*tcp/ip struct holding connection information*/
    struct tcp_pcb *pcb;
    /*buffer to hold serial information*/
    static int8 *serial_receive_array;
    /*client mode: connect to this server address*/
    struct ip_addr ServerIPAddr;
    
    /* Parameters are not used - suppress compiler error */
    ( void )pvParameters;

    /*wait until tcp/ip stack has a valid IP address*/
    while( (uint8)get_lwip_ready() == FALSE )
    {
       /*Leave execution for 1000 ticks*/
       vTaskDelay(1000);
    }

    /*array space*/
    if( (serial_receive_array=(static int8 *)mem_malloc( UART_BUFFER_LIMIT>>1 )) == NULL )
    {
      /*Task no longer needed*/
      vTaskDelete(NULL);
    }

    /*FSL: create semaphore that will allow to sleep process*/
    vSemaphoreCreateBinary(xUARTSemaphore);
    
    /*FSL: create mutex for shared resource*/
    UARTmutex = xSemaphoreCreateMutex();

    /**********************FSL: serial start-up*******************************/
    //if UARThandle NULL, serial cannot be used!!!
    UARThandle = xUARTinit((eCOMPort)board_get_uart_port()/*serCOM1*/, 
                             (eBaud)board_get_uart_baud()/*ser19200*/, 
                             (eParity)board_get_uart_parity()/*serNO_PARITY*/, 
                             (eDataBits)board_get_uart_number_of_bits()/*serBITS_8*/, 
                             (eStopBits)board_get_uart_stop_bits()/*serSTOP_1*/,
                             (eFlowControl)board_get_uart_flow_control()/*serFlowControlXONXOFF*/,
                             (eCOMsemaphore)serSemaphoreON,/*Turn on semaphore ON activity*/  
                             UART_BUFFER_LIMIT/*defined at header file*/);
    
    /*if handle cant be created*/
    if( UARThandle == NULL )
    {
      /*Task no longer needed*/
      vTaskDelete(NULL);      
    }

    /**********************FSL: low level start-up****************************/

    /* Create a new TCP PCB. */
    pcb = tcp_new();
    
    /*check for server or client init*/
    if( !(uint8)board_get_bridge_tcp_server() )
    {
      /*server*/
      /* Bind the PCB to specified TCP port. */
      tcp_bind(pcb, IP_ADDR_ANY, (uint16)board_get_bridge_tcp_port());
      /* Change TCP state to LISTEN */
      pcb = tcp_listen(pcb);
      /* callback when a new connection arrives */
      tcp_accept(pcb, BRIDGE_UART_Accept);      
    }
    else
    {
      /*get server address*/
      ServerIPAddr.addr = (uint32)board_get_eth_server_add();
      /*client connection*/
      if( tcp_connect(pcb,&ServerIPAddr,(uint16)board_get_bridge_tcp_port(),BRIDGE_UART_Accept) != ERR_OK )
      {
        /*Task no longer needed*/
        vTaskDelete(NULL);        
      }
    }

    /*************************************************************************/

    /* Loop forever */
    for( ;; )
    {	       
       /*Block task until UART first character arrives*/
       xSemaphoreTake( xUARTSemaphore, portMAX_DELAY );

       /*FSL:available elements from UART ready to send to MAC buffers*/
       BRIDGE_UART_ETH_TX(serial_receive_array);
    }
      
    return;/*FSL:never get here!!*/
}