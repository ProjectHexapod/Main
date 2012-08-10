/*
 * A simple server/client socket interfacing the tcp/ip stack directly:
 * b06862
 *
 * Features:
 *   session is not closed until client does it first: TODO: automatic close
 *   SERIAL side sends if: at least a character is ready AND a 1/2 second has occurred.
 *   tcp packet length sent from the client only depends on client
 *   serial buffers lengths were selected according to performance and limits in memory
 *   will drop characters if internal queue is full
 */

/* ------------------------ FreeRTOS includes ----------------------------- */
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"
#include "sockets.h"

/* ------------------------ Project includes ------------------------------ */
#include "valve.h"

/*****************************************************************************/

// global mutex to prevent thread conflicts for lwip
extern xSemaphoreHandle lwip_mutex;

/*Mutex to MAC buffers*/
xSemaphoreHandle valve_mutex;

/**
 * Valve task
 *
 * @param new_val number in ticks to set the compare register to.  
 * 					Duty cycle becomes new_val/PWM_MODULO_COUNT
 * @return none
 */
void setDutyCycle(uint16 new_val)
{
	TPM1C2V = new_val;
}

void setDriveDir( int8 dir )
{
	if(dir>0)
	{
		PTED_PTED4 = 0; // Coil 0 inhibit OFF
		PTED_PTED3 = 1; // Coil 1 inhibit ON
		return;
	}
	if(dir<0)
	{
		PTED_PTED4 = 1; // Coil 0 inhibit ON
		PTED_PTED3 = 0; // Coil 1 inhibit OFF
		return;
	}
	// Inhibit both sides
	PTED_PTED4 = 1; // Coil 0 inhibit ON
	PTED_PTED3 = 1; // Coil 1 inhibit ON
}

/**
 * Valve task
 *
 * @param none  
 * @return none
 */
void
VALVE_Task( void *pvParameters )
{
	uint32 gateway_addr;
	uint32 retval;
	uint8  no_data_ticks_counter = 0;
	int recv_sock;
	uint8* recv_buff;
	struct sockaddr_in* bind_addr;
	struct sockaddr_in* recv_addr;
	socklen_t recv_len;
	
	/*FSL: create mutex for shared resource*/
	valve_mutex = xSemaphoreCreateMutex(); 

	// PWM Init 
	/* TPM1SC: TOF=0,TOIE=0,CPWMS=0,CLKSB=0,CLKSA=0,PS2=0,PS1=0,PS0=0 */
	TPM1SC = 0x00;              /* Disable device */ 
	/* TPM1C2SC: CH2F=0,CH2IE=0,MS2B=1,MS2A=1,ELS2B=1,ELS2A=1,??=0,??=0 */
	TPM1C2SC = 0x3C;            /* Set up PWM mode with output signal level low */ 
	// 0x00FF MODULO ends up generating 96kHz PWM - good!
	/* TPM1MOD: BIT15=1,BIT14=1,BIT13=1,BIT12=1,BIT11=1,BIT10=1,BIT9=1,BIT8=1,BIT7=1,BIT6=1,BIT5=1,BIT4=1,BIT3=1,BIT2=1,BIT1=1,BIT0=1 */
	TPM1MOD = PWM_MODULO_COUNT;          /* Set modulo register */ 
	/* TPM1SC: TOF=0,TOIE=0,CPWMS=0,CLKSB=0,CLKSA=1,PS2=0,PS1=0,PS0=0 */
	TPM1SC = 0x08;              /* Run the counter (set CLKSB:CLKSA) */ 
	/* PTEPF1: E5=3 */
	PTEPF1 |= 0x0C;
	
	// PWM Enable
	/* TPM1SC: TOF=0,TOIE=0,CPWMS=0,CLKSB=0,CLKSA=1,PS2=0,PS1=0,PS0=0 */
	TPM1SC = 0x08;              /* Run the counter (set CLKSB:CLKSA) */ 
	/* PTEPF1: E5=3 */
	PTEPF1 |= 0x0C;
	
    // Set up the inhibit pins as GPIO outputs
    PTEDD_PTEDD3 = 1;
    PTEDD_PTEDD4 = 1;
    // Start with both coils inhibited
    PTED_PTED3   = 1;
    PTED_PTED4   = 1;
    
    if( (recv_buff = (void*)malloc(RECV_BUFFSIZE)) == NULL )
    {
    	// Memory allocaiton failure
    	vTaskDelete(NULL);
    }
    
    /*wait until ip stack has a valid IP address*/
	while( get_lwip_ready() == FALSE )
	{
	   /*Leave execution for 100 ticks*/
	   vTaskDelay(100);
	}
    
    while( !xSemaphoreTake(lwip_mutex, 1) )
    			;
    // Receive socket initialization
    // Create a socket to receive UDP data on
    if( (recv_sock = lwip_socket(0x00, SOCK_DGRAM, IPPROTO_UDP)) == -1 )
    {
    	// Failed to create socket
    	vTaskDelete(NULL);
    }

	gateway_addr = board_get_eth_gateway();
	
	bind_addr = (struct sockaddr_in*)mem_malloc(sizeof(struct sockaddr_in));
	bind_addr->sin_family = AF_INET;
	bind_addr->sin_len    = sizeof(struct in_addr);
	bind_addr->sin_port   = 1545;
	bind_addr->sin_addr.s_addr = INADDR_ANY;
	
	// Bind the socket.  We are now ready to receive packets.
	if( lwip_bind(recv_sock, (struct sockaddr*)bind_addr, sizeof(struct sockaddr_in)) )
	{
		// Bind error!
		vTaskDelete(NULL);
	}
	xSemaphoreGive(lwip_mutex);
	
	// Allocate space for the receive address information
	recv_addr = (struct sockaddr_in*)mem_malloc(sizeof(struct sockaddr_in));
	recv_len = sizeof(struct sockaddr_in);
	
	/* Loop forever */
	for( ;; )
	{
		while( !xSemaphoreTake(valve_mutex, 1) )
			;
		if( (retval = lwip_recvfrom(
				recv_sock, 		//Socket to receive from
				recv_buff, 		//Buffer to write data in to
				RECV_BUFFSIZE, 	//size of buffer
				O_NONBLOCK,		//flags
				(struct sockaddr*)recv_addr, 		//Where to put sender information
		        &recv_len)) == 2 ) 	//Length of receive from adress structure
		{
			// We received the right amount of data!
			setDriveDir ((int8)recv_buff[1]);
			setDutyCycle(recv_buff[0]);
			no_data_ticks_counter = 0;
		}
		else
		{
			// Have we exceeded our timeout?
			if( ++no_data_ticks_counter >= NO_DATA_TICKS_THRESHOLD )
			{
				// Shut it down!
				setDutyCycle(0);
			}
		}
		xSemaphoreGive(valve_mutex);
		/* Leave execution for 1 tick */
		/* Ends up running at 500Hz */
		vTaskDelay(1);
	}      
 
    return;
}