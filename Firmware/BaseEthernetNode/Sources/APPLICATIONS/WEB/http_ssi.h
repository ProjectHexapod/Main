#ifndef WEB_SSI_H
#define WEB_SSI_H

#include "cf_board.h"

#define SSI_START         "<!--#echo var=\""
#define SSI_END           "\"-->"

#define MAC_ADDRESS_STRING "%02X.%02X.%02X.%02X.%02X.%02X"
#define IP_ADDRESS_STRING  "%d.%d.%d.%d"

/*
 * The command table entry data structure
 */
typedef const struct
{
    CHAR *  command;                /* SSI string to replace  */
    INT    (*func)(void *);         /* actual function to call */
} SSI_CMD;

typedef const struct
{
    CHAR *  language;
    CHAR *  language_code;
} LANGUAGES;

/*inline */uint8 
max_number_of_languages();

/*FSL: external functions*/
extern INT adc_channel0(void *var);
extern INT adc_channel1(void *var);
extern INT adc_channel2(void *var);
extern INT html_counter(void *var);
extern INT language_greeting(void *var);
extern INT baudrate_reader(void *var);
extern INT flowcontrol_reader(void *var);
extern INT serialport_reader(void *var);
extern INT serialparity_reader(void *var);
extern INT serialbits_reader(void *var);
extern INT serialstopbits_reader(void *var);
extern INT mac_macaddress_reader(void *var);
/*IP address replacing routines*/
extern  INT mac_ipaddress_reader(void *var);
/*IP Mask address replacing routines*/
extern  INT mac_ipmkaddress_reader(void *var);
/*IP Gateway address replacing routines*/
extern  INT mac_ipgwaddress_reader(void *var);

/*IP Server address replacing routines*/
extern  INT mac_ipserveraddress_reader(void *var);
/*mac address type*/
extern  INT mac_static_reader(void *var);
/*spi baudrate*/
extern  INT spi_baudrate_reader(void *var);
/*spi port reader*/
extern  INT spi_port_reader(void *var);
/*spi polarity reader*/
extern  INT spi_polarity_reader(void *var);

/*spi polarity reader*/
extern  INT spi_phase_reader(void *var);
/*spi polarity reader*/
extern  INT spi_mode_reader(void *var);
/*spi polarity reader*/
static INT spi_interrupt_reader(void *var);
/*tcp client-server reader*/
extern  INT tcp_server_reader(void *var);

/*tcp config-reader mode reader*/
extern  INT tcp_config_reader(void *var);
/*tcp output reader*/
extern  INT tcp_output_reader(void *var);
/*tcp port routines*/
extern  INT tcp_port_reader(void *var);
/*
 * Macros for User InterFace command table entries
 */

#ifndef SSI_CMD_CHANNEL0
#define SSI_CMD_CHANNEL0    \
    {"CHANNEL0",adc_channel0}
#endif

#ifndef SSI_CMD_CHANNEL1
#define SSI_CMD_CHANNEL1    \
    {"CHANNEL1",adc_channel1}
#endif

#ifndef SSI_CMD_CHANNEL2
#define SSI_CMD_CHANNEL2    \
    {"CHANNEL2",adc_channel2}
#endif

#ifndef SSI_CMD_COUNTER
#define SSI_CMD_COUNTER     \
    {"COUNTER",html_counter}
#endif

#ifndef SSI_CMD_GREETING
#define SSI_CMD_GREETING     \
    {"GREETING",language_greeting}
#endif

#ifndef SSI_CMD_BAUDRATE
#define SSI_CMD_BAUDRATE     \
    {"BAUD",baudrate_reader}
#endif

#ifndef SSI_CMD_FLOWCONTROL
#define SSI_CMD_FLOWCONTROL     \
    {"FLOW",flowcontrol_reader}
#endif
  
#ifndef SSI_CMD_SERIALPORT
#define SSI_CMD_SERIALPORT     \
    {"PORT",serialport_reader}
#endif  

#ifndef SSI_CMD_SERIALPARI
#define SSI_CMD_SERIALPARI     \
    {"PARI",serialparity_reader}
#endif

#ifndef SSI_CMD_SERIALBITS
#define SSI_CMD_SERIALBITS     \
    {"BITS",serialbits_reader}
#endif

#ifndef SSI_CMD_SERIALSTOP
#define SSI_CMD_SERIALSTOP     \
    {"STOP",serialstopbits_reader}
#endif

#ifndef SSI_CMD_MACADD
#define SSI_CMD_MACADD     \
    {"MACADD",mac_macaddress_reader}
#endif

#ifndef SSI_CMD_MACIPADD
#define SSI_CMD_MACIPADD     \
    {"MACIPADD",mac_ipaddress_reader}
#endif

#ifndef SSI_CMD_MACGWADD
#define SSI_CMD_MACGWADD     \
    {"MACGWADD",mac_ipgwaddress_reader}
#endif

#ifndef SSI_CMD_MACMKADD
#define SSI_CMD_MACMKADD     \
    {"MACMKADD",mac_ipmkaddress_reader}
#endif

#ifndef SSI_CMD_MACSAADD
#define SSI_CMD_MACSAADD     \
    {"MACSAADD",mac_ipserveraddress_reader}
#endif

#ifndef SSI_CMD_MACSTAT
#define SSI_CMD_MACSTAT     \
    {"MACSTAT",mac_static_reader}
#endif

#ifndef SSI_CMD_TCPPORT
#define SSI_CMD_TCPPORT     \
    {"TCPPORT",tcp_port_reader}
#endif

#ifndef SSI_CMD_TCPSER
#define SSI_CMD_TCPSER     \
    {"TCPSER",tcp_server_reader}
#endif

#ifndef SSI_CMD_TCPCONF
#define SSI_CMD_TCPCONF     \
    {"TCPCONF",tcp_config_reader}
#endif

#ifndef SSI_CMD_TCPOUT
#define SSI_CMD_TCPOUT     \
    {"TCPOUT",tcp_output_reader}
#endif

#ifndef SSI_CMD_SPIPORT
#define SSI_CMD_SPIPORT     \
    {"SPIPORT",spi_port_reader}
#endif

#ifndef SSI_CMD_SPIBAUD
#define SSI_CMD_SPIBAUD     \
    {"SPIBAUD",spi_baudrate_reader}
#endif

#ifndef SSI_CMD_SPIPOLA
#define SSI_CMD_SPIPOLA     \
    {"SPIPOLA",spi_polarity_reader}
#endif

#ifndef SSI_CMD_SPIPHASE
#define SSI_CMD_SPIPHASE     \
    {"SPIPHASE",spi_phase_reader}
#endif

#ifndef SSI_CMD_SPIMAS
#define SSI_CMD_SPIMAS     \
    {"SPIMAS",spi_mode_reader}
#endif

#ifndef SSI_CMD_SPIINT
#define SSI_CMD_SPIINT     \
    {"SPIINT",spi_interrupt_reader}
#endif

#define SSI_MAX_COMMANDS       		sizeof(SSI_CMD_ARRAY)/sizeof(SSI_CMD )

//languages
#define GREETING_ENGLISH        "Hello!!"
#define GREETING_FRENCH    		  "Salut!!"
#define GREETING_DEUTCH         "Hallo!!"
#define GREETING_CHINESSE       "China"
#define GREETING_ITALIAN        "Chau!!"
#define GREETING_RUSSIAN        "Russia"
#define GREETING_JAPANESE       "Japan"
#define GREETING_ARABIC         "Arabic"
#define GREETING_TAIWAN         "Taiwan"
#define GREETING_PORTUGAL       "Portugal"
#define GREETING_POLISH         "Polish"
#define GREETING_SPANISH        "Hola!!"
#define GREETING_KOREAN         "Korean"

//language codes
#define GREETING_ENGLISH_CODE   "en"
#define GREETING_FRENCH_CODE    "fr"
#define GREETING_DEUTCH_CODE    "de"
#define GREETING_CHINESSE_CODE  "zh"
#define GREETING_ITALIAN_CODE   "it"
#define GREETING_RUSSIAN_CODE   "ru"
#define GREETING_JAPANESE_CODE  "ja"
#define GREETING_ARABIC_CODE    "ar"
#define GREETING_TAIWAN_CODE    "tw"
#define GREETING_PORTUGAL_CODE  "pt"
#define GREETING_POLISH_CODE    "pl"
#define GREETING_SPANISH_CODE   "es"
#define GREETING_KOREAN_CODE    "ko"

#define GREETING_LANGUAGE_CODE_LENGTH  sizeof(GREETING_ENGLISH_CODE)-1

//language structs
#ifndef ENGLISH_OPTION
#define ENGLISH_OPTION    \
    {GREETING_ENGLISH,GREETING_ENGLISH_CODE}
#endif
#ifndef FRENCH_OPTION
#define FRENCH_OPTION    \
    {GREETING_FRENCH,GREETING_FRENCH_CODE}
#endif
#ifndef DEUTCH_OPTION
#define DEUTCH_OPTION    \
    {GREETING_DEUTCH,GREETING_DEUTCH_CODE}
#endif
#ifndef CHINESSE_OPTION
#define CHINESSE_OPTION    \
    {GREETING_CHINESSE,GREETING_CHINESSE_CODE}
#endif
#ifndef ITALIAN_OPTION
#define ITALIAN_OPTION    \
    {GREETING_ITALIAN,GREETING_ITALIAN_CODE}
#endif
#ifndef RUSSIAN_OPTION
#define RUSSIAN_OPTION    \
    {GREETING_RUSSIAN,GREETING_RUSSIAN_CODE}
#endif
#ifndef JAPANESE_OPTION
#define JAPANESE_OPTION    \
    {GREETING_JAPANESE,GREETING_JAPANESE_CODE}
#endif
#ifndef ARABIC_OPTION
#define ARABIC_OPTION    \
    {GREETING_ARABIC,GREETING_ARABIC_CODE}
#endif
#ifndef TAIWAN_OPTION
#define TAIWAN_OPTION    \
    {GREETING_TAIWAN,GREETING_TAIWAN_CODE}
#endif
#ifndef PORTUGAL_OPTION
#define PORTUGAL_OPTION    \
    {GREETING_PORTUGAL,GREETING_PORTUGAL_CODE}
#endif
#ifndef POLISH_OPTION
#define POLISH_OPTION    \
    {GREETING_POLISH,GREETING_POLISH_CODE}
#endif
#ifndef SPANISH_OPTION
#define SPANISH_OPTION    \
    {GREETING_SPANISH,GREETING_SPANISH_CODE}
#endif
#ifndef KOREAN_OPTION
#define KOREAN_OPTION    \
    {GREETING_KOREAN,GREETING_KOREAN_CODE}
#endif

#ifndef MAX_LANGUAGES
  #define MAX_LANGUAGES        sizeof(WEB_LANGUAGES)/sizeof(LANGUAGES)
#endif

/*FSL:prototypes*/
/**
 * Implements a SSI Replacement
 *
 * @param array to replace
 * @param replaced array 
 * @return returned value by function linked to array to replace
 */
uint8 
SSI_parser(uint8 *input, uint8 *output);

#endif
