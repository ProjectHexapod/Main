#ifndef _EMAIL_CLIENT_H_
#define _EMAIL_CLIENT_H_

#define EMAIL_TASK_PRIORITY       ( tskIDLE_PRIORITY + 3 )

#define SMTP_PORT                       25/*TCP port*/

#define SMTP_REQUEST_MAX_LENGTH         128

/*SMTP Client Requests*/
#define SMTP_HELO_REQUEST               "HELO fsl.com\r\n" /*no authentication*/
#define SMTP_EHLO_REQUEST               "EHLO fsl.com\r\n" /*authentication*/
#define SMTP_AUTH_LOGIN_REQUEST         "AUTH LOGIN\r\n"
#define SMTP_ENCODED_STRING             "%s\r\n"
#define SMTP_MAIL_FROM_STRING           "MAIL FROM: <%s>\r\n"
#define SMTP_MAIL_TO_STRING             "RCPT TO: <%s>\r\n"
#define SMTP_DATA_REQUEST               "DATA\r\n"
#define SMTP_HEADER_STRING              "From: <%s>\r\n"\
                                        "To: <%s>\r\n"\
                                        "Subject: %s\r\n\r\n"
#define SMTP_DATA_EMAIL_END             "\r\n.\r\n"
#define SMTP_QUIT_REQUEST               "QUIT\r\n"

/*SMTP Server Responses*/
#define SMTP_CODE_235                   "235"
#define SMTP_CODE_250                   "250"              /*requested email action OK and completed*/
#define SMTP_CODE_334                   "334"
#define SMTP_CODE_354                   "354"              /*start the mail input*/
                                                           
typedef struct
{
    CHAR *  to;          /*email recepient*/
    CHAR *  subject;     /*email subject*/
    CHAR *  data;        /*email content*/
    volatile CHAR flag;  /*set if email task need to check delivery*/
    volatile CHAR ready; /*if cleared, email was deliverd, otherwise not*/
} EMAIL_TEMPLATE;

/**
 * Start email service by creating a mutex
 *
 * @param none
 * @return none
 */
void
Email_init ( void );

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
Email_send ( EMAIL_TEMPLATE *info );

/**
 * Running task to send an Email
 *
 * @param info email info to be used for SMTP communication
 * @return 
 */
static void
vEmailClient( void *pvParameters );
 
#endif