/*
 * File:        setget.c
 * Purpose:     Board support functions for the global set/show routines
 *
 * Notes:       
 *
 */

/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"

#include "setget.h"
#include "flash.h"

/********************************************************************/
void
update_board_params (uint8 *data, uint16 length, uint32 offset)
{
    /*
     * This function copies the PARAM section of the Flash
     * into SRAM, modifies the SRAM copy of PARAM with 'data'
     * for 'length' bytes, then writes the updated copy into
     * Flash again.
     */
    uint8 *target;
    uint16 index;
    ROM_OPTIONS ram_options;/*temporal variable to hold rom options*/
    
    target = (uint8 *)((uint32)&ram_options + offset);
 
    memcpy((void*)&ram_options,(void*)CUSTOM_ROM_ADDRESS,ROM_OPTIONS_SIZE); 
 
    for (index = 0; index < length; ++index)
    {
        *target++ = *data++;
    }                               
 
    /*FSL:critical section*/
	  portENTER_CRITICAL();	  
	  
	  /*erase logical page*/
    Flash_Erase(CUSTOM_ROM_ADDRESS);
    /*write logical page*/             
    Flash_Burst(CUSTOM_ROM_ADDRESS, ROM_OPTIONS_LONG_SIZE, &ram_options);

	  portEXIT_CRITICAL();

    return;
}

/********************************************************************/
void
get_all_params (void *data)
{

    memcpy(data,(void*)CUSTOM_ROM_ADDRESS,ROM_OPTIONS_SIZE);

    return;
}

/********************************************************************/
void 
set_all_params (void *data)
{
    /*FSL:critical section*/
	  portENTER_CRITICAL();	  
	  
	  /*erase logical page*/
    Flash_Erase(CUSTOM_ROM_ADDRESS);
    /*write logical page*/             
    Flash_Burst(CUSTOM_ROM_ADDRESS, ROM_OPTIONS_LONG_SIZE, data);

	  portEXIT_CRITICAL();

    return;    
}

/***********GET FUNCTIONS******************/

/****************************Ethernet Get functions******************/

/********************************************************************/
void
board_get_eth_ethaddr (uint8 ethaddr[])
{
    uint8 i;

    for (i = 0; i < 6; i++)
    {
        ethaddr[i] = ((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->eth_ethaddr[i];
    }
}

/********************************************************************/
uint32
board_get_eth_ip_add (void)
{
    uint8 i;
    T32_8 eth_ip_add;

    for (i = 0; i < 4; i++)
    {
        eth_ip_add.bytes[i] = ((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->eth_ip_add[i];
    }
    
    return eth_ip_add.lword;
}

/********************************************************************/
uint32
board_get_eth_netmask (void)
{
    uint8 i;
    T32_8 eth_netmask;

    for (i = 0; i < 4; i++)
    {
        eth_netmask.bytes[i] = ((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->eth_netmask[i];
    }
    
    return eth_netmask.lword;
}

/********************************************************************/
uint32
board_get_eth_gateway (void)
{
    uint8 i;
    T32_8 eth_gateway;

    for (i = 0; i < 4; i++)
    {
        eth_gateway.bytes[i] = ((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->eth_gateway[i];
    }
    
    return eth_gateway.lword;
}

/********************************************************************/
uint32
board_get_eth_server_add (void)
{
    uint8 i;
    T32_8 eth_server_add;

    for (i = 0; i < 4; i++)
    {
        eth_server_add.bytes[i] = ((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->eth_server_add[i];
    }
    
    return eth_server_add.lword;
}

/****************************Bridge Get functions********************/

/********************************************************************/
uint8
board_get_eth_dhcp_auto (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->eth_dhcp_auto);
}

/********************************************************************/
uint8
board_get_bridge_configuration (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->bridge_configuration);
}

/********************************************************************/
uint8
board_get_bridge_tcp_mode (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->bridge_tcp_mode);
}

/********************************************************************/
uint8
board_get_bridge_tcp_server (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->bridge_tcp_server);
}

/********************************************************************/
uint16
board_get_bridge_tcp_port (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->bridge_tcp_port);
}


/****************************UART Get functions**********************/

/********************************************************************/
uint8
board_get_uart_port (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->uart_port);
}

/********************************************************************/
uint32
board_get_uart_baud (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->uart_baud);
}

/********************************************************************/
uint8
board_get_uart_parity (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->uart_parity);
}

/********************************************************************/
uint8
board_get_uart_number_of_bits (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->uart_number_of_bits);
}

/********************************************************************/
uint8
board_get_uart_stop_bits (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->uart_stop_bits);
}

/********************************************************************/
uint8
board_get_uart_flow_control (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->uart_flow_control);
}

/****************************SPI Get functions***********************/

/********************************************************************/
uint8
board_get_spi_port (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->spi_port);
}

/********************************************************************/
uint16
board_get_spi_baud (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->spi_baud);
}

/********************************************************************/
uint8
board_get_spi_polarity (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->spi_polarity);
}

/********************************************************************/
uint8
board_get_spi_phase (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->spi_phase);
}

/********************************************************************/
uint8
board_get_spi_master (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->spi_master);
}

/********************************************************************/
uint8
board_get_spi_interrupt (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->spi_interrupt);
}

/****************************EMail Get functions*********************/

/********************************************************************/
void
board_get_email_username (uint8 email_username[])
{
    uint8 i;
    for (i = 0; i < STRING_SIZE; i++)
    {
        if ( (email_username[i] = ((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->email_username[i]) == '\0' )
        {
           break;
        }
    }    
}
/********************************************************************/
void
board_get_email_password (uint8 email_password[])
{
    uint8 i;
    for (i = 0; i < STRING_SIZE; i++)
    {
        if ( (email_password[i] = ((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->email_password[i]) == '\0' )
        {
           break;
        }
    }    
}
/********************************************************************/
void
board_get_email_smtp_server (uint8 email_smtp_server[])
{
    uint8 i;
    for (i = 0; i < STRING_SIZE; i++)
    {
        if ( (email_smtp_server[i] = ((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->email_smtp_server[i]) == '\0' )
        {
           break;
        }
    }    
}

/********************************************************************/
uint8
board_get_email_authentication_required (void)
{
    return (((ROM_OPTIONS *)CUSTOM_ROM_ADDRESS)->email_authentication_required);
}

/***********SET FUNCTIONS******************/

/****************************Ethernet Set functions******************/

/********************************************************************/
void
board_set_eth_ethaddr (uint8 ethaddr[])
{
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    update_board_params(ethaddr, 6, (uint32)&tparam->eth_ethaddr);
}

/********************************************************************/
void
board_set_eth_ip_add (uint32 eth_ip_add)
{
    uint8 var[4];
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint32 *)var) = eth_ip_add;

    update_board_params(var, 4, (uint32)&tparam->eth_ip_add);
}

/********************************************************************/
void
board_set_eth_netmask (uint32 eth_netmask)
{
    uint8 var[4];
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint32 *)var) = eth_netmask;

    update_board_params(var, 4, (uint32)&tparam->eth_netmask);
}

/********************************************************************/
void
board_set_eth_gateway (uint32 eth_gateway)
{
    uint8 var[4];
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint32 *)var) = eth_gateway;

    update_board_params(var, 4, (uint32)&tparam->eth_gateway);
}

/********************************************************************/
void
board_set_eth_server_add (uint32 eth_server_add)
{
    uint8 var[4];
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint32 *)var) = eth_server_add;

    update_board_params(var, 4, (uint32)&tparam->eth_server_add);
}

/****************************Bridge Set functions********************/

/********************************************************************/
void
board_set_eth_dhcp_auto (uint8 eth_dhcp_auto)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = eth_dhcp_auto;

    update_board_params(var, 1, (uint32)&tparam->eth_dhcp_auto);
}

/********************************************************************/
void
board_set_bridge_configuration (uint8 bridge_configuration)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = bridge_configuration;

    update_board_params(var, 1, (uint32)&tparam->bridge_configuration);
}

/********************************************************************/
void
board_set_bridge_tcp_mode (uint8 bridge_tcp_mode)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = bridge_tcp_mode;

    update_board_params(var, 1, (uint32)&tparam->bridge_tcp_mode);
}

/********************************************************************/
void
board_set_bridge_tcp_server (uint8 bridge_tcp_server)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = bridge_tcp_server;

    update_board_params(var, 1, (uint32)&tparam->bridge_tcp_server);
}

/********************************************************************/
void
board_set_bridge_tcp_port (uint16 bridge_tcp_port)
{
    uint8 var[2];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint16 *)var) = bridge_tcp_port;

    update_board_params(var, 2, (uint32)&tparam->bridge_tcp_port);
}

/****************************UART Set functions**********************/

/********************************************************************/
void
board_set_uart_port (uint8 uart_port)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = uart_port;

    update_board_params(var, 1, (uint32)&tparam->uart_port);
}

/********************************************************************/
void
board_set_uart_baud (uint32 uart_baud)
{
    uint8 var[4];
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint32 *)var) = uart_baud;

    update_board_params(var, 4, (uint32)&tparam->uart_baud);
}

/********************************************************************/
void
board_set_uart_parity (uint8 uart_parity)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = uart_parity;

    update_board_params(var, 1, (uint32)&tparam->uart_parity);
}

/********************************************************************/
void
board_set_uart_number_of_bits (uint8 uart_number_of_bits)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = uart_number_of_bits;

    update_board_params(var, 1, (uint32)&tparam->uart_number_of_bits);
}

/********************************************************************/
void
board_set_uart_stop_bits (uint8 uart_stop_bits)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = uart_stop_bits;

    update_board_params(var, 1, (uint32)&tparam->uart_stop_bits);
}

/********************************************************************/
void
board_set_uart_flow_control (uint8 uart_flow_control)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = uart_flow_control;

    update_board_params(var, 1, (uint32)&tparam->uart_flow_control);
}

/****************************SPI Set functions***********************/

/********************************************************************/
void
board_set_spi_port (uint8 spi_port)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = spi_port;

    update_board_params(var, 1, (uint32)&tparam->spi_port);
}

/********************************************************************/
void
board_set_spi_baud (uint16 spi_baud)
{
    uint8 var[2];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint16 *)var) = spi_baud;

    update_board_params(var, 1, (uint32)&tparam->spi_baud);
}

/********************************************************************/
void
board_set_spi_polarity (uint8 spi_polarity)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = spi_polarity;

    update_board_params(var, 1, (uint32)&tparam->spi_polarity);
}

/********************************************************************/
void
board_set_spi_phase (uint8 spi_phase)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = spi_phase;

    update_board_params(var, 1, (uint32)&tparam->spi_phase);
}

/********************************************************************/
void
board_set_spi_master (uint8 spi_master)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = spi_master;

    update_board_params(var, 1, (uint32)&tparam->spi_master);
}

/********************************************************************/
void
board_set_spi_interrupt (uint8 spi_interrupt)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = spi_interrupt;

    update_board_params(var, 1, (uint32)&tparam->spi_interrupt);
}

/****************************EMail Set functions*********************/


/********************************************************************/
void
board_set_email_username (uint8 email_username[])
{
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    update_board_params(email_username, STRING_SIZE, (uint32)&tparam->email_username);
}
/********************************************************************/
void
board_set_email_password (uint8 email_password[])
{
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    update_board_params(email_password, STRING_SIZE, (uint32)&tparam->email_password);
}
/********************************************************************/
void
board_set_email_smtp_server (uint8 email_smtp_server[])
{
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    update_board_params(email_smtp_server, STRING_SIZE, (uint32)&tparam->email_smtp_server);
}
/********************************************************************/
void
board_set_email_authentication_required (uint8 email_authentication_required)
{
    uint8 var[1];
    
    ROM_OPTIONS *tparam = (ROM_OPTIONS *)NULL;

    *((uint8 *)var) = email_authentication_required;

    update_board_params(var, 1, (uint32)&tparam->email_authentication_required);
}

/********************************************************************/

/*Function array*/
const SIX_BYTES six_bytes_array[] = 
{
    {board_get_eth_ethaddr,board_set_eth_ethaddr},
    {board_get_email_username,board_set_email_username},
    {board_get_email_password,board_set_email_password},
    {board_get_email_smtp_server,board_set_email_smtp_server}
};

const FOUR_BYTES four_bytes_array[] = 
{
    {board_get_eth_ip_add,board_set_eth_ip_add},
    {board_get_eth_netmask,board_set_eth_netmask},
    {board_get_eth_gateway,board_set_eth_gateway},
    {board_get_eth_server_add,board_set_eth_server_add},
    {board_get_uart_baud,board_set_uart_baud}
};

const TWO_BYTES two_bytes_array[] = 
{
    {board_get_bridge_tcp_port,board_set_bridge_tcp_port},
    {board_get_spi_baud,board_set_spi_baud}
};

const ONE_BYTE one_byte_array[] = 
{
    {board_get_eth_dhcp_auto,board_set_eth_dhcp_auto},
    {board_get_bridge_configuration,board_set_bridge_configuration},
    {board_get_bridge_tcp_mode,board_set_bridge_tcp_mode},
    {board_get_bridge_tcp_server,board_set_bridge_tcp_server},
    {board_get_uart_port,board_set_uart_port},
    {board_get_uart_parity,board_set_uart_parity},
    {board_get_uart_number_of_bits,board_set_uart_number_of_bits},
    {board_get_uart_stop_bits,board_set_uart_stop_bits},
    {board_get_uart_flow_control,board_set_uart_flow_control},
    {board_get_spi_port,board_set_spi_port},
    {board_get_spi_polarity,board_set_spi_polarity},
    {board_get_spi_phase,board_set_spi_phase},
    {board_get_spi_master,board_set_spi_master},
    {board_get_spi_interrupt,board_set_spi_interrupt},
    {board_get_email_authentication_required,board_set_email_authentication_required}
};

uint8 
get_one_byte_elements()
{
  return ONE_BYTE_ELEMENTS;
}

uint8 
get_two_bytes_elements()
{
  return TWO_BYTES_ELEMENTS;
}

uint8 
get_four_bytes_elements()
{
  return FOUR_BYTES_ELEMENTS;
}

uint8 
get_six_bytes_elements()
{
  return SIX_BYTES_ELEMENTS;
}