#ifndef _UTILITIES_H_
#define _UTILITIES_H_

/*FSL: flag used to request a memalloc inside netconn_rcv_req(...)*/
#define NETCONN_RCV_NETBUFFER         1
#define IP_DELIMITATOR                '.'
#define MAC_DELIMITATOR               IP_DELIMITATOR/*':'*/
#define STRING_END                    "\r\n"
#define STRING_DOUBLE_END             "\r\n\r\n"

#define str_len(x)        sizeof(x)-1

/*FSL: Stack space neede by each Task*/
#define WEBSERVER_STACK_SPACE		  160//OK
#define UART_BRIDGE_STACK_SPACE   144//OK
#define SPI_BRIDGE_STACK_SPACE    144//??
#define DHCP_STACK_SPACE          112//OK
#define LED_STACK_SPACE            32//NO
#define EMAILCLIENT_STACK_SPACE		 96//OK
#define SRL_BRIDGE_BUFFER_LIMIT    96//???
#define TERMINAL_STACK_SPACE      144//OK
#define SDCARD_STACK_SPACE        224//???
#define FTPSERVER_STACK_SPACE     144//OK

/*MIME Media Types*/
#define CONTENT_HTML      "text/html"                 /*HTM, HTML, SHTML*/
#define CONTENT_CSS       "text/css"                  /*CSS*/
#define CONTENT_TEXT      "text/plain"                /*TXT, FSL*/
#define CONTENT_JPG       "image/jpeg"                /*JPG, JPEG*/
#define CONTENT_GIF       "image/gif"                 /*GIF*/
#define CONTENT_BMP       "image/bmp"                 /*BMP*/
#define CONTENT_UNKNOWN   "application/octet-stream"  /*unknown MIME type*/

typedef const struct
{
    CHAR *  mime_extension;
    CHAR *  mime_type;
} MIME_TYPE;

/*
 * Macros for MIME Types
 */
#ifndef MIME_TYPE_HTM
#define MIME_TYPE_HTM    \
    {".HTM",CONTENT_HTML}
#endif

#ifndef MIME_TYPE_SHTML
#define MIME_TYPE_SHTML    \
    {".SHTML",CONTENT_HTML}
#endif

#ifndef MIME_TYPE_CSS
#define MIME_TYPE_CSS    \
    {".CSS",CONTENT_CSS}
#endif

#ifndef MIME_TYPE_TXT
#define MIME_TYPE_TXT    \
    {".TXT",CONTENT_TEXT}
#endif

#ifndef MIME_TYPE_FSL
#define MIME_TYPE_FSL    \
    {".FSL",CONTENT_TEXT}
#endif

#ifndef MIME_TYPE_JPG
#define MIME_TYPE_JPG    \
    {".JPG",CONTENT_JPG}
#endif

#ifndef MIME_TYPE_JPEG
#define MIME_TYPE_JPEG    \
    {".JPEG",CONTENT_JPG}
#endif

#ifndef MIME_TYPE_GIF
#define MIME_TYPE_GIF    \
    {".GIF",CONTENT_GIF}
#endif

#ifndef MIME_TYPE_BMP
#define MIME_TYPE_BMP    \
    {".BMP",CONTENT_BMP}
#endif  

#define MIME_MAX_TYPES       		sizeof(MIME_TYPE_ARRAY)/sizeof(MIME_TYPE )

/**
 * Receives tcp/udp information copying to a static
 *  array or use network buffer directly depending on flag var
 *  Info is received thru tcp/udp/raw connection descriptor
 *  Features: reentrant
 *
 * @param connection descriptor
 * @param static array to be used to copy network buffers
 * @param selector from apps array or use directly from lwIP network buffers
 * @param network buffer pointer of pointer
 * @return length of buffer. Read conn->err for details: 
 *    OK, (ERR_OK) CLSD (ERR_CLSD), TIMEOUT (ERR_TIMEOUT), OUT OF MEM (ERR_MEM)
 */
uint16 
netconn_rcv_req(void *connec, uint8 *alloc_rq, void **nbuffer, uint8 flag);

/**
 * Set timeout for selected connection. Call it after netconn_listen(...)
 *   for client or netconn_new(...) for server
 *
 * @param connection descriptor
 * @param wait time for connection until is time out'ed
 * @return none
 */
void 
netconn_set_timeout(void *connec, INT timeout);

/**
 * Returns MIME type depending on file extension
 *
 * @param file's name
 * @return pointer to MIME type
 */
uint8 *
MIME_GetMediaType(uint8 *array_to_send);

/*
** base64_encodeblock
**
** encode 3 8-bit binary bytes as 4 '6-bit' characters
*/
static void 
base64_encodeblock( UCHAR in[3], UCHAR out[4], INT len );

/*
** decode
**
** decode a base64 encoded stream discarding padding, line breaks and noise
*/
CHAR * 
base64_encode(CHAR *source, CHAR *destination);

/**
 * Gets a string in 10.23.12.98 format and returns a four byte IP address array
 *
 * @param string containing IP address
 * @param numerical representation of IP address
 * @return 1 for OK, otherwise failed
 */
uint8
ip_convert_address (CHAR *ipstring, CHAR ipaddr[]);

/**
 * Gets a string in 00:CF:52:35:00:01 format and returns a six byte MAC address array
 *
 * @param string containing MAC address
 * @param numerical representation of MAC address 
 * @return 1 for OK, otherwise failed
 */
uint8
parse_ethaddr (CHAR *ethstr, uint8 *ethaddr);

/**
 * Returns an integer number contained in the string starting with
 * the key and in selected base. Stops when a non-number char is found.
 * Example:  "SPIPORT=1&SPOPOLA=2" is the string
 *  Returns an integer 1 with key '=' and base 10
 *
 * @param string to parse
 * @param key to start parsing
 * @param base of number to parse
 * @return parsed numbered, otherwise zero. 
 *         string pointer is modified pointing to the end of the parsed number
 */
uint32
parse_number(uint8 **string, uint8 key, uint8 number_base);

/**
 * Build a string from another string using start and end delimitator pointers
 *
 * @param string to be search
 * @param built string
 * @param start character delimitator
 * @param end character delimitator
 * @return none
 */
void
parse_mac_ip_address_string(uint8 **string, uint8 *found, uint8 start, uint8 end);

/**
 * Search and return a string from a linked list
 *
 * @param linked list in pbuf typedef
 * @param buffer to use. Must be greater than 2 * pbuf max size.
 * @param starting string
 * @param ending string
 * @return pointer to found string. NULL if was not found
 */
uint8 *
search_string_linked_list(void *linked, uint8 *buffer, uint8 *search_start, uint8 *search_end);

/**
 * Search string in a continous string
 *
 * @param string to search
 * @param starting string
 * @param ending string
 * @return found string using buffer as allocator. NULL if not found
 */
uint8 *
search_string(uint8 *buffer, uint8 *search_start, uint8 *search_end);

#endif