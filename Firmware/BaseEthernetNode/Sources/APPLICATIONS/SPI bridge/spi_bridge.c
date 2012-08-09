/*
 * A simple server/client socket interfacing the tcp/ip stack directly:
 * b06862
 *
 * Features:
 *   session is not closed until client does it first: TODO: automatic close
 *   SERIAL side sends if: at least a character is ready AND a 1/2 second has occurred.
 *   tcp packet length sent from the client only depends on client
 *   serial buffers lengths were selected according to performance and limits in memory
 *   will drop characters if internal queue is full
 */

/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

/* ------------------------ lwIP includes --------------------------------- */
#include "tcp.h"

/* ------------------------ Project includes ------------------------------ */
#include "spi_bridge.h"
#include "spi_rtos.h"
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
struct spi_tx_state
{
  struct tcp_pcb *tx_pcb;
  struct bridge_state *p_bridge_state;
};

/*FSL: variable holding usefull SPI/MAC information*/
struct spi_tx_state p_spi_tx_state;

/*Handle for SPI capabilities*/
xSPIPortHandle SPIhandle;

/*Mutex to MAC buffers*/
xSemaphoreHandle SPImutex;

/*Semaphore to wake up task: comes from spi_rtos.c*/
extern xSemaphoreHandle xSPISemaphore;

/*buffer to hold received spi information*/
static int8 *spi_receive_array;

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
BRIDGE_SPI_ETH_CLOSE(struct tcp_pcb *pcb, struct bridge_state *hs);

/**
 * Function called when a packet needs to be sent thru Ethernet
 *  Automatically split packet lenght to fit on packet max size
 *
 * @param tcp connection descriptor
 * @param bridge information
 * @return none
 */
static void
BRIDGE_SPI_ETH_SEND(struct tcp_pcb *pcb, struct bridge_state *hs);

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
BRIDGE_SPI_ETH_CLOSE(struct tcp_pcb *pcb, struct bridge_state *hs)
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
BRIDGE_SPI_ETH_SEND(struct tcp_pcb *pcb, struct bridge_state *hs)
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
    //tcp_output(pcb);   
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
BRIDGE_SPI_ETH_ERROR(void *arg, err_t err)
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
BRIDGE_SPI_ETH_SEND_CALLBACK(void *arg, struct tcp_pcb *pcb, u16_t len)
{
  struct bridge_state *hs;

  hs = arg;
  
  if (hs->left > 0) 
  {
    BRIDGE_SPI_ETH_SEND(pcb, hs);
  } 
  else 
  {    
    tcp_sent(pcb, NULL);    
  
    /*FSL: tcp transaction is over: release simple internal flag*/
    xSemaphoreGive(SPImutex);
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
BRIDGE_SPI_Accept(void *arg, struct tcp_pcb *pcb, err_t err)
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

  /*spi structure*/
  p_spi_tx_state.tx_pcb = pcb;
  p_spi_tx_state.p_bridge_state = hs;

  /* Tell TCP that this is the structure we wish to be passed for our callbacks */
  tcp_arg(pcb, hs);

  /*called function when RX*/
  tcp_recv(pcb, BRIDGE_SPI_ETH_RX);

  tcp_err(pcb, BRIDGE_SPI_ETH_ERROR);

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
BRIDGE_SPI_ETH_RX(void *arg, struct tcp_pcb *pcb, struct pbuf *p, err_t err)
{
    uint16 i;
    struct bridge_state *hs;
    char *rq;
    uint16 length;
    struct pbuf *q;
    spiMode actual_spi_mode = (spiMode)board_get_spi_master();
    eSPIPort actual_spi_port = (eSPIPort)board_get_spi_port();

    hs = arg;
    
    /* If we got a NULL pbuf in p, the remote end has closed the connection. */
    if(p != NULL) 
    {                
        /*Enable Chip Select*/
        if( actual_spi_mode == serMaster )
        {
          xSPIEnableChipSelect(actual_spi_port);
        }
 
        /*FSL:send as many pbuf availables*/
        for(q = p; q != NULL; q = q->next)
        {
          /*spi master handling*/
          if( actual_spi_mode == serMaster )
          {
            /*FSL: do not start a new one until this is over*/
            xSemaphoreTake(SPImutex, portMAX_DELAY);
            
            /*payload pointer in the pbuf contains the data in the TCP segment*/
            rq = q->payload;
            length = q->len;
            
            /*FSL: update Ethernet tx index*/
            p_spi_tx_state.p_bridge_state->data = (int8 *)spi_receive_array;
            p_spi_tx_state.p_bridge_state->left = length;
            
            i=0;
            /*send to SPI*/
            while(length--)
            {
                /*FSL: push to spi controller buffer*/
                xSPIMasterSetGetChar(SPIhandle, *(rq++), spi_receive_array+i, portMAX_DELAY);
                i++;
            }
            
            /* Tell TCP that we wish be to informed of data that has been
            successfully sent by a call to the http_sent() function. */
            tcp_sent(p_spi_tx_state.tx_pcb, BRIDGE_SPI_ETH_SEND_CALLBACK);

          	/*build packet to send*/
          	BRIDGE_SPI_ETH_SEND(p_spi_tx_state.tx_pcb, p_spi_tx_state.p_bridge_state);            
          }
          /*spi slave handling*/
          else
          {
            /*payload pointer in the pbuf contains the data in the TCP segment*/
            rq = q->payload;
            length = q->len;

            /*send to SPI in slave mode: will be dequeue when a character is sent thru SPI*/
            while(length--)
            {
                /*FSL: push to spi controller buffer: if buffer is full, then character is dropped!*/
                if( xSPISlaveSendChar(SPIhandle,*(rq++),0) == pdFAIL )
                {
                  break;
                }
            }          
          }
        }

        /*Disable Chip Select*/
        if( actual_spi_mode == serMaster )
        {
          xSPIDisableChipSelect(actual_spi_port);
        }       
        
        /* Inform TCP that we have taken the data. */
        tcp_recved(pcb, p->tot_len);
        
        /* Free the pbuf */
        pbuf_free(p);
    }
    else
    {
    	/*close session if CLIENT did it first*/
      BRIDGE_SPI_ETH_CLOSE(pcb, hs);
    }      
    return ERR_OK;
}

/**
 * Send to Ethernet as soon as there are available characters on SPI queue
 *
 * @param none  
 * @return zero if everything's fine, otherwise 1
 */
static err_t 
BRIDGE_SPI_ETH_TX( void )
{
  uint16 i=0;

  /*Only transmit if socket is already opened*/
  if( p_spi_tx_state.tx_pcb->state == ESTABLISHED )
  {
    /*wait for a continuos transfer and must be lower than buffer size*/
    while( ( i < (SPI_BRIDGE_BUFFER_LIMIT) ) && 
           /*wait only 1 TICK*/
           (xSPISlaveReceiveChar(SPIhandle,&spi_receive_array[i],1)) )
    {
      i++;
    }

  	/*only send if there are available characters*/
    if(i)
    {                   
      /*FSL: do not start a new one until this is over*/
      xSemaphoreTake(SPImutex, portMAX_DELAY);

      /*FSL: update Ethernet tx index*/
      p_spi_tx_state.p_bridge_state->data = (int8 *)spi_receive_array;
      p_spi_tx_state.p_bridge_state->left = i;
      
      /* Tell TCP that we wish be to informed of data that has been
      successfully sent by a call to the http_sent() function. */
      tcp_sent(p_spi_tx_state.tx_pcb, BRIDGE_SPI_ETH_SEND_CALLBACK);

      /*build packet to send*/
      BRIDGE_SPI_ETH_SEND(p_spi_tx_state.tx_pcb, p_spi_tx_state.p_bridge_state); 
    }    
  }  
  return ERR_OK;
}

/**
 * Ethernet to SPI task
 *
 * @param none  
 * @return none
 */
void
BRIDGE_SPI_Task( void *pvParameters )
{
    /*tcp/ip struct holding connection information*/
    struct tcp_pcb *pcb;
    /*client mode: connect to this server address*/
    struct ip_addr ServerIPAddr;
    
    /* Parameters are not used - suppress compiler error */
    ( void )pvParameters;

    /*wait until tcp/ip stack has a valid IP address*/
    while( get_lwip_ready() == FALSE )
    {
       /*Leave execution for 1000 ticks*/
       vTaskDelay(1000);
    }

    /*SPI array space*/
    if( (spi_receive_array = ( static int8 * )mem_malloc( PBUF_POOL_BUFSIZE )) == NULL )
    {
      /*Task no longer needed*/
      vTaskDelete(NULL);
    }
    
    /*FSL: create mutex for shared resource*/
    SPImutex = xSemaphoreCreateMutex();

#warning "check max baudrate as a spi slave!!"

    /**********************FSL: spi start-up*******************************/
    //if SPIhandle NULL, serial cannot be used!!!
    SPIhandle = xSPIinit((eSPIPort)board_get_spi_port()/*serSPI2*/, 
                             (spiBaud)board_get_spi_baud()/*ser1000*/, 
                             (spiPolarity)board_get_spi_polarity()/*serIDLEslow*/, 
                             (spiPhase)board_get_spi_phase()/*serMiddleSample*/, 
                             (spiMode)board_get_spi_master()/*serMaster*/,
                             (spiInterrupt)board_get_spi_interrupt()/*serPolling*/,  
                             SPI_BRIDGE_BUFFER_LIMIT/*defined at header file*/);

    /*if handle cant be created*/
    if( SPIhandle == NULL )
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
      tcp_accept(pcb, BRIDGE_SPI_Accept);      
    }
    else
    {
      /*get server address*/
      ServerIPAddr.addr = (uint32)board_get_eth_server_add();
      /*client connection*/
      if( tcp_connect(pcb,&ServerIPAddr,(uint16)board_get_bridge_tcp_port(),BRIDGE_SPI_Accept) != ERR_OK )
      {
        /*Task no longer needed*/
        vTaskDelete(NULL);        
      }
    }

    if( (spiMode)board_get_spi_master() == serMaster )
    {
      /*Task no longer needed, delete it!*/
      vTaskDelete( NULL );  
    }
    else /*slave support*/
    {
      /*FSL: create semaphore that will allow to sleep process*/
      //xSPISemaphore = xSemaphoreCreateCounting(10,0);
      vSemaphoreCreateBinary(xSPISemaphore);
      
      /* Loop forever */
      for( ;; )
      {	       
         /*Block task until first SPI character arrives*/
         xSemaphoreTake( xSPISemaphore, portMAX_DELAY );
         
         /*FSL:available elements from SPI ready to send to MAC buffers*/
         BRIDGE_SPI_ETH_TX();
      }      
    }
 
    return;/*FSL:never get here!!*/
}