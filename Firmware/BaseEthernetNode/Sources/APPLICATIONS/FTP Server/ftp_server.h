#ifndef _FTP_SERVER_H_
#define _FTP_SERVER_H_


enum
{
  FTP_CLOSED,
  FTP_OPEN
};

#define FTP_TASK_PRIORITY          tskIDLE_PRIORITY + 3

#define FTP_TCP_CONTROL_PORT       21

#define FTP_REQUEST_SPACE          32/*Client request should not be longer*/

/*FTP Server Requests*/
#define FTP_USER_REQUEST           "USER"
#define FTP_PASS_REQUEST           "PASS"              
#define FTP_QUIT_REQUEST           "QUIT"
#define FTP_PORT_REQUEST           "PORT"
#define FTP_NLST_REQUEST           "NLST"
#define FTP_STOR_REQUEST           "STOR"
#define FTP_RETR_REQUEST           "RETR"
#define FTP_DELE_REQUEST           "DELE"

/*FTP Server Response*/
#define FTP_WELCOME_RESPONSE        "220 Service Ready\r\n"
#define FTP_USER_RESPONSE           "331 USER OK. PASS needed\r\n"
#define FTP_PASS_FAIL_RESPONSE      "530 NOT LOGGUED IN\r\n"
#define FTP_PASS_OK_RESPONSE        "230 USR LOGGUED IN\r\n"
#define FTP_PORT_OK_RESPONSE        "200 PORT OK\r\n"
#define FTP_NLST_OK_RESPONSE        "150 NLST OK\r\n"
#define FTP_RETR_OK_RESPONSE        "150 RETR OK\r\n"
#define FTP_STOR_OK_RESPONSE        "150 STOR OK\r\n"
#define FTP_DELE_OK_RESPONSE        "150 DELE OK\r\n"
#define FTP_QUIT_RESPONSE           "221 BYE OK\r\n"
#define FTP_TRANSFER_OK_RESPONSE    "226 Transfer OK\r\n"
#define FTP_WRITE_FAIL_RESPONSE     "550 File unavailable\r\n"
#define FTP_CMD_NOT_IMP_RESPONSE    "502 Command Unimplemented\r\n"
#define FTP_DATA_PORT_FAILED        "425 Cannot open Data Port\r\n"
#define FTP_UNKNOWN_RESPONSE        "500 Unrecognized Command\r\n"
#define FTP_BAD_SEQUENCE_RESPONSE   "503 Bad Sequence of Commands\r\n"

/********Prototype Functions************************************/

/**
 * FTP Server Main Control Socket Parser: requests and responses
 *  Available requests: USER, PASS, PORT, QUIT
 *
 * @param connection descriptor
 * @param buffer to hold FTP requests
 * @return none
 */
static uint8
vFTPConnection(struct netconn *connfd, uint8 *alloc_rq);

/**
 * Closes or Leave session depending on client request
 *
 * @param connection descriptor
 * @param buffer space 
 * @return 0 keep session, otherwise session needs to be closed
 */
uint8
FTP_QUIT_OR_WRONG_REQUEST(struct netconn *connfd, uint8 *alloc_rq);

/**
 * FTP Server Main Data Socket Parser: requests and responses
 *  Available requests: NLST, RTR, STOR
 *
 * @param connection descriptor
 * @param string containing data socket port number and address
 * @return none
 */
static uint8 
FTP_DataFlowControl(struct netconn *connfd, uint8 *alloc_rq);

/**
 * Look if a file already exist with the name
 *  No case sensitive
 *
 * @param file name to look for on FAT
 * @return 0 if file was found, otherwise not
 */
uint8
FTP_Does_File_Exist(uint8 *data);

/**
 * Callback to send files name to ethernet
 *
 * @param descriptor to use for sending
 * @param filename string
 * @return always 1
 */
UINT8
FTP_SD_send(void* var,UINT8 *fileName);

/**
 * Callback to check if file exists
 *
 * @param filename to compare
 * @param filename string
 * @return 0 if file found, otherwise zero
 */
UINT8
FTP_CompareFile(void* var,UINT8 *fileName);

/**
 * Returns thru connection descriptor all files names in FAT
 *
 * @param connection descriptor to send files' names
 * @return 0 if read was OK, otherwise not
 */
uint8
FTP_Read_List_Of_Files(struct netconn *connfd);

/**
 * Check if filename exists in FAT system for reading
 *
 * @param file name to check
 * @return 0 if read is possible, otherwise not
 */
uint8
FTP_Read_Is_Possible(uint8 *data);

/**
 * Gets a file from FAT and send it to a connection descriptor
 *  Call FTP_Read_Is_Possible(...)
 *
 * @param connection descriptor to write data read data
 * @return 0 if read was OK, otherwise not
 */
uint8
FTP_Read_File(struct netconn *connfd);

/**
 * Puts a file from a connection descriptor and send it to FAT
 *  First check if file do not exist to avoid duplication of files in FAT
 *
 * @param connection descriptor to use read data
 * @param file name to write.
 * @return 0 if read was OK, otherwise not
 */
uint8
FTP_Write_File(struct netconn *connfd, uint8 *data);

/**
 * Start an embedded FTP server Task: 1 client and 1 file per transfer
 *
 * @param paremeter pointer to use with task
 * @return none
 */
void
vBasicFTPServer( void *pvParameters );

#endif