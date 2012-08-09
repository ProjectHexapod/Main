#ifndef _HTTP_WEB_H_
#define _HTTP_WEB_H_

/* ------------------------ Defines ---------------------------------------- */
/* The port on which we listen. */
#define HTTP_PORT                   80
#define HTTP_WORKING_SPACE         128
#define GET_FLAG                     0
#define POST_FLAG                    1

/* Priorities for the demo application tasks. */
#define HTTP_TASK_PRIORITY          ( tskIDLE_PRIORITY + 4 )
#define HTTP_TASKS_STACK_USE        1/*FSL: tasks consumption of RAM*/
#define HTTP_DYNAMIC_SUPPORT        1/*FSL: support dynamic content with SSI*/
#define HTTP_SD_CARD_SUPPORT        1/*FSL: SD card support*/
#define WEBPAGE_INDEX_LENGTH        3673

/*HTTP Options*/
#define HTTP_SESSIONS               5/*tcp sessions*/
#define HTTP_WEB_TIMEOUT          200/*default web app timeout*/
#define SDCARD_BLOCK_FEATURE        1/*used for SD support*/

/*HTTP Requests*/
#define HTTP_GET_REQUEST            "GET /"
#define HTTP_POST_REQUEST           "POST /"
#define HTTP_CNTNT_LNG_REQUEST      "Accept-Language: "

/*HTTP Responses*/
#define HTTP_HEADER_OK_PART1        "HTTP/1.1 200 OK\r\nCache-Control: no-cache\r\nContent-type: "
#define HTTP_HEADER_OK_PART2        "\r\nContent-length: "
#define HTTP_DYMAMIC_HEADER         "\r\nTransfer-Encoding: chunked\r\n"
#define HTTP_STATIC_HEADER          "HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n"
#define HTTP_DYNAMIC_HEADER         "HTTP/1.1 200 OK\r\nContent-type: text/html\r\nTransfer-Encoding: chunked\r\n"
#define HTTP_WRONG_HEADER           "HTTP/1.1 500 OK\r\nContent-type: text/html\r\nContent-length: 82\r\n\r\n"
//#define HTTP_WRONG_DATA             "\r\n57\r\n<HTML><BODY><H1>Error</H1><BR>Page doens't exist\r\n or out of memory.</BODY></HTML>\r\n0\r\n\r\n"
#define HTTP_WRONG_DATA             "<HTML><BODY><H1>Error</H1><BR>Page doens't exist\r\n or out of memory.</BODY></HTML>"
#define HTTP_TASK_STATUS_START      "<html><head><meta http-equiv=\"refresh\" content=\"2\"></head><BODY \"bgcolor=\"silver\">Running tasks:"\
                                    "<p><pre>Task          State  Priority  Stack    #<br>*****************************************<br>"
#define HTTP_TASK_STATUS_END        "\r\nFreeRTOS+lwip port (c)2009 by Freescale Semiconductor</pre></BODY></html>"

/*Web Connection Options*/
typedef enum
{
  WEB_CLOSED,
  WEB_OPEN
} web_state;

/*Web Connection*/
typedef struct
{
  void      *connection;            /*netconn pointer*/
  uint16    timeout;                /*timeout for app before closing session*/
  web_state state;                  /*session session*/
} web_session;

/* ------------------------ Prototypes ------------------------------------ */

/********************Private Functions ***************************************/

/**
 * Handle each request: timeout, close or request: HTTP 2.0 compliant
 *
 * @param connection descriptor
 * @param temporal buffer to be used for internal HTTP server
 * @return zero if session must be kept, otherwise session will be closed
 */
static uint8
HTTP_ProcessConnection( web_session *connfd_web, uint8 *space );

/**
 * Implements a HTTP GET or POST requests: send web page per request
 *   Note: no case sensitive
 *
 * @param connection descriptor
 * @param HTTP request
 * @param temporal buffer 
 * @param GET or POST request 
 * @return none
 */
static void 
HTTP_ProcessRequest(struct netconn *pcb, void *request, uint8 *temporal_buffer, uint8 flag);

#if HTTP_SD_CARD_SUPPORT
/**
 * Look for a file from SDcard
 *
 * @param connection descriptor
 * @param file's name
 * @return zero if OK, otherwise file not found
 */
static uint8
HTTP_GetFileFromSDcard(struct netconn *pcb, uint8 *array);
#endif

/**
 * Look for a file from internal flash system
 *
 * @param connection descriptor
 * @param file's name
 * @return zero if OK, otherwise file not found
 */
static uint8
HTTP_GetFileFromInternalMemory(struct netconn *pcb, uint8 *name);

/**
 * Returns Language greeting to be used for web page
 *
 * @param HTTP request to look for language string
 * @return index to language to use
 */
static uint8 
HTTP_GetLanguageIndex(void *string);

/**
 * Sends a complete web page: header and data
 *   internally select between static or dynamic processing
 *
 * @param connection descriptor
 * @param buffer to use for parsing
 * @param web page data
 * @param web page data length
 * @return none
 */
static void 
HTTP_SendWebPage(struct netconn *pcb, uint8 *array_to_send, uint8 *dynamic_info, uint16 dynamic_info_length);

/**
 * Return TRUE if file's name ends with SHTML or FSL extension, which means
 *   they need a dynamic processing
 *
 * @param file's name
 * @return none
 */
inline uint8
HTTP_IsDynamicExtension(uint8 *array_to_send);

/**
 * Send a web page header: process it for static or dynamic depending on dynamic flag
 *
 * @param connection descriptor
 * @param buffer to use for parsing
 * @param web page data length to be used for static header. NULL for dynamic
 * @param flag to select between static or dynamic data processing
 * @return none
 */
inline /*static*/ void
HTTP_SendHeader(struct netconn *pcb, uint8 *array_to_send, uint16 dynamic_info_length, uint8 dynamic_flag);

/**
 * Send a web page data: process it for static or dynamic depending on dynamic flag
 *
 * @param connection descriptor
 * @param flag to select between static or dynamic data processing
 * @param buffer to use for parsing
 * @param static data
 * @param static data length
 * @return none
 */
inline /*static*/ void
HTTP_SendData(struct netconn *pcb, uint8 dynamic_flag, uint8 *array_to_send, uint8 *dynamic_info, uint16 dynamic_info_length);

/**
 * Send a web page data replacing strings with SSI rules
 *
 * @param connection descriptor
 * @param temporal buffer for replacing
 * @param static data to be parsed with SSI rules
 * @param static data length 
 * @param send "Transfer-Encoding: chunked" footer  
 * @return none
 */
inline /*static*/ void
HTTP_SendDynamicData(struct netconn *pcb, uint8 *array_to_send, uint8 *dynamic_info, uint16 dynamic_info_length, uint8 flag);

/**
 * Send a web page with all tasks' status
 *
 * @param connection descriptor 
 * @return none
 */
static void
HTTP_ShowTasksStatus(struct netconn *pcb);

/**
 * Send a packet with "Transfer-Encoding: chunked" rules
 *
 * @param connection descriptor
 * @param data to send
 * @param data length
 * @param copy or a reference to be used for data  
 * @return none
 */
static void
HTTP_SendDynamicPacket(struct netconn *pcb, const void *data, u16_t len, u8_t apiflags);

/**
 * Send "Transfer-Encoding: chunked" footer
 *
 * @param connection descriptor
 * @return none
 */
static void
HTTP_SendDynamicFooter(struct netconn *pcb);

/**
 * Send page not found error to HTTP connection
 *
 * @param connection descriptor
 * @return none
 */
inline static void 
HTTP_SendError(struct netconn *pcb);

/********************Public Functions ***************************************/

/**
 * Start an embedded HTTP server Task: 1 client and multiple files per transfer
 *
 * @param none
 * @return none
 */
void
HTTP_Server_Task( void *pvParameters );

#endif
