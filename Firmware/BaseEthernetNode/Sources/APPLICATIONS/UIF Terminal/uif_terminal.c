/*
 * File:    uif.c
 * Purpose: Provide an interactive user interface
 *              
 * Notes:   The commands, set/show parameters, and prompt are configured 
 *          at the project level
 */

/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

#include "cf_board.h"
#include "uif_terminal.h"

#include "uart_rtos.h"
#include "adc_rtos.h"
#include "setget.h"
#include "utilities.h"

/*
 * dBUG commands
 */
UIF_CMD UIF_CMDTAB[] =
{
    UIF_CMDS_ALL
    //CPU_CMDS_ALL
} ;
const CHAR UIF_NUM_CMD = UIF_CMDTAB_SIZE;

/*
 * dBUG SET/SHOW commands
 */
UIF_SETCMD UIF_SETCMDTAB[] =
{
    UIF_SETCMDS_ALL
    //CPU_SETCMDS_ALL
} ;
const CHAR UIF_NUM_SETCMD = UIF_SETCMDTAB_SIZE;

/********************************************************************/
/*
 * Global messages -- constant strings
 */
static const CHAR PROMPT[] = "shell> ";

const CHAR HELPMSG[] =
    "Enter 'help' for help.\n\r";

const CHAR INVARG[] =
    "Error: Invalid argument: %s\n\r";

const CHAR INVALUE[] = 
    "Error: Invalid value: %s\n\r";

/*
 * Strings used by this file only
 */
static const CHAR INVCMD[] =
    "Error: No such command: %s\n\r";

static const CHAR HELPFORMAT[] = 
    "%8s  %-25s %s %s\n\r";

static const CHAR SYNTAX[] = 
    "Error: Invalid syntax for: %s\n\r";

static const CHAR INVOPT[] = 
    "Error: Invalid set/show option: %s\n\r";

static const CHAR OPTFMT[] = 
    "%12s: ";

static CHAR cmdline1 [UIF_MAX_LINE];
static CHAR cmdline2 [UIF_MAX_LINE];

/********************************************************************/

const CHAR IPFMT[] = "%d.%d.%d.%d\n";
const CHAR SETERR3[] = "Error: Invalid IP address: %s\n";

/********************************************************************/

/*FSL:printf prototype*/
INT
printf (const CHAR *fmt, ...);

/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/

/********************************************************************/
void
uif_setethaddr (INT argc, CHAR **argv)
{
    /*
     * This function sets or shows the Ethernet Address
     * assigned to this board.  The address is contained in
     * ROM memory.
     */
    uint8 ethaddr[6];
    uint8 i;

    (void)argc;

    if (argv[2] == NULL)
    {
        board_get_eth_ethaddr (ethaddr);        
        for (i = 0; i < 6; i++)
        {
            if (i != 5)
            {
                printf("%02X:",ethaddr[i]);
            }
            else
            {
                printf("%02X\n",ethaddr[i]);
            }
        }
        return;
    }

    if (parse_ethaddr(argv[2],ethaddr))
    {
        board_set_eth_ethaddr (ethaddr);
    }
    else
    {
        printf("Error: Invalid Ethernet Address:  %s\n", argv[2]);
    }
}

void 
uif_setbaud_server (INT argc, CHAR **argv)
{    
    INT success, baud;

    /*get part*/
    if (argc != 3)
    {
        printf("%d\n",board_get_uart_baud());
        return;
    }
    /*set part*/
    baud =  get_value(argv[2], &success, 10);
    switch (baud)
    {
        /*validation data*/
        case 300:
        case 600:
        case 1200:
        case 2400:
        case 4800:
        case 9600:
        case 19200:
        case 38400:
        case 57600:
        case 115200:
            board_set_uart_baud(baud);
            break;
        default:
            printf(INVARG,argv[2]);
            break;
    }  
}

/********************************************************************/
void
uif_setcmd_ipadd (INT argc, CHAR **argv)
{
    T32_8 ip;   /* IP address */

    (void)argc;

    if (argv[2] == NULL)
    {
        ip.lword = board_get_eth_ip_add();
        printf(IPFMT,
            ip.bytes[0],
            ip.bytes[1],
            ip.bytes[2],
            ip.bytes[3]);
        return;
    }
    if (!ip_convert_address((CHAR *)argv[2],(CHAR *)ip.bytes))
    {
        printf(SETERR3,argv[2]);
        return;
    }
    board_set_eth_ip_add(ip.lword);
}

/********************************************************************/
void
uif_setcmd_serveradd (INT argc, CHAR **argv)
{
    T32_8 ip;   /* IP address */

    (void)argc;

    if (argv[2] == NULL)
    {
        ip.lword = board_get_eth_server_add();
        printf(IPFMT,
            ip.bytes[0],
            ip.bytes[1],
            ip.bytes[2],
            ip.bytes[3]);
        return;
    }
    if (!ip_convert_address((CHAR *)argv[2],(CHAR *)ip.bytes))
    {
        printf(SETERR3,argv[2]);
        return;
    }
    board_set_eth_server_add(ip.lword);
}

/********************************************************************/
void
uif_setcmd_gateway (INT argc, CHAR **argv)
{
    T32_8 ip;   /* IP address */

    (void)argc;

    if (argv[2] == NULL)
    {
        ip.lword = board_get_eth_gateway();
        printf(IPFMT,
            ip.bytes[0],
            ip.bytes[1],
            ip.bytes[2],
            ip.bytes[3]);
        return;
    }
    if (!ip_convert_address((CHAR *)argv[2],(CHAR *)ip.bytes))
    {
        printf(SETERR3,argv[2]);
        return;
    }
    board_set_eth_gateway(ip.lword);
}

/********************************************************************/
void
uif_setcmd_netmask (INT argc, CHAR **argv)
{
    T32_8 ip;   /* IP address */

    (void)argc;

    if (argv[2] == NULL)
    {
        ip.lword = board_get_eth_netmask();
        printf(IPFMT,
            ip.bytes[0],
            ip.bytes[1],
            ip.bytes[2],
            ip.bytes[3]);
        return;
    }
    if (!ip_convert_address((CHAR *)argv[2],(CHAR *)ip.bytes))
    {
        printf(SETERR3,argv[2]);
        return;
    }
    board_set_eth_netmask(ip.lword);
}

/********************************************************************/
void
uif_setcmd_username (INT argc, CHAR **argv)
{
    CHAR fn[STRING_SIZE];

    (void)argc;

    if (argv[2] == NULL)
    {
        board_get_email_username(fn);
        printf("%s\n",fn);
        return;
    }
    board_set_email_username(argv[2]);
}

/********************************************************************/
void
uif_setcmd_password (INT argc, CHAR **argv)
{
    CHAR fn[STRING_SIZE];

    (void)argc;

    if (argv[2] == NULL)
    {
        board_get_email_password(fn);
        printf("%s\n",fn);
        return;
    }
    board_set_email_password(argv[2]);
}

/********************************************************************/
void
uif_setcmd_smtpserver (INT argc, CHAR **argv)
{
    CHAR fn[STRING_SIZE];

    (void)argc;

    if (argv[2] == NULL)
    {
        board_get_email_smtp_server(fn);
        printf("%s\n",fn);
        return;
    }
    board_set_email_smtp_server(argv[2]);
}

/********************************************************************/
void
uif_setcmd_email_authentication (INT argc, CHAR **argv)
{
    INT success, answer;

    /*get part*/
    if (argc != 3)
    {
        printf("%d\n",(uint8)board_get_email_authentication_required());
        return;
    }
    /*set part*/
    answer =  get_value(argv[2], &success, 10);
    
    board_set_email_authentication_required(answer);  
}
/********************************************************************/
/********************************************************************/
/********************************************************************/
/********************************************************************/
CHAR *
get_line (CHAR *line)
{
    INT pos;
    INT ch;

    pos = 0;
    ch = (INT)in_char();
    while ( (ch != 0x0D /* CR */) &&
            (ch != 0x0A /* LF/NL */) &&
            (pos < UIF_MAX_LINE))
    {
        switch (ch)
        {
            case 0x08:      /* Backspace */
            case 0x7F:      /* Delete */
                if (pos > 0)
                {
                    pos -= 1;
                    out_char(0x08);    /* backspace */
                    out_char(' ');
                    out_char(0x08);    /* backspace */
                }
                break;
            default:
                if ((pos+1) < UIF_MAX_LINE)
                {
                    if ((ch > 0x1f) && (ch < 0x80))
                    {
                        line[pos++] = (CHAR)ch;
                        out_char((CHAR)ch);
                    }
                }
                break;
        }
        ch = (INT)in_char();
    }
    line[pos] = '\0';
    out_char(0x0D);    /* CR */
    out_char(0x0A);    /* LF */

    return line;
}

/********************************************************************/
INT
make_argv (CHAR *cmdline, CHAR *argv[])
{
    INT argc, i, in_text;

    /* 
     * Break cmdline into strings and argv
     * It is permissible for argv to be NULL, in which case
     * the purpose of this routine becomes to count args
     */
    argc = 0;
    i = 0;
    in_text = FALSE;
    while (cmdline[i] != '\0')  /* getline() must place 0x00 on end */
    {
        if (((cmdline[i] == ' ')   ||
             (cmdline[i] == '\t')) )
        {
            if (in_text)
            {
                /* end of command line argument */
                cmdline[i] = '\0';
                in_text = FALSE;
            }
            else
            {
                /* still looking for next argument */
                
            }
        }
        else
        {
            /* got non-whitespace character */
            if (in_text)
            {
            }
            else
            {
                /* start of an argument */
                in_text = TRUE;
                if (argc < UIF_MAX_ARGS)
                {
                    if (argv != NULL)
                        argv[argc] = &cmdline[i];
                    argc++;
                }
                else
                    /*return argc;*/
                    break;
            }

        }
        i++;    /* proceed to next character */
    }
    if (argv != NULL)
        argv[argc] = NULL;
    return argc;
}

/********************************************************************/
void
run_cmd (void)
{
    /*
     * Global array of pointers to emulate C argc,argv interface
     */
    INT argc;
    CHAR *argv[UIF_MAX_ARGS + 1];   /* one extra for null terminator */

    get_line(cmdline1);

    if (!(argc = make_argv(cmdline1,argv)))
    {
        /* no command entered, just a blank line */
        strcpy(cmdline1,cmdline2);
        argc = make_argv(cmdline1,argv);
    }
    cmdline2[0] = '\0';

    if (argc)
    {
        INT i;
        for (i = 0; i < UIF_NUM_CMD; i++)
        {
            if (strcasecmp(UIF_CMDTAB[i].cmd,argv[0]) == 0)
            {
                if (((argc-1) >= UIF_CMDTAB[i].min_args) &&
                    ((argc-1) <= UIF_CMDTAB[i].max_args))
                {
                    if (UIF_CMDTAB[i].flags & UIF_CMD_FLAG_REPEAT)
                    {
                        strcpy(cmdline2,argv[0]);
                    }
                    UIF_CMDTAB[i].func(argc,argv);
                    return;
                }
                else
                {
                    printf(SYNTAX,argv[0]);
                    return;
                }
            }
        }
        printf(INVCMD,argv[0]);
        printf(HELPMSG);
    }
}
/********************************************************************/
uint32
get_value (CHAR *s, INT *success, INT base)
{
	uint32 value;
	CHAR *p;

	value = strtoul(s,&p,base);
	if ((value == 0) && (p == s))
	{
		*success = FALSE;
		return 0;
	}
	else
	{
		*success = TRUE;
		return value;
	}
}
/********************************************************************/
void
uif_cmd_help (INT argc, CHAR **argv)
{
	INT index;
	
	(void)argc;
	(void)argv;
	
	printf("\n");
	for (index = 0; index < UIF_NUM_CMD; index++)
	{
		printf(HELPFORMAT,
			UIF_CMDTAB[index].cmd,
			UIF_CMDTAB[index].description,
			UIF_CMDTAB[index].cmd,
			UIF_CMDTAB[index].syntax);
	}
	printf("\n");
}
/********************************************************************/
void
uif_cmd_set (INT argc, CHAR **argv)
{
    INT index;

	  printf("\n");
    if (argc == 1)
    {
        printf("Valid 'set' options:\n");
        for (index = 0; index < UIF_NUM_SETCMD; ++index)
        {
            printf(OPTFMT,UIF_SETCMDTAB[index].option);
            printf("%s\n",UIF_SETCMDTAB[index].syntax);
        }
     	  printf("\n");
        return;
    }

    if (argc != 3)
    {
        printf("Error: Invalid argument list\n");
        return;
    }

    for (index = 0; index < UIF_NUM_SETCMD; index++)
    {
        if (strcasecmp(UIF_SETCMDTAB[index].option,argv[1]) == 0)
        {
            if (((argc-1-1) >= UIF_SETCMDTAB[index].min_args) &&
                ((argc-1-1) <= UIF_SETCMDTAB[index].max_args))
            {
                UIF_SETCMDTAB[index].func(argc,argv);
                return;
            }
            else
            {
                printf(INVARG,argv[1]);
                return;
            }
        }
    }
    printf(INVOPT,argv[1]);
}

/********************************************************************/
void
uif_cmd_show (INT argc, CHAR **argv)
{
    INT index;

	  printf("\n");
    if (argc == 1)
    {
        /*
         * Show all Option settings
         */
        argc = 2;
        argv[2] = NULL;
        for (index = 0; index < UIF_NUM_SETCMD; index++)
        {
            printf(OPTFMT,UIF_SETCMDTAB[index].option);
            UIF_SETCMDTAB[index].func(argc,argv);
         	  printf("\n");
        }
     	  printf("\n");
        return;
    }

    for (index = 0; index < UIF_NUM_SETCMD; index++)
    {
        if (strcasecmp(UIF_SETCMDTAB[index].option,argv[1]) == 0)
        {
            if (((argc-1-1) >= UIF_SETCMDTAB[index].min_args) &&
                ((argc-1-1) <= UIF_SETCMDTAB[index].max_args))
            {
                printf(OPTFMT,UIF_SETCMDTAB[index].option);
                UIF_SETCMDTAB[index].func(argc,argv);
             	  printf("\n\n");
                return;
            }
            else
            {
                printf(INVARG,argv[1]);
                return;
            }
        }
    }
    printf(INVOPT,argv[1]);
}

/********************************************************************/

/*FSL: running task*/
void
vBasicSerialTerminal( void *pvParameters )
{    
    /*Handle for UART capabilities*/
    xComPortHandle handle_printf;
    
    //xADCPortHandle adc_handle;

    /* Parameters are not used - suppress compiler error */
    ( void )pvParameters;

    /**********************FSL: serial start-up*******************************/
    
    //if handle NULL, serial cannot be used!!!
    handle_printf = xUARTinit((eCOMPort)board_get_uart_port()/*serCOM1*/, 
                             (eBaud)board_get_uart_baud()/*ser19200*/, 
                             (eParity)board_get_uart_parity()/*serNO_PARITY*/, 
                             (eDataBits)board_get_uart_number_of_bits()/*serBITS_8*/, 
                             (eStopBits)board_get_uart_stop_bits()/*serSTOP_1*/,
                             (eFlowControl)board_get_uart_flow_control()/*serFlowControlXONXOFF*/,
                             serSemaphoreOFF,/*Semaphore OFF*/ 
                             PRINTF_BUFFER_LIMIT/*defined at header file*/);

    //adc_handle = xADCInit((adcBits)adcEightBits);
    
    //xADCchannelInit((eADCchannel)ADC_CHANNEL);

    set_printf_handle(handle_printf);

    /* Loop forever */
    for( ;; )
    {	       
       /*This will run forever and ever*/
        printf(PROMPT);
        //printf("%d\n\r",ADC_start_get_single_conversion(ADC_CHANNEL));
        run_cmd();
    }
        
    return;/*FSL:never get here!!*/
}
