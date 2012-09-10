/* ------------------------ System includes ------------------------------- */
#include "stdlib.h"
#include "mcu_init.h"
#include "cc.h"

/* ------------------------ FreeRTOS includes ----------------------------- */
//#include "FreeRTOS.h"
//#include "task.h"
#include "spi_rtos.h"

/* ------------------------ LWIP includes --------------------------------- */
//#include "lwip/api.h"
//#include "lwip/tcpip.h"
//#include "lwip/memp.h"

/* ------------------------ Application includes -------------------------- */
//#include "http_server.h"
//#include "mag_enc.h"
//#include "valve.h"
#include "utilities.h"

/*b06862: Dec/10/2009: startup changes*/

/*********************************Prototypes**********************************/
// global buffer that provides interface to outside world
uint8 interface[128];
#define MAC_I     0
#define MAC_L     6
#define MAC_W_I   MAC_I+MAC_L
#define MAC_W_L   1
#define MAG_ENC_I MAC_W_I + MAC_W_L
#define MAG_ENC_L 3
#define VALVE_I   MAG_ENC_INDEX + MAG_ENC_SIZE
#define VALVE_L   1

// Global handle for Mag Encoder SPI
xSPIPortHandle SPIhandle;

/*********************************Functions***********************************/

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

void interrupt VectorNumber_Vrtc TickISR( void )
{
	//unsigned portLONG ulSavedInterruptMask;
	uint8 i;
	/*SPI array space*/
	/* 3 bytes is all that is required for mag enc */
	static uint8  spi_receive_array[3];

	/* Clear the interrupt. */
	RTCSC |= RTCSC_RTIF_MASK;

	//__RESET_WATCHDOG(); /* feeds the dog */

	// SERVICE MAGNETIC ENCODER ON SPI PORT
	// Assert CS
	PTCD_PTCD4 = 0;
	// Read Data
	for( i=0; i < 3; i++ )
	{
		xSPIMasterSetGetChar(	SPIhandle,
								SPI_DONTCARE,  // Data to write
								(signed char*)(spi_receive_array + i), //Address to write to 
								portMAX_DELAY); //Timeout 
	}
	// Deassert CS
	PTCD_PTCD4 = 1;
	
	// SERVICE THE VALVE DRIVER
	setDriveDir (0);
	setDutyCycle(0);
	
	// COPY NEW DATA IN TO INTERFACE BUFFER
	portDISABLE_INTERRUPTS();
	memcpy(interface+MAG_ENC_I, spi_receive_array, 3);
	portENABLE_INTERRUPTS();
	//portCLEAR_INTERRUPT_MASK_FROM_ISR( ulSavedInterruptMask );
}

/**
 * Main Routine: calls all inits
 *
 * @param none 
 * @return none
 */
void 
main(void) 
{
    /*FSL: independent platform standard init*/
    MCU_startup();
    
    /*TCP/IP stack init*/
    vlwIPInit(  );

	portDISABLE_INTERRUPTS();
    
#if 1
    // PWM Init 
	/* TPM1SC: TOF=0,TOIE=0,CPWMS=0,CLKSB=0,CLKSA=0,PS2=0,PS1=0,PS0=0 */
	TPM1SC = 0x00;              /* Disable device */ 
	/* TPM1C2SC: CH2F=0,CH2IE=0,MS2B=1,MS2A=1,ELS2B=1,ELS2A=1,??=0,??=0 */
	TPM1C2SC = 0x3C;            /* Set up PWM mode with output signal level low */ 
	// 0x00FF MODULO ends up generating 96kHz PWM - good!
	/* TPM1MOD: BIT15=1,BIT14=1,BIT13=1,BIT12=1,BIT11=1,BIT10=1,BIT9=1,BIT8=1,BIT7=1,BIT6=1,BIT5=1,BIT4=1,BIT3=1,BIT2=1,BIT1=1,BIT0=1 */
	TPM1MOD = 0x00FF;          /* Set modulo register */ 
	/* TPM1SC: TOF=0,TOIE=0,CPWMS=0,CLKSB=0,CLKSA=1,PS2=0,PS1=0,PS0=0 */
	TPM1SC = 0x08;              /* Run the counter (set CLKSB:CLKSA) */ 
	/* PTEPF1: E5=3 */
	PTEPF1 |= 0x0C;
	
	// Set duty cycle 50%
	TPM1C2V = (word)(0x0080);
	
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
#endif
#if 1
	// SPI Init
	
	/**********************FSL: spi start-up*******************************/
	SPIhandle = xSPIinit(    (eSPIPort)serSPI1, 
							 (spiBaud)spi1000, 
							 (spiPolarity)serIDLEshigh, 
							 (spiPhase)serMiddleSample, 
							 (spiMode)serMaster,
							 (spiInterrupt)serPolling,  
							 16/*SPI buffer limit*/); 

	/**********************FSL: low level start-up****************************/

	// Set GPIO direction
	PTCD_PTCD4 = 0;
	PTCDD_PTCDD4 = 1;
#endif
	
	// Setup the core ticker
	/* 1KHz clock. */
	RTCSC |= 8;
	
#define TICK_RATE_HZ          ( ( portTickType ) 2000 )
#define RTC_CLOCK_HZ		  ( ( u32_t ) 1000 )
	
	RTCMOD = RTC_CLOCK_HZ / TICK_RATE_HZ;
	
	/* Enable the RTC to generate interrupts - interrupts are already disabled
	when this code executes. */
	RTCSC_RTIE = 1;
	
	portENABLE_INTERRUPTS();
    
    while(1)
    {
    	
    }
    
    /* please make sure that you never leave main */
    for(;;)
    ;
}
