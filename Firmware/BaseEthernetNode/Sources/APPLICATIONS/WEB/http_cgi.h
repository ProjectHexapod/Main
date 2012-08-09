#ifndef WEB_CGI_H
#define WEB_CGI_H

#include "cf_board.h"

/*
 * The command table entry data structure
 */
typedef const struct
{
    CHAR *  command;                /* CGI string id  */
    INT    (*func)(CHAR *, void *); /* actual function to call */
} CGI_CMD;

/*FSL:prototypes*/

/*FSL: extern functions*/

extern INT 
uart_configuration_process(CHAR *name, void *request);

extern INT 
reset_configuration_process(CHAR *name, void *request);

extern INT 
spi_configuration_process(CHAR *name, void *request);

extern INT 
mac_configuration_process(CHAR *name, void *request);

extern INT 
tcp_configuration_process(CHAR *name, void *request);

/*
 * Macros for User InterFace command table entries
 */

#ifndef CGI_UART_CONFIGURATION
#define CGI_UART_CONFIGURATION    \
    {"uart.cgi",uart_configuration_process}
#endif

#ifndef CGI_SPI_CONFIGURATION
#define CGI_SPI_CONFIGURATION    \
    {"spi.cgi",spi_configuration_process}
#endif

#ifndef CGI_MAC_CONFIGURATION
#define CGI_MAC_CONFIGURATION    \
    {"mac.cgi",mac_configuration_process}
#endif

#ifndef CGI_TCP_CONFIGURATION
#define CGI_TCP_CONFIGURATION    \
    {"tcp.cgi",tcp_configuration_process}
#endif

#ifndef CGI_RESET_CONFIGURATION
#define CGI_RESET_CONFIGURATION    \
    {"reset.cgi",reset_configuration_process}
#endif

#define CGI_MAX_COMMANDS       		sizeof(CGI_CMD_ARRAY)/sizeof(CGI_CMD )

/**
 * Implements a CGI call
 *
 * @param CGI name
 * @param argument to be used for CGI called function 
 * @return returned value by function linked to execute by POST request
 */
uint8 
CGI_parser(int8 *name, void *request);

#endif