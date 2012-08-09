/*
 * A simple server direcly interfacing the tcp/ip stack:
 *
 * Features:
 *   session is not closed until client does it first: TODO: automatic close
 *   SERIAL side sends if: at least a character is ready AND a 1/2 second has occurred.
 *   default serial working at 115.2Kbps 8-N-1
 *   tcp packet length sent from the client only depends on client
 *   serial buffers lengths were selected according to performance and limits in memory
 *   SW and HW flow control avoid to drop characters
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

void
SendSerialTask( void *pvParameters );

/*-----------------------------------------------------------------------------------*/
static void
close_conn(struct tcp_pcb *pcb, struct bridge_state *hs)
{
  tcp_arg(pcb, NULL);
  tcp_sent(pcb, NULL);
  tcp_recv(pcb, NULL);
  mem_free(hs);
  tcp_close(pcb);
}

/*-----------------------------------------------------------------------------------*/
static void
send_data(struct tcp_pcb *pcb, struct bridge_state *hs)
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

/*-----------------------------------------------------------------------------------*/
void 
conn_err(void *arg, err_t err)
{
  struct bridge_state *hs;

  hs = arg;
  mem_free(hs);
}

/*-----------------------------------------------------------------------------------*/
err_t 
http_sent(void *arg, struct tcp_pcb *pcb, u16_t len)
{
  struct bridge_state *hs;

  hs = arg;
  
  if (hs->left > 0) 
  {
    send_data(pcb, hs);
  } 
  else 
  {
    /*FSL: tcp transaction is over: release simple internal flag*/
    xSemaphoreGive(UARTmutex);
    
    tcp_sent(pcb, NULL);    
  }

  return ERR_OK;
}

/* accepted connection */
static err_t
connection_accept(void *arg, struct tcp_pcb *pcb, err_t err)
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
  tcp_recv(pcb, tcp_rx);

  tcp_err(pcb, conn_err);

  tcp_setprio(pcb,TCP_PRIO_MAX);
  
  return ERR_OK;
}

/*****************************************************************************/

static err_t
tcp_rx(void *arg, struct tcp_pcb *pcb, struct pbuf *p, err_t err)
{
    struct bridge_state *hs;
    char *rq;
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
                xSerialPutChar(UARThandle, *(rq++), portMAX_DELAY);
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
      close_conn(pcb, hs);
    }      
    return ERR_OK;
}

/*FSL:send as soon as there are available characters on UART queue*/
static err_t 
tcp_tx( int8 *array )
{
  uint16 i=0;

  /*Only transmit if socket is already opened*/
  if( p_uart_tx_state.tx_pcb->state == ESTABLISHED )
  {
    /*wait for a continuos transfer and must be lower than buffer size*/
    while( ( i < (SERIAL_BUFFER_LIMIT) ) && (xSerialGetCharFlowControl(UARThandle,&array[i])) )
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
      successfully sent by a call to the http_sent() function. */
      tcp_sent(p_uart_tx_state.tx_pcb, http_sent);

    	/*build packet to send*/
    	send_data(p_uart_tx_state.tx_pcb, p_uart_tx_state.p_bridge_state);
    }    
  }  
  return ERR_OK;
}

/*FSL: running task*/
void
vBasicSerialBridge( void *pvParameters )
{
    /*tcp/ip struct holding connection information*/
    struct tcp_pcb *pcb;
    /*buffer to hold serial information*/
    static int8 *serial_receive_array;
    
    /* Parameters are not used - suppress compiler error */
    ( void )pvParameters;

    /*array space*/
    serial_receive_array = ( static int8 * )pvPortMalloc( SERIAL_BUFFER_LIMIT );

    /*FSL: create semaphore that will allow to sleep process*/
    //xUARTSemaphore = xSemaphoreCreateCounting(10,0);
    vSemaphoreCreateBinary(xUARTSemaphore);
    
    /*FSL: create mutex for shared resource*/
    UARTmutex = xSemaphoreCreateMutex();

    /**********************FSL: low level start-up****************************/
    /* Create a new TCP PCB. */
    pcb = tcp_new();
    /* Bind the PCB to specified TCP port. */
    tcp_bind(pcb, IP_ADDR_ANY, SERIAL_BRIDGE_PORT);
    /* Change TCP state to LISTEN */
    pcb = tcp_listen(pcb);
    /* callback when a new connection arrives */
    tcp_accept(pcb, connection_accept);

    /**********************FSL: serial start-up*******************************/
    //if UARThandle NULL, serial cannot be used!!!
    UARThandle = xSerialPortInit((eCOMPort)board_get_serial_port()/*serCOM1*/, 
                             (eBaud)board_get_serial_baud()/*ser19200*/, 
                             (eParity)board_get_serial_parity()/*serNO_PARITY*/, 
                             (eDataBits)board_get_serial_number_of_bits()/*serBITS_8*/, 
                             (eStopBits)board_get_serial_stop_bits()/*serSTOP_1*/,
                             (eFlowControl)board_get_serial_flow_control()/*serFlowControlXONXOFF*/,
                             (eCOMsemaphore)serSemaphoreON,/*Turn on semaphore ON activity*/  
                             SERIAL_BUFFER_LIMIT/*defined at header file*/);

    /* Loop forever */
    for( ;; )
    {	       
       /*Block task until a UART character arrives*/
       xSemaphoreTake( xUARTSemaphore, portMAX_DELAY );

       /*FSL:available elements from UART ready to send to MAC buffers*/
       tcp_tx(serial_receive_array);
    }
      
    return;/*FSL:never get here!!*/
}