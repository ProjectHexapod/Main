/*
    This file was adapted from a FreeRTOS lwIP slip demo supplied by a third party.
*/

/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

/* ------------------------ lwIP includes --------------------------------- */
#include "api.h"

#include "lwip/api.h"
#include "lwip/dhcp.h"
#include "lwip/tcpip.h"

#include "netif/loopif.h"
#include "mac_rtos.h"
#include "setget.h"

#include "dhcp_app.h"
#include "signals.h"

#include "email_client.h"
#include "utilities.h"

/*user name and password*/
#define EMAIL_RECIPIENT                       "MCF51CN128@freescale.com"
#define EMAIL_SUBJECT                         "IP Address Notification"

#define EMAIL_DATA_STRING   \
   "Hello, My IP Number is %d.%d.%d.%d, Do not reply!!\r\n\r\n" \
   "Have a good day\r\n\r\n-MCF51CN128\r\n"

/**************************Prototypes*****************************************/

/*FSL:sprintf prototype*/
INT
sprintf(CHAR *, const CHAR *, ... );

/**************************Functions******************************************/

/**
 * DHCP Task: request an IP address after reset
 *
 * @param ethernet descriptor
 * @return none
 */
void
vDHCPClient( void *pvParameters )
{
    struct netif *fecif;
    fecif = (struct netif *)pvParameters;

    netifapi_dhcp_start(fecif);

    while( (uint8)lwip_interface_is_up() == 0 ) 
    {
       /*Leave execution*/
       vTaskDelay(0);       
    }
    
    /*FSL:get ip addresses and store them in ROM*/
    board_set_eth_ip_add( fecif->ip_addr.addr );
    board_set_eth_netmask( fecif->netmask.addr );
    board_set_eth_gateway( fecif->gw.addr );

#if EMAIL_NOTIFICATION_AFTER_GETTING_IP_ADDRESS    
    {
      EMAIL_TEMPLATE email;
      CHAR *temporal_buffer;
      T32_8 ip;   /* IP address */
      
      if( (temporal_buffer = ( CHAR * )mem_malloc( 128 )) == NULL )
      {
        goto dhcp_exit_routine;
      }
      
      ip.lword = board_get_eth_ip_add();
      /*filling info*/
      email.to      = EMAIL_RECIPIENT;
      email.subject = EMAIL_SUBJECT;
      
      /*fill data with IP address*/
      sprintf(temporal_buffer,EMAIL_DATA_STRING,ip.bytes[0],ip.bytes[1],ip.bytes[2],ip.bytes[3]);
      email.data    = temporal_buffer;
      
      /*init email*/
      Email_init();
    
      /*send email: first*/
      Email_send(&email);
      
      while( email.flag )
      {        
        /*wait for completition*/
        vTaskDelay(100);
        /*a context switch might be called*/
      }
dhcp_exit_routine:

      /*delete space used by the variable until email is sent*/
      mem_free(temporal_buffer);

      /*FSL: at this point email has been sent or a failure has been found*/
#if 0      
      //how to test if an email has been sent or failed                  
      if( email.ready == 0 )
      {
         //sucessfully sent
      }
      else
      {
         //error!!!        
      }
#endif
    }
#endif

    /*FSL: start LED task: removed due to small ram memory */
    //( void )xTaskCreate( vToggleLED, (const signed portCHAR *)"LED", LED_STACK_SPACE, NULL, LED_TASK_PRIORITY, NULL );

    /*FSL:stack init is ready*/
    set_lwip_ready(TRUE);
#if 0/*checking stack space*/
    for(;;)
    {
       /*Leave execution*/
       vTaskDelay(1000);       
    }
#endif

    /*Task no longer needed, delete it!*/
    vTaskDelete( NULL );

    /*never get here!*/    
    return;
}

/**
 * Toggle LED Task: alive function
 *
 * @param none
 * @return none
 */
void
vToggleLED( void *pvParameters )
{
    (void)pvParameters;
    
    LED_toogle_init();    
    /*infinite loop*/
    for(;;)
    {
       LED_toggle();
       /*wait for while*/
       vTaskDelay(100);
    }  
}
