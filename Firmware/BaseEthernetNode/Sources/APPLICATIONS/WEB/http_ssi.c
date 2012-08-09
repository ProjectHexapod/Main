#include "http_ssi.h"
#include "stdlib.h"

#include "setget.h"
#include "utilities.h"

/*shared variable*/
uint8 default_language;

SSI_CMD SSI_CMD_ARRAY[]  = 
{
  SSI_CMD_CHANNEL0,
  SSI_CMD_CHANNEL1,
  SSI_CMD_CHANNEL2,
  SSI_CMD_COUNTER,
  SSI_CMD_GREETING,     /*for default dynamic web page*/
  SSI_CMD_BAUDRATE,     /*baudrate reader*/
  SSI_CMD_FLOWCONTROL,  /*flow control reader*/
  SSI_CMD_SERIALPORT,
  SSI_CMD_SERIALPARI,
  SSI_CMD_SERIALBITS,
  SSI_CMD_SERIALSTOP,
  SSI_CMD_MACADD,
  SSI_CMD_MACIPADD,
  SSI_CMD_MACGWADD,
  SSI_CMD_MACMKADD,
  SSI_CMD_MACSAADD,
  SSI_CMD_MACSTAT,
  SSI_CMD_TCPPORT,
  SSI_CMD_TCPSER,
  SSI_CMD_TCPCONF,
  SSI_CMD_TCPOUT,
  SSI_CMD_SPIPORT,
  SSI_CMD_SPIBAUD,
  SSI_CMD_SPIPOLA,
  SSI_CMD_SPIPHASE,
  SSI_CMD_SPIMAS,
  SSI_CMD_SPIINT
};

LANGUAGES WEB_LANGUAGES[] =
{
  ENGLISH_OPTION,
  FRENCH_OPTION,  
  DEUTCH_OPTION,  
  CHINESSE_OPTION,
  ITALIAN_OPTION, 
  RUSSIAN_OPTION, 
  JAPANESE_OPTION,
  ARABIC_OPTION,  
  TAIWAN_OPTION,  
  PORTUGAL_OPTION,
  POLISH_OPTION,  
  SPANISH_OPTION, 
  KOREAN_OPTION   
};

/*FSL:sprintf prototype*/
INT
sprintf(CHAR *, const CHAR *, ... );

/**
 * Implements a SSI Replacement
 *
 * @param array to replace
 * @param replaced array 
 * @return returned value by function linked to array to replace
 */
uint8 
SSI_parser(uint8 *input, uint8 *output)
{
     uint8 i;

     for(i=0;i<SSI_MAX_COMMANDS;i++)
     {
        if(!strncmp((const CHAR *)input,(const CHAR *)SSI_CMD_ARRAY[i].command,strlen(SSI_CMD_ARRAY[i].command)))//contains array
        {
            return SSI_CMD_ARRAY[i].func(output);//execute function if matches
        }
     }
     //SSI: no replacement was found!!!
     return NULL;
}

//***************************************************************************//

/*inline */uint8 
max_number_of_languages()
{
  return MAX_LANGUAGES;
}

static INT 
adc_channel0(void *var)
{    
    static uint8 counter1 = 0;
    
    sprintf(var,"%d",counter1++);
    
    return 1;
}

static INT 
adc_channel1(void *var)
{
    static uint8 counter2 = 50;
    
    sprintf(var,"%d",counter2++);
    
    return 1;
}

static INT 
adc_channel2(void *var)
{
    static uint8 counter3 = 100;
    
    sprintf(var,"%d",counter3++);
    
    return 1;
}

static INT 
html_counter(void *var)
{
    static uint8 counter4 = 200;
    
    sprintf(var,"%d",counter4++);
    
    return 1;    
}

static INT 
language_greeting(void *var)
{  
    //implement for languages!!!
    sprintf(var,"%s",WEB_LANGUAGES[default_language].language);
    
    return 1;	
}

static INT
baudrate_reader(void *var)
{   
    sprintf(var,"%d",board_get_uart_baud());
    
    return 1;	
}

static INT
flowcontrol_reader(void *var)
{  
    uint8 i = board_get_uart_flow_control();
    
    //replace for the string:
    switch(i)
    {
      case 0:
         strcpy(var,"None");
         break;
      case 1:
         strcpy(var,"Hardware");
         break;      
      case 2:
      default:
         strcpy(var,"Software");
         break;      
    }
    
    return 1;	
}

static INT
serialport_reader(void *var)
{  
    uint8 i = board_get_uart_port();
    
    //replace for the string:
    switch(i)
    {
      case 0:
      default:
         strcpy(var,"UART0");
         break;
      case 1:
         strcpy(var,"UART1");
         break;      
      case 2:
         strcpy(var,"UART2");
         break;      
    }
    
    return 1;	
}

static INT
serialparity_reader(void *var)
{  
    uint8 i = board_get_uart_parity();
    
    //replace for the string:
    switch(i)
    {
      case 0:
      default:
         strcpy(var,"NONE");
         break;
      case 1:
         strcpy(var,"ODD");
         break;      
      case 2:
         strcpy(var,"EVEN");
         break;      
    }
    
    return 1;	
}

static INT
serialbits_reader(void *var)
{  
    uint8 i = board_get_uart_number_of_bits();
    
    //replace for the string:
    switch(i)
    {
      case 3:
      default:
         strcpy(var,"8 bits");
         break;
      case 4:
         strcpy(var,"9 bits");
         break;      
    }
    
    return 1;	
}

static INT
serialstopbits_reader(void *var)
{  
    uint8 i = board_get_uart_stop_bits();
    
    //replace for the string:
    switch(i)
    {
      case 0:
      default:
         strcpy(var,"1 bit");
         break;      
    }
    
    return 1;	
}

/*MAC replacing routines*/
static INT
mac_macaddress_reader(void *var)
{  
    uint8 mac_address[6];
    
    board_get_eth_ethaddr(&mac_address);
    
    sprintf(var,MAC_ADDRESS_STRING,mac_address[0],mac_address[1],mac_address[2],mac_address[3],mac_address[4],mac_address[5]);
   
    return 1;	
}

/*IP address replacing routines*/
static INT
mac_ipaddress_reader(void *var)
{  
    T32_8 ip_address;
    
    ip_address.lword = board_get_eth_ip_add();
    
    sprintf(var,IP_ADDRESS_STRING,ip_address.bytes[0],ip_address.bytes[1],ip_address.bytes[2],ip_address.bytes[3]);
   
    return 1;	
}

/*IP Mask address replacing routines*/
static INT
mac_ipmkaddress_reader(void *var)
{  
    T32_8 ip_address;
    
    ip_address.lword = board_get_eth_netmask();
    
    sprintf(var,IP_ADDRESS_STRING,ip_address.bytes[0],ip_address.bytes[1],ip_address.bytes[2],ip_address.bytes[3]);
   
    return 1;	
}

/*IP Gateway address replacing routines*/
static INT
mac_ipgwaddress_reader(void *var)
{  
    T32_8 ip_address;
    
    ip_address.lword = board_get_eth_gateway();
    
    sprintf(var,IP_ADDRESS_STRING,ip_address.bytes[0],ip_address.bytes[1],ip_address.bytes[2],ip_address.bytes[3]);
   
    return 1;	
}

/*IP Server address replacing routines*/
static INT
mac_ipserveraddress_reader(void *var)
{  
    T32_8 ip_address;
    
    ip_address.lword = board_get_eth_server_add();
    
    sprintf(var,IP_ADDRESS_STRING,ip_address.bytes[0],ip_address.bytes[1],ip_address.bytes[2],ip_address.bytes[3]);
   
    return 1;	
}

/*mac address type*/
static INT
mac_static_reader(void *var)
{  
    uint8 i = board_get_eth_dhcp_auto();
    
    //replace for the string:
    switch(i)
    {
      case 0:
      default:
         strcpy(var,"Static");
         break;
      case 1:
         strcpy(var,"DHCP");
         break;      
    }
    
    return 1;	
}

/*spi baudrate*/
static INT
spi_baudrate_reader(void *var)
{  
    uint16 i = board_get_spi_baud();

/*
<option value="12">12Kbps</option>
<option value="50">50Kbps</option>

<option value="100">100Kbps</option>
<option value="300">300Kbps</option>
<option value="500">500Kbps</option>
<option value="1000" selected>1Mbps</option>
<option value="2000">2Mbps</option>
<option value="4200">4Mbps</option>
<option value="6250">6Mbps</option>
<option value="12500">12Mbps</option>
 */    
    //replace for the string:
    switch(i)
    {
      case 12:
      default:
         strcpy(var,"12Kbps");
         break;
      case 50:
         strcpy(var,"50Kbps");
         break;
      case 100:
         strcpy(var,"100Kbps");
         break;
      case 300:
         strcpy(var,"300Kbps");
         break;
      case 500:
         strcpy(var,"500Kbps");
         break;
      case 1000:
         strcpy(var,"1Mbps");
         break;
      case 2000:
         strcpy(var,"2Mbps");
         break;
      case 4200:
         strcpy(var,"4Mbps");
         break;
      case 6250:
         strcpy(var,"6Mbps");
         break;
      case 12500:
         strcpy(var,"12Mbps");
         break;                                                                        
    }
    
    return 1;	
}

/*spi port reader*/
static INT
spi_port_reader(void *var)
{  
    uint8 i = board_get_spi_port();
    
    //replace for the string:
    switch(i)
    {
      case 0:
      default:
         strcpy(var,"SPI0");
         break;
      case 1:
         strcpy(var,"SPI1");
         break;      
    }
    
    return 1;	
}

/*spi polarity reader*/
static INT
spi_polarity_reader(void *var)
{  
    uint8 i = board_get_spi_polarity();
    
    //replace for the string:
    switch(i)
    {
      case 0:
      default:
         strcpy(var,"High");
         break;
      case 1:
         strcpy(var,"Low");
         break;      
    }
    
    return 1;	
}

/*spi polarity reader*/
static INT
spi_phase_reader(void *var)
{  
    uint8 i = board_get_spi_phase();
    
    //replace for the string:
    switch(i)
    {
      case 0:
      default:
         strcpy(var,"Middle");
         break;
      case 1:
         strcpy(var,"Start");
         break;      
    }
    
    return 1;	
}

/*spi slave-master reader*/
static INT
spi_mode_reader(void *var)
{  
    uint8 i = board_get_spi_master();
    
    //replace for the string:
    switch(i)
    {
      case 0:
      default:
         strcpy(var,"Slave");
         break;
      case 1:
         strcpy(var,"Master");
         break;      
    }
    
    return 1;	
}

/*spi polarity reader*/
static INT
spi_interrupt_reader(void *var)
{  
    uint8 i = board_get_spi_interrupt();
    
    //replace for the string:
    switch(i)
    {
      case 0:
      default:
         strcpy(var,"Polling");
         break;
      case 1:
         strcpy(var,"Interrupt");
         break;      
    }
    
    return 1;	
}

/*tcp client-server reader*/
static INT
tcp_server_reader(void *var)
{  
    uint8 i = board_get_bridge_tcp_server();
    
    //replace for the string:
    switch(i)
    {
      case 0:
      default:
         strcpy(var,"Server");
         break;
      case 1:
         strcpy(var,"Client");
         break;      
    }
    
    return 1;	
}

/*tcp config-reader mode reader*/
static INT
tcp_config_reader(void *var)
{  
    uint8 i = board_get_bridge_configuration();
    
    //replace for the string:
    switch(i)
    {
      case 0:
      default:
         strcpy(var,"Config");         
         break;
      case 1:         
         strcpy(var,"Bridge");
         break;      
    }
    
    return 1;	
}

/*tcp output reader*/
static INT
tcp_output_reader(void *var)
{  
    uint8 i = board_get_bridge_tcp_mode();
    
    //replace for the string:
    switch(i)
    {
      case 0:
      default:
         strcpy(var,"UART");
         break;
      case 1:
         strcpy(var,"SPI");
         break;      
    }
    
    return 1;	
}

/*tcp port routines*/
static INT
tcp_port_reader(void *var)
{  
    uint16 port = board_get_bridge_tcp_port();
    
    sprintf(var,"%d",port);
   
    return 1;	
}