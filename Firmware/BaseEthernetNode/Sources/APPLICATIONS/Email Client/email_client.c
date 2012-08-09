/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

/* ------------------------ lwIP includes --------------------------------- */
#include "api.h"

#include "email_client.h"
#include "mcu_init.h"
#include "setget.h"
#include "utilities.h"/*base64 encoding utilities*/

/*Mutex to Email Server*/     
xSemaphoreHandle EMailMutex;

/********************************************************************/
/*Prototype*/
INT
sprintf (CHAR *s, const CHAR *fmt, ...);
/********************************************************************/

/**
 * Start email service by creating mutex
 *
 * @param none
 * @return none
 */
void
Email_init ( void )
{
   /*FSL: create mutex for shared resource*/
   EMailMutex = xSemaphoreCreateMutex();
}

/********************************************************************/

/**
 * Send an email using SMTP protocol to specified variables.
 *   flag element cleared means attempt to send is over
 *   ready element cleared means succesful attempt, otherwise error
 *
 * @param info email info to be used for SMTP communication
 * @return pointer to the created task
 *         NULL if no task could be created
 */
void *
Email_send ( EMAIL_TEMPLATE *info )
{      
   /*wait until tcp/ip stack has a valid IP address*/
   while( lwip_interface_is_up() == 0 )
   {
       /*Leave execution for 1000 ticks*/
       vTaskDelay(1000);
   }

   /*FSL: do not start a new one until this is over*/
   xSemaphoreTake(EMailMutex, portMAX_DELAY);
   
   /*Email has not been sent yet: waiting for EMail task*/
   info->flag = 0xFF;
   
   /* Start the email client to send request information thru SMTP: asynch */
   return (void *)sys_thread_new("MAIL", vEmailClient, (void *)info, EMAILCLIENT_STACK_SPACE, EMAIL_TASK_PRIORITY );
   
   /*mutex released when email task is over, either result*/
}

/**
 * Returns 0 if search parameter is not found
 *
 * @param string to compare
 * @param text to find on string to compare
 * @return found flag. Clear if found, otherwise not
 */
static uint8
Email_res_val(uint8 *string, CHAR *search)
{
  if( strstr(string,search) != NULL)
  {
    return 0;/*found*/
  }
  else
  {
    return 1;/*not found*/
  }
}

/********************************************************************/

/**
 * Running task to send an Email
 *
 * @param info email info to be used for SMTP communication
 * @return 
 */
static void
vEmailClient( void *pvParameters )
{
    /*email variables*/
    struct netconn *conn;

    /*FSL:holding information*/
    uint8 *temporal_buffer;
    
    /*hold names taken from ROM*/
    uint8 *temporal_name_buffer;
     
    /*SMTP server IP address*/    
    struct ip_addr smtp_server;
    
    EMAIL_TEMPLATE *email_info;

    /*FSL: get email info to be used*/
    email_info = (EMAIL_TEMPLATE *)pvParameters;

    /*FSL: check if this space is enough: max required was 99 bytes*/
    if ( ((temporal_buffer = ( uint8 * )mem_malloc( SMTP_REQUEST_MAX_LENGTH )) == NULL) || 
         ((temporal_name_buffer = ( uint8 * )mem_malloc( STRING_SIZE )) == NULL) )
    {
       /*out of memoryy*/
       goto exit_mail_task;
    }
    
    /**********************FSL: socket start-up*******************************/
    
    /* Create a new TCP connection handle. */
    conn = netconn_new(NETCONN_TCP);
    
    /*set timeout for this connection*/
    netconn_set_timeout((void *)conn,0x1FF/*timeout*/);

    /*Get SMTP server address*/
    board_get_email_smtp_server(temporal_buffer);
    if( netconn_gethostbyname((const CHAR *)temporal_buffer,&smtp_server) != ERR_OK )
    {
       /*error*/
       goto exit_mail_socket_low_level;
    }

    /*wait until it's linked to server*/
    if( netconn_connect(conn,&smtp_server,SMTP_PORT) != ERR_OK )
    {
       /*error*/
       goto exit_mail_socket_low_level;
    }
    //**********************************Connection ESTABLISHMENT START*********

    /*S0:get server response: FIRST connection establishment: RESPONSE 220*/
    netconn_rcv_req((void *)conn,temporal_buffer,NULL,NULL) ;
    if( conn->err != ERR_OK ){goto exit_mail_socket_low_level;}

    /*get authentication variable*/
    if( (uint8)board_get_email_authentication_required() == 0 )
    {
        /*C1:Connection establishment: HELO DOMAIN*/
        netconn_write(conn,SMTP_HELO_REQUEST,str_len(SMTP_HELO_REQUEST),NULL);
        /*S1:get server response: RESPONSE 250*/
        netconn_rcv_req((void *)conn,temporal_buffer,NULL,NULL) ;
        if( conn->err != ERR_OK ){goto exit_mail_socket_low_level;}
    }
    else
    {
        /*C1:Send: EHLO DOMAIN*/
        netconn_write(conn,SMTP_EHLO_REQUEST,str_len(SMTP_EHLO_REQUEST),NULL);
        /*S1:RESPONSE 250*/
        netconn_rcv_req((void *)conn,temporal_buffer,NULL,NULL) ;
        if( conn->err != ERR_OK ){goto exit_mail_socket_low_level;}
        if( Email_res_val(temporal_buffer,SMTP_CODE_250) != 0 ){goto exit_mail_socket_high_level;}

        /*C2:start login using AUTH LOGIN*/
        netconn_write(conn,SMTP_AUTH_LOGIN_REQUEST,str_len(SMTP_AUTH_LOGIN_REQUEST),NULL);
        /*S2:RESPONSE 334: VXNlcm5hbWU6 (Username:)*/
        netconn_rcv_req((void *)conn,temporal_buffer,NULL,NULL) ;
        if( conn->err != ERR_OK ){goto exit_mail_socket_low_level;}
        if( Email_res_val(temporal_buffer,SMTP_CODE_334) != 0 ){goto exit_mail_socket_high_level;}

        /*base64 web page: http://www.motobit.com/util/base64-decoder-encoder.asp*/

        /*C3:sending username encoded as base64*/
        board_get_email_username(temporal_name_buffer);
        sprintf( (CHAR *)temporal_buffer, SMTP_ENCODED_STRING, base64_encode((CHAR *)temporal_name_buffer,(CHAR *)temporal_buffer) );
        netconn_write(conn,temporal_buffer,strlen(temporal_buffer),NETCONN_COPY);
        /*S3:RESPONSE 334: UGFzc3dvcmQ6 (Password:)*/
        netconn_rcv_req((void *)conn,temporal_buffer,NULL,NULL) ;
        if( conn->err != ERR_OK ){goto exit_mail_socket_low_level;}
        if( Email_res_val(temporal_buffer,SMTP_CODE_334) != 0 ){goto exit_mail_socket_high_level;}
        
        /*C4:sending password encoded as base64*/
        board_get_email_password(temporal_name_buffer);
        sprintf( (CHAR *)temporal_buffer, SMTP_ENCODED_STRING, base64_encode((CHAR *)temporal_name_buffer,(CHAR *)temporal_buffer) );
        netconn_write(conn,temporal_buffer,strlen(temporal_buffer),NETCONN_COPY);
        /*S4:RESPONSE: 235 OK: already signed up*/
        netconn_rcv_req((void *)conn,temporal_buffer,NULL,NULL) ;
        if( conn->err != ERR_OK ){goto exit_mail_socket_low_level;}
        if( Email_res_val(temporal_buffer,SMTP_CODE_235) != 0 ){goto exit_mail_socket_low_level;}   
    }   
    //**********************************Connection ESTABLISHMENT END***********
    
    //**********************************Connection MESSAGE TRANSFER START******
    
    /*C5: sending MAIL FROM*/
    board_get_email_username(temporal_name_buffer);
    sprintf( (CHAR *)temporal_buffer, SMTP_MAIL_FROM_STRING, temporal_name_buffer); 
    netconn_write(conn,temporal_buffer,strlen(temporal_buffer),NETCONN_COPY);
    /*S5: validating it: RESPONSE: 250*/
    netconn_rcv_req((void *)conn,temporal_buffer,NULL,NULL) ;
    if( conn->err != ERR_OK ){goto exit_mail_socket_low_level;}
    if( Email_res_val(temporal_buffer,SMTP_CODE_250) != 0 ){goto exit_mail_socket_high_level;}
    
    /*C6: sending RECIPIENT FROM*/
    sprintf( (CHAR *)temporal_buffer, SMTP_MAIL_TO_STRING, email_info->to);
    netconn_write(conn,temporal_buffer,strlen(temporal_buffer),NETCONN_COPY);
    /*S6: validating it: RESPONSE: 250*/
    netconn_rcv_req((void *)conn,temporal_buffer,NULL,NULL) ;
    if( conn->err != ERR_OK ){goto exit_mail_socket_low_level;}
    if( Email_res_val(temporal_buffer,SMTP_CODE_250) != 0 ){goto exit_mail_socket_high_level;}

    /*C7: sending data command: DATA*/
    netconn_write(conn,SMTP_DATA_REQUEST,str_len(SMTP_DATA_REQUEST),NULL);
    /*S7: validating it: RESPONSE: 354*/
    netconn_rcv_req((void *)conn,temporal_buffer,NULL,NULL) ;
    if( conn->err != ERR_OK ){goto exit_mail_socket_low_level;}
    if( Email_res_val(temporal_buffer,SMTP_CODE_354) != 0 ){goto exit_mail_socket_high_level;} 
    
    /*C8: sending HEADER and DATA without receiving a string from SMTP server*/
    board_get_email_username(temporal_name_buffer);
    sprintf( (CHAR *)temporal_buffer, SMTP_HEADER_STRING, temporal_name_buffer,email_info->to,email_info->subject);
    netconn_write(conn,temporal_buffer,strlen(temporal_buffer),NETCONN_COPY);
    netconn_write(conn,email_info->data,strlen(email_info->data),NETCONN_COPY);        

    /*C9: closing email DATA*/
    netconn_write(conn,SMTP_DATA_EMAIL_END,str_len(SMTP_DATA_EMAIL_END),NULL);
    /*S9: email complete: RESPONSE: 250*/
    netconn_rcv_req((void *)conn,temporal_buffer,NULL,NULL) ;
    if( conn->err != ERR_OK ){goto exit_mail_socket_low_level;}
    if( Email_res_val(temporal_buffer,SMTP_CODE_250) != 0 ){goto exit_mail_socket_high_level;}
    
    /*FSL: at this point, email was succesfully sent*/
    if( email_info->flag )
    {
      email_info->flag = 0;/*no more comparisons*/
      email_info->ready = 0;/*cleared if Email was succesfully sent*/
    }
    //**********************************Connection MESSAGE TRANSFER END********

    //**********************************Connection TERMINATION START***********
exit_mail_socket_high_level:
    /*C10: quit session: QUIT*/
    netconn_write(conn,SMTP_QUIT_REQUEST,str_len(SMTP_QUIT_REQUEST),NULL);
    /*S10: email complete: RESPONSE: 221*/
    netconn_rcv_req((void *)conn,temporal_buffer,NULL,NULL) ;
    if( conn->err != ERR_OK ){goto exit_mail_socket_low_level;}

    //**********************************Connection TERMINATION END***********

exit_mail_socket_low_level:
    /*delete TCP connection*/
    netconn_close(conn);
    netconn_delete(conn);

    /*delete the temporal buffers*/
    mem_free( temporal_buffer );
    mem_free( temporal_name_buffer );

exit_mail_task:
    if( email_info->flag )
    {
      email_info->flag = 0;/*no more comparisons*/
      email_info->ready = 0xFF;/*Email error*/
    }

    /*release eMail Mutex*/
    xSemaphoreGive(EMailMutex);

#if 0/*measuring stack space needed for this task*/    
    for(;;)
    {
      /*Leave execution*/
      vTaskDelay(100);      
    }
#endif    

    /*Task no longer needed, delete it!*/
    vTaskDelete( NULL );

    /*never get here!*/    
    return;
}