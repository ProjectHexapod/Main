/* ------------------------ System includes ------------------------------- */
#include "stdlib.h"
#include "mcu_init.h"

/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"

/* ------------------------ lwIP includes --------------------------------- */
#include "lwip/api.h"
#include "lwip/dhcp.h"
#include "lwip/tcpip.h"
#include "lwip/ip.h"
#include "lwip/memp.h"
#include "lwip/stats.h"

#include "netif/loopif.h"
#include "mac_rtos.h"
#include "setget.h"
#include "utilities.h"

#include "clock.h"

/*FSL: default interface descriptor: ETH0*/
/*global variable not accesible to rest of the project due to its static condition*/
static struct netif fec5xxx_if;

/*stack is ready to be called*/
static uint8 lwip_ready = FALSE;

/**
 * set stack state
 *
 * @param TRUE if ready, otherwise FALSE 
 * @return none
 */
void 
set_lwip_ready(uint8 ready)
{
  lwip_ready = ready;
}

/**
 * get stack state
 *
 * @param none
 * @return TRUE if ready, otherwise FALSE
 */
uint8 
get_lwip_ready(void)
{
  return lwip_ready;
}

/*********************************Functions***********************************/

/**
 * get interface state, if ip is already configured
 *
 * @param none 
 * @return 1 if interface is up, otherwise zero
 */
uint8 
lwip_interface_is_up(void)
{
   return netif_is_up(&fec5xxx_if);
}

/**********************Public Functions **************************************/

/**
 * starts lwip tcp/ip stack
 *
 * @param none 
 * @return none
 */
void
vlwIPInit( void )
{
    struct ip_addr  xIpAddr, xNetMast, xGateway;       
    
    /* Initialize lwIP and its interface layer. */
    sys_init(  );
    mem_init(  );
    memp_init(  );
    pbuf_init(  );
    netif_init(  );
    ip_init(  );
    tcpip_init( NULL, NULL );

    /**********************FSL: FEC start-up**********************************/
     
	  /* Create and configure the FEC interface. */
	  xIpAddr.addr = board_get_eth_ip_add();
	  xNetMast.addr = board_get_eth_netmask();   
	  xGateway.addr = board_get_eth_gateway();

    /*add configured interface and gring up MAC controller*/
    netif_add( &fec5xxx_if, &xIpAddr, &xNetMast, &xGateway, NULL, MAC_init, tcpip_input );

    /* make it the default interface */
    netif_set_default( &fec5xxx_if );
    

   /* bring it up */
   netif_set_up( &fec5xxx_if );
   /*FSL:stack init is ready*/
   set_lwip_ready(TRUE);
    
    return;
}

/**
 * Low level call to init hardware
 *
 * @param none 
 * @return none
 */
void 
MCU_startup()
{
   /*basic MCU startup*/
   MCU_init();

   /*FSL: init flash once*/  
   FlashInit();
   
   return;
}

/**
 * set targeted MCU
 *
 * @param none
 * @return none
 */
void
MCU_reset(void)
{
  MCU_low_level_reset();
}