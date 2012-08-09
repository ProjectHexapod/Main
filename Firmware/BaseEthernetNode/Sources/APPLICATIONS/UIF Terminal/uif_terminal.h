/*
 * File:    uif.h
 * Purpose: Provide an interactive user interface
 *              
 * Notes:   The commands, set/show parameters, and prompt are configured 
 *          at the project level
 */

#ifndef _UIF_H_
#define _UIF_H_

/********************************************************************/

#define PRINTF_BUFFER_LIMIT       50
#define TERMINAL_TASK_PRIORITY    1
/*
 * Function prototypes
 */
CHAR *
get_line (CHAR *);

uint32
get_value (CHAR *, INT *, INT);

void
run_cmd (void);

INT
make_argv (CHAR *, CHAR **);

void
uif_cmd_help (INT, CHAR **);

void
uif_cmd_set (INT, CHAR **);

void
uif_cmd_show (INT, CHAR **);

/********************************************************************/

void 
uif_setbaud_server(INT, CHAR **);

void
uif_setethaddr (INT argc, CHAR **argv);

void
uif_setcmd_ipadd (INT argc, CHAR **argv);

void
uif_setcmd_serveradd (INT argc, CHAR **argv);

void
uif_setcmd_gateway (INT argc, CHAR **argv);

void
uif_setcmd_netmask (INT argc, CHAR **argv);

void
uif_setcmd_username (INT argc, CHAR **argv);

void
uif_setcmd_password (INT argc, CHAR **argv);

void
uif_setcmd_smtpserver (INT argc, CHAR **argv);

void
uif_setcmd_email_authentication (INT argc, CHAR **argv);
/********************************************************************/

void
vBasicSerialTerminal( void *pvParameters );

/*
 * Maximum command line arguments
 */
#define UIF_MAX_ARGS	10

/*
 * Maximum length of the command line
 */
#define UIF_MAX_LINE	80

/*
 * The command table entry data structure
 */
typedef const struct
{
    CHAR *  cmd;                    /* command name user types, ie. GO  */
    INT     min_args;               /* min num of args command accepts  */
    INT     max_args;               /* max num of args command accepts  */
    INT     flags;                  /* command flags (e.g. repeat)      */
    void    (*func)(INT, CHAR **);  /* actual function to call          */
    CHAR *  description;            /* brief description of command     */
    CHAR *  syntax;                 /* syntax of command                */
} UIF_CMD;

/*
 * Prototype and macro for size of the command table
 */
extern UIF_CMD UIF_CMDTAB[];
extern const CHAR UIF_NUM_CMD;
#define UIF_CMDTAB_SIZE             (sizeof(UIF_CMDTAB)/sizeof(UIF_CMD))

#define UIF_CMD_FLAG_REPEAT         0x1

/*
 * Macros for User InterFace command table entries
 */
#ifndef UIF_CMD_HELP
#define UIF_CMD_HELP    \
    {"help",0,1,0,uif_cmd_help,"Help","<cmd>"},
#endif

#ifndef UIF_CMD_SET
#define UIF_CMD_SET \
    {"set",0,2,0,uif_cmd_set,"Set Config","<option value>"},
#endif

#ifndef UIF_CMD_SHOW
#define UIF_CMD_SHOW    \
    {"show",0,1,0,uif_cmd_show,"Show Config","<option>"},
#endif

/*
 * Macro to include all standard user interface commands
 */
#define UIF_CMDS_ALL    \
    UIF_CMD_HELP        \
    UIF_CMD_SET         \
    UIF_CMD_SHOW

/*
 * The set/show table entry data structure
 */
typedef const struct
{
    CHAR *  option;
    INT     min_args;
    INT     max_args;
    void    (*func)(INT, CHAR **);
    CHAR *  syntax;
} UIF_SETCMD;

/********************************************************************/

/*
 * Macro to include dBUG SET/SHOW commands
 */
#define UIF_SETCMDS_ALL     \
    UIF_SETCMD_BAUD,        \
    UIF_SETCMD_MAC,         \
    UIF_SETCMD_IP,          \
    UIF_SETCMD_SERVER,      \
    UIF_SETCMD_NETMASK,     \
    UIF_SETCMD_GATEWAY,     \
    UIF_SETCMD_USERNAME,    \
    UIF_SETCMD_PASSWORD,    \
    UIF_SETCMD_SMTPSERVER,  \
    UIF_SETCMD_EMAILAUTHENTICATION
         

/********************************************************************/

/*
 * Macros for SET/SHOW command table entries
 */
#ifndef UIF_SETCMD_BAUD
#define UIF_SETCMD_BAUD     \
    {"baud",0,1,uif_setbaud_server,"<9600|19200|115200>"}
#endif

#ifndef UIF_SETCMD_MAC
#define UIF_SETCMD_MAC     \
    {"mac",0,1,uif_setethaddr,"<FF:FF:FF:FF:FF:FF>"}
#endif


#ifndef UIF_SETCMD_IP
#define UIF_SETCMD_IP     \
    {"ip",0,1,uif_setcmd_ipadd,"<board IP>"}
#endif

#ifndef UIF_SETCMD_SERVER
#define UIF_SETCMD_SERVER     \
    {"server",0,1,uif_setcmd_serveradd,"<host IP>"}
#endif

#ifndef UIF_SETCMD_NETMASK
#define UIF_SETCMD_NETMASK     \
    {"netmask",0,1,uif_setcmd_netmask,"<netmask>"}
#endif

#ifndef UIF_SETCMD_GATEWAY
#define UIF_SETCMD_GATEWAY     \
    {"gateway",0,1,uif_setcmd_gateway,"<gateway IP>"}
#endif

#ifndef UIF_SETCMD_USERNAME
#define UIF_SETCMD_USERNAME     \
    {"username",0,1,uif_setcmd_username,"Email User"}
#endif

#ifndef UIF_SETCMD_PASSWORD
#define UIF_SETCMD_PASSWORD     \
    {"password",0,1,uif_setcmd_password,"Email Password"}
#endif

#ifndef UIF_SETCMD_SMTPSERVER
#define UIF_SETCMD_SMTPSERVER     \
    {"smtp",0,1,uif_setcmd_smtpserver,"Email SMTP server"}
#endif

#ifndef UIF_SETCMD_EMAILAUTHENTICATION
#define UIF_SETCMD_EMAILAUTHENTICATION     \
    {"auth",0,1,uif_setcmd_email_authentication,"1/0"}
#endif
/*
 * Prototype and macro for size of the table
 */
extern UIF_SETCMD UIF_SETCMDTAB[];
extern const CHAR UIF_NUM_SETCMD;
#define UIF_SETCMDTAB_SIZE      (sizeof(UIF_SETCMDTAB)/sizeof(UIF_SETCMD))

/*
 * Define ON and OFF for use by set/show commands
 */
#ifndef ON
#define ON      1
#endif

#ifndef OFF
#define OFF     0
#endif

/*
 * Strings defined in uif.c that may be useful to external functions
 */
extern const CHAR HELPMSG[];
extern const CHAR INVARG[];
extern const CHAR INVALUE[];

/********************************************************************/

#endif /* _UIF_H_ */
