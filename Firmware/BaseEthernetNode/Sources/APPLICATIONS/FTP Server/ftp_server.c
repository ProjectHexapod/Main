/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

/* ------------------------ lwIP includes --------------------------------- */
#include "api.h"

/* ------------------------ Project includes ------------------------------ */
#include "SD.h"         /* SD Card Driver (SPI mode) */
#include "FAT.h"

/* ------------------------ Project includes ------------------------------ */
#include "ftp_server.h"
#include "utilities.h"

#define FTP_USERNAME          "user"
#define FTP_PASSWORD          "Freescale123"

 
/*Handle SD card*/
static FATHandler *SD_FTP_Handle;

/*Read Buffer for App*/  
static UINT8 *SDbuffer;

#define FTP_MUTEX_ENTER   xSemaphoreTake((xSemaphoreHandle)SD_FTP_Handle->FAT_Mutex, portMAX_DELAY);
#define FTP_MUTEX_EXIT    xSemaphoreGive((xSemaphoreHandle)SD_FTP_Handle->FAT_Mutex);

/*FSL:sprintf prototype*/
INT
sprintf(CHAR *, const CHAR *, ... );

/********************Private Functions ***************************************/

/**
 * FTP Server Main Control Socket Parser: requests and responses
 *  Available requests: USER, PASS, PORT, QUIT
 *
 * @param connection descriptor
 * @param buffer to hold FTP requests
 * @return none
 */
static uint8
vFTPConnection(struct netconn *connfd, uint8 *alloc_rq)
{
  //uint8 temp_data;
  uint8 correct_login = FALSE;

  /*send FTP server first RESPONSE*/
  //****RESPONSE OK CONNECTED
  netconn_write(connfd,FTP_WELCOME_RESPONSE,str_len(FTP_WELCOME_RESPONSE),NULL);
  
  do
  {
    /*if reception is OK: wait for REQUEST from client*/
    netconn_rcv_req((void *)connfd, alloc_rq, NULL,NULL);
    if(connfd->err != ERR_OK)
    {
      /*session closed by client*/
      break;
    }
    
    /*authentication required*/           
    if( correct_login == TRUE)//already logged in
    {
       /*PORT request*/
       if( strstr(alloc_rq,FTP_PORT_REQUEST) != NULL )
       {
          FTP_DataFlowControl(connfd,&alloc_rq[sizeof(FTP_PORT_REQUEST)]);
       }
       /*DELETE request*/
       else if( strstr(alloc_rq,FTP_DELE_REQUEST) != NULL )
       {
          if (FILE_DELETED == FAT_FileDelete(SD_FTP_Handle,SDbuffer,(uint8 *)strupr(&alloc_rq[sizeof(FTP_DELE_REQUEST)])) )
          {
             //****RESPONSE: OK
             netconn_write(connfd,FTP_DELE_OK_RESPONSE,str_len(FTP_DELE_OK_RESPONSE),NULL);            
          }
          else
          {
             //****RESPONSE: FAILED
             netconn_write(connfd,FTP_WRITE_FAIL_RESPONSE,str_len(FTP_WRITE_FAIL_RESPONSE),NULL);             
          }
       }
       /*UNIMPLEMENTED request*/
       else
       {
          if( !FTP_QUIT_OR_WRONG_REQUEST(connfd,alloc_rq) )
          {
             break;/*QUIT command*/
          }
       }
    }
    else//not logged in
    {
       if( strstr(alloc_rq,FTP_USER_REQUEST) != NULL )
       {          
          /*authentication process: username matchs exactly?*/
          if( !strncmp(&alloc_rq[sizeof(FTP_USER_REQUEST)],FTP_USERNAME,str_len(FTP_USERNAME)) )
          {
              //*****RESPONSE USER OK
              netconn_write(connfd,FTP_USER_RESPONSE,str_len(FTP_USER_RESPONSE),NULL);
              
              /*if reception is OK: wait for REQUEST from client*/
              netconn_rcv_req((void *)connfd, alloc_rq, NULL, NULL);
              if(connfd->err != ERR_OK)
              {
                 /*session closed by client*/
                 break;
              }
              
              if( strstr(alloc_rq,FTP_PASS_REQUEST) != NULL )
              {
                  /*authentication process: password matchs exactly?*/
                  if( !strncmp(&alloc_rq[sizeof(FTP_PASS_REQUEST)],FTP_PASSWORD,str_len(FTP_PASSWORD)) )
                  {
                    //***RESPONSE: PASSWORD OK
                    netconn_write(connfd,FTP_PASS_OK_RESPONSE,str_len(FTP_PASS_OK_RESPONSE),NULL);
                    
                    correct_login = TRUE;
                  }
                  else
                  {
                    //***RESPONSE: PASSWORD FAILED
                    netconn_write(connfd,FTP_PASS_FAIL_RESPONSE,str_len(FTP_PASS_FAIL_RESPONSE),NULL);
                  }
              }
              else
              {
                  //***RESPONSE: EXPECTING PASS request
                  netconn_write(connfd,FTP_BAD_SEQUENCE_RESPONSE,str_len(FTP_BAD_SEQUENCE_RESPONSE),NULL);
              }
          }
          else
          {
              //***RESPONSE USER FAILED
              netconn_write(connfd,FTP_PASS_FAIL_RESPONSE,str_len(FTP_PASS_FAIL_RESPONSE),NULL);
          }
       }
       else
       {
          if( !FTP_QUIT_OR_WRONG_REQUEST(connfd,alloc_rq) )
          {
             break;/*QUIT command*/
          }
       }
    }
  }while(1);      

ftp_tcp_exit_low:
  /*client closing the session*/
  netconn_close(connfd);
  netconn_delete(connfd);
  
  /*close the session!!*/

  return 1;/*default close value*/
}

/**
 * Closes or Leave session depending on client request
 *
 * @param connection descriptor
 * @param buffer space 
 * @return 0 keep session, otherwise session needs to be closed
 */
uint8
FTP_QUIT_OR_WRONG_REQUEST(struct netconn *connfd, uint8 *alloc_rq)
{
   if( strstr(alloc_rq,FTP_QUIT_REQUEST) != NULL )
   {
      //****RESPONSE CLOSING SESSION: BYE
      netconn_write(connfd,FTP_QUIT_RESPONSE,str_len(FTP_QUIT_RESPONSE),NULL); 
      return 1;/*close session*/
   }
   else
   {
      //****UNKNOWN REQUEST
      netconn_write(connfd,FTP_UNKNOWN_RESPONSE,str_len(FTP_UNKNOWN_RESPONSE),NULL);
      return 0;/*keep session*/
   }  
}

/**
 * Open data socket: ftp server connects to client.
 *
 * @param ip address to connect to
 * @param tcp port to connect to
 * @return connection descriptor, if NULL error, other OK.
 */
struct netconn *
FTP_OpenDataPort(struct ip_addr *add, uint16 port)
{
  /*START:open specific port requested by PORT*/
  /* Create a new TCP connection handle. */
  struct netconn *conn_data;
  
  /*create data port*/
  if( (conn_data = netconn_new(NETCONN_TCP)) == NULL )
  {
     return NULL;/*error*/
  }
  /*wait until it's linked to server*/
  if( netconn_connect(conn_data,add,port) != ERR_OK )
  {
     return NULL;/*error*/
  }    
  /*set timeout for this connection*/
  //netconn_set_timeout((void *)conn_data,4000/*timeout*/);
  
  /*END*/
  return conn_data;  
}

/**
 * Close data socket
 *
 * @param connection descriptor
 * @return 0 if connection was closed
 */
static uint8
FTP_CloseDataPort(struct netconn *conn_data)
{
  /*delete TCP connection*/
  netconn_close(conn_data);
  netconn_delete(conn_data);  
  
  return 0;
}

/**
 * FTP Server Main Data Socket Parser: requests and responses
 *  Available requests: NLST, RTR, STOR
 *
 * @param connection descriptor
 * @param string containing data socket port number and address
 * @return none
 */
static uint8 
FTP_DataFlowControl(struct netconn *connfd, uint8 *alloc_rq)
{
    /*netconn describing DATA flow path*/
    struct netconn *conn_data;
    /*FTP client IP address*/
    T32_8 ip_address;
    T16_8 ftp_port;    
    /*temporal pointers*/
    CHAR *end;
    /*temporal counter*/
    CHAR i;

    /*****START: get PORT information: parsing*/
    //Get IP: four parts
    for(i=0;i<sizeof(ip_address);i++)
    {
       end = (CHAR *)strchr((const CHAR *)alloc_rq,',');        
       ip_address.bytes[i] = (uint8)strtoul(alloc_rq,(char **)&end,10);
       alloc_rq = (uint8 *)end + 1;      
    }
    //Get FTP Port:first part
    end = (CHAR *)strchr((const CHAR *)alloc_rq,',');        
    ftp_port.u8[0] = (uint8)strtoul(alloc_rq,(char **)&end,10);
    alloc_rq = (uint8 *)end + 1;
    //Get FTP Port:second part
    end = (CHAR *)strchr((const CHAR *)alloc_rq,'\r');        
    ftp_port.u8[1] = (uint8)strtoul(alloc_rq,(char **)&end,10);
    /*****END**********************************/
     
    //*****RESPONSE: OPEN PORT
    netconn_write(connfd,FTP_PORT_OK_RESPONSE,str_len(FTP_PORT_OK_RESPONSE),NULL);
    
    /*if reception is OK: wait for REQUEST from client from CONTROL port*/
    netconn_rcv_req((void *)connfd, alloc_rq, NULL, NULL);
    if(connfd->err != ERR_OK)
    {
       /*session closed by client*/
       return 1;/*FAIL*/
    }
    
    /*NLST*/
    if( strstr(alloc_rq,FTP_NLST_REQUEST) != NULL )
    {
      if( (conn_data = FTP_OpenDataPort((struct ip_addr *)&(ip_address.lword),ftp_port.u16)) != NULL )
      {
        //****Response Sending
        netconn_write(connfd,FTP_NLST_OK_RESPONSE,str_len(FTP_NLST_OK_RESPONSE),NULL);
        
        //Send the file list
        FTP_Read_List_Of_Files(conn_data);
        
        //Start Closing Data Stream
        FTP_CloseDataPort(conn_data);
        
        //****RESPONSE: OK
        netconn_write(connfd,FTP_TRANSFER_OK_RESPONSE,str_len(FTP_TRANSFER_OK_RESPONSE),NULL);
      }
      else
      {
        //****RESPONSE PORT cant be opened!!
        netconn_write(connfd,FTP_DATA_PORT_FAILED,str_len(FTP_DATA_PORT_FAILED),NULL);
        
        return 1;/*FAIL*/        
      }
    }
    /*READ*/
    else if( strstr(alloc_rq,FTP_RETR_REQUEST) != NULL )    
    {
      if( !FTP_Read_Is_Possible(&alloc_rq[sizeof(FTP_RETR_REQUEST)]) )
      {
        if( (conn_data = FTP_OpenDataPort((struct ip_addr *)&(ip_address.lword),ftp_port.u16)) != NULL )
        {
          //****Response Sending
          netconn_write(connfd,FTP_RETR_OK_RESPONSE,str_len(FTP_RETR_OK_RESPONSE),NULL);
          
          //send info
          FTP_Read_File(conn_data);
          
          //Start Closing Data Stream
          FTP_CloseDataPort(conn_data);
          
          //****RESPONSE: OK
          netconn_write(connfd,FTP_TRANSFER_OK_RESPONSE,str_len(FTP_TRANSFER_OK_RESPONSE),NULL);
        }
        else
        {
          return 1;
        }
      }
      else
      {
        //****RESPONSE: DUPLICATION FILE NAME
        netconn_write(connfd,FTP_WRITE_FAIL_RESPONSE,str_len(FTP_WRITE_FAIL_RESPONSE),NULL);
      }
    }
    /*WRITE*/
    else if( strstr(alloc_rq,FTP_STOR_REQUEST) != NULL )
    {
      if( !FTP_Does_File_Exist(&alloc_rq[sizeof(FTP_STOR_REQUEST)]) )
      {
         //****RESPONSE: FILE ALREADY EXISTS
         netconn_write(connfd,FTP_WRITE_FAIL_RESPONSE,str_len(FTP_WRITE_FAIL_RESPONSE),NULL);         
      }
      else
      {
        if( (conn_data = FTP_OpenDataPort((struct ip_addr *)&(ip_address.lword),ftp_port.u16)) != NULL )
        {
          //****Response Sending
          netconn_write(connfd,FTP_STOR_OK_RESPONSE,str_len(FTP_STOR_OK_RESPONSE),NULL);
          
          /*filename to write*/
          FTP_Write_File(conn_data,&alloc_rq[sizeof(FTP_STOR_REQUEST)]);
          
          //Start Closing Data Stream: client closes tcp session: against protocol!!
          FTP_CloseDataPort(conn_data);
          
          //****RESPONSE: OK
          netconn_write(connfd,FTP_TRANSFER_OK_RESPONSE,str_len(FTP_TRANSFER_OK_RESPONSE),NULL);
        }
        else
        {
          return 1;/*FAIL*/
        }        
      }
    }
    /*UNKNOWN OR NOT IMPLEMENTED*/
    else
    {
      //****Response: unknown request
      netconn_write(connfd,FTP_CMD_NOT_IMP_RESPONSE,str_len(FTP_CMD_NOT_IMP_RESPONSE),NULL); 
    }
    
    return 0;/*OK*/
}

/**
 * Look if a file already exist with the name
 *  No case sensitive
 *
 * @param file name to look for on FAT
 * @return 0 if file was found, otherwise not
 */
uint8
FTP_Does_File_Exist(uint8 *data)
{
    UINT8 result = 1;
    UINT8 i=0;
    
    /*convert to upper case:???*/
    strupr(data);

    /*FSL: SD Mutex Enter*/
    FTP_MUTEX_ENTER
    
    if(!FAT_LS(SD_FTP_Handle,SDbuffer,(void*)data,FTP_CompareFile))
    {
      result = 0;/*file found*/
    }

    /*SD Mutex Exit*/
    FTP_MUTEX_EXIT
    
    return result;/*File not found*/
}

/**
 * Callback to send files name to ethernet
 *
 * @param descriptor to use for sending
 * @param filename string
 * @return always 1
 */
UINT8
FTP_SD_send(void* var,UINT8 *fileName)
{
    struct netconn *connfd = (struct netconn *)var;
    
    /*append "\r\n"*/
    strcat( fileName, STRING_END );
    /*send files name*/
    netconn_write(connfd,fileName,strlen(fileName),NETCONN_COPY);
    return 1;  
}

/**
 * Callback to check if file exists
 *
 * @param data to compare
 * @param filename string
 * @return 0 if file found, otherwise zero
 */
UINT8
FTP_CompareFile(void* var,UINT8 *fileName)
{
    UINT8 *string = (UINT8 *)var;
    
    if( !strcmp(string,(const uint8 *)SDbuffer) )
      return 0;/*File Found*/
    else
      return 1;/*File not found*/
}

/**
 * Returns thru connection descriptor all files names in FAT
 *
 * @param connection descriptor to send files' names
 * @return 0 if read was OK, otherwise not
 */
uint8
FTP_Read_List_Of_Files(struct netconn *connfd)
{
    UINT8 u8BlockCounter=0;
    UINT8 u8BlockOffset=0;
    
    //TODO: what happens if no files at all?
    
    /*FSL: SD Mutex Enter*/
    FTP_MUTEX_ENTER

    /*dont care what it returns*/
    (void)FAT_LS(SD_FTP_Handle,SDbuffer,connfd,FTP_SD_send);  

    /*SD Mutex Exit*/
    FTP_MUTEX_EXIT
    
    return 0;/*OK*/
}

/**
 * Check if filename exists in FAT system for reading
 *
 * @param file name to check
 * @return 0 if read is possible, otherwise not
 */
uint8
FTP_Read_Is_Possible(uint8 *data)
{
  UINT8 result = 1;

  /*FSL: SD Mutex Enter*/
  FTP_MUTEX_ENTER;

  /*Look for file on SD card: uppercase is needed*/
  if( !FAT_FileOpen(SD_FTP_Handle,SDbuffer,(uint8 *)strupr(data),READ) )
  {
     result = 0;/*OK*/
  }

  /*SD Mutex Exit*/
  FTP_MUTEX_EXIT

  return result;/*Fail*/
}

/**
 * Gets a file from FAT and send it to a connection descriptor
 *  Call FTP_Read_Is_Possible(...)
 *
 * @param connection descriptor to write data read data
 * @return 0 if read was OK, otherwise not
 */
uint8
FTP_Read_File(struct netconn *connfd)
{
  UINT16 u16Length;
  
  /*first call: FTP_Read_Is_Possible(...)*/

  /*FSL: SD Mutex Enter*/
  FTP_MUTEX_ENTER
     
  /*File exists so */
  
  while( (u16Length=FAT_FileRead(SD_FTP_Handle,SDbuffer)) == BLOCK_SIZE )
  {     
    /*start sending SD BLOCKs*/     
    netconn_write(connfd,SDbuffer,BLOCK_SIZE,NETCONN_COPY);
  }
  if(u16Length)
  {
    /*start sending remaining SD BLOCK*/     
    netconn_write(connfd,SDbuffer,u16Length,NETCONN_COPY);      
  }

  /*SD Mutex Exit*/
  FTP_MUTEX_EXIT

  return 0;/*OK*/  
}

/**
 * Puts a file from a connection descriptor and send it to FAT
 *  First check if file do not exist to avoid duplication of files in FAT
 *
 * @param connection descriptor to use read data
 * @param file name to write.
 * @return 0 if read was OK, otherwise not
 */
uint8
FTP_Write_File(struct netconn *connfd, uint8 *data)
{
    UINT16 length;
    /*receiver buffer*/
    struct netbuf *inbuf;
    struct pbuf *q;
    
    /*Prior:string already doesnt exist on FAT*/
    /*FSL: SD Mutex Enter*/
    FTP_MUTEX_ENTER
    
    /*Write File: remaining bits: doesn't check for file names' duplication*/
    if( FAT_FileOpen(SD_FTP_Handle,SDbuffer,(uint8 *)strupr(data),CREATE) == FILE_CREATE_OK )
    {
       do
       {       
         /*stay here until session is: closed, received or out of memory*/
         length = netconn_rcv_req((void *)connfd, NULL, (void **)&inbuf, NETCONN_RCV_NETBUFFER);
         if( connfd->err == ERR_OK )
         {
           /*start segment index: copy all the network buffer segments*/
           q = inbuf->ptr;        
           do
           {             
             /*write as many bytes as needed*/
             FAT_FileWrite(SD_FTP_Handle,SDbuffer,q->payload,q->len);             
           }
           while( ( q = q->next ) != NULL );
           
           /*free pbuf memory*/
           netbuf_delete(inbuf);
         }
         else
         {
            /*session closed, out of memory, timeout: leave loop*/
            break;
         }       
       }while(1);
       
       /*close file*/
       FAT_FileClose(SD_FTP_Handle,SDbuffer);
    }
    
    /*SD Mutex Exit*/
    FTP_MUTEX_EXIT
    
    return length;/*Error*/  
}

/**
 * Start an embedded FTP server Task: 1 client and 1 file per transfer
 *
 * @param paremeter pointer to use with task
 * @return none
 */
void
vBasicFTPServer( void *pvParameters )
{
    /*Connection descriptors for FTP control port*/
    struct netconn *conn, *connection;
    uint8 *alloc_rq;
    
    UINT8 i = FTP_CLOSED;/*keep session information*/

    /* Parameters are not used - suppress compiler error. */
    ( void )pvParameters;

    /*Apps buffer*/
    if( ((SDbuffer=(uint8 *)mem_malloc( BLOCK_SIZE )) == NULL) || 
        ((alloc_rq=(uint8 *)mem_malloc( FTP_REQUEST_SPACE )) == NULL) )
    {
      mem_free(SDbuffer);      
      mem_free(alloc_rq);
      /*Task no longer needed, delete it!*/
      vTaskDelete( NULL );      
    }    
    /* SD Card Initialization */
    if( (SD_FTP_Handle = FAT_INIT(SDbuffer)) == NULL )
    {
      /*delete requested memory*/
      mem_free(SDbuffer);      
      mem_free(alloc_rq);
      /*error*/
      FAT_Close();
      /*Task no longer needed, delete it!*/
      vTaskDelete( NULL );
    }
    
    /**********************FSL: socket start-up*******************************/
    
    /* Create a new TCP connection handle. */
    conn = netconn_new(NETCONN_TCP);

    /* Bind the connection to port 21 on any local IP address. */
    netconn_bind(conn, NULL, FTP_TCP_CONTROL_PORT);
 
    /* Put the connection into LISTEN state. */
    netconn_listen(conn);

    /*set timeout for this connection*/
    netconn_set_timeout((void *)conn,0/*timeout*/);

    for(;;)/*infinite loop*/
    {
      if( i == FTP_CLOSED )/*FTP_CLOSE*/
      {
         if( (connection = netconn_accept(conn)) != NULL )
         {
            i = FTP_OPEN;
             /*set timeout for this connection*/
             netconn_set_timeout((void *)connection,0/*timeout*/);             
         }
      }
      else/*FTP_OPEN*/
      {
         /* Service connection */
         if( vFTPConnection( connection, alloc_rq ) )
         {
            i = FTP_CLOSED;
         }
      }
    }

    /*never get here!*/    
    return;
}
