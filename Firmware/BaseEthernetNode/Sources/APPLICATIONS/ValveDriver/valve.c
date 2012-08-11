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
#include "api.h"

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
	struct netconn* recv_conn;
	struct netbuf* recv_buf;
	void*  payload;
	uint16 payload_len;
	
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
    
    /*wait until ip stack has a valid IP address*/
	while( get_lwip_ready() == FALSE )
	{
	   /*Leave execution for 100 ticks*/
	   vTaskDelay(100);
	}

    /* Create a new UDP connection handle. */
	recv_conn = netconn_new(NETCONN_UDP);
	recv_buf  = netbuf_new();
	
	netconn_bind(recv_conn, IP_ADDR_ANY, 1545);
	
	/* Loop forever */
	for( ;; )
	{
		while( !xSemaphoreTake(valve_mutex, 1) )
			;
		recv_buf = netconn_recv( recv_conn );
		if( recv_buf != NULL )
		{
			// We received data!
			netbuf_data(recv_buf, &payload, &payload_len);
			setDriveDir (((int8*) payload)[1]);
			setDutyCycle(((uint8*)payload)[0]);
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