/* ------------------------ System includes ------------------------------- */
#include "mcu_init.h"
#include "MCF51CN128.h"
#include "spi.h"
#include "flash.h"
#include "mac_rtos.h"
#include "interface.h"

#define   Cpu_DisableInt() asm {move.w SR,D0; ori.l #0x0700,D0; move.w D0,SR;} /* Disable interrupts */
#define   Cpu_EnableInt()  asm {move.w SR,D0; andi.l #0xF8FF,D0; move.w D0,SR;} /* Enable interrupts */

#define portMAX_DELAY 0xffffffff
typedef unsigned char u8_t;
typedef signed char s8_t;
typedef unsigned short u16_t;
typedef signed short s16_t;
typedef unsigned long u32_t;
typedef signed long s32_t;
typedef u32_t   mem_ptr_t;
typedef int     sys_prot_t;

typedef enum 
{ 
	serIDLEslow, 
	serIDLEshigh 
} spiPolarity;

typedef enum 
{ 
	serMiddleSample, 
	serStartSample  
} spiPhase;

typedef enum
{
  serSlave,
  serMaster
} spiMode;

#define SPI_DONTCARE 0xFF

/*********************************Prototypes**********************************/
// global buffer that provides interface to outside world

interface_struct _interface_g;
extern const interface_struct _interface_rom;

interface_struct *interface_struct_g = &_interface_g;
unsigned char *interface_buff_g 			 = (unsigned char*)&_interface_g;

#define INTERFACE_L sizeof(interface_struct)

// number of ticks we've gone without receiving a command packet.
// If this exceeds some threshold, put the outputs in a 'safe' position
static unsigned char nticks_since_recv = 0;

// One tick is 1ms
// If we go 20ms without receiving a command packet, something's gone wrong with the host.
#define TICKS_TO_SAFE_MODE 20

/*********************************Functions***********************************/

void loadInterfaceFromFlash(void)
{
	memcpy(interface_struct_g, &_interface_rom, sizeof(interface_struct));
}

void writeInterfaceToFlash(void)
{
	Cpu_DisableInt();
	//erase logical page
	Flash_Erase(&_interface_rom);
	// write logical page
	// Length is expected in long words, so divide by 4
	Flash_Burst(&_interface_rom, sizeof(interface_struct)/4, interface_struct_g);
	Cpu_EnableInt();
}

enum CIDS {
	CMD_GENERIC_READWRITE,
	CMD_WRITE_TO_FLASH,
	CMD_RESET
};

struct pHeader {
	struct eth_addr dst_addr;
	struct eth_addr src_addr;
	unsigned char  magic_word; // always 0x69
	unsigned char  cmd_id;		 // Used to identify the command
	unsigned short packet_id;  // Set by master for tracking responses.  Can be anything.
};

#define TRACK_CHAR(x)  (x) = (unsigned char*)tracked; tracked += 1
#define TRACK_SHORT(x) (x) = (unsigned short*)tracked; tracked += 2
#define TRACK_LONG(x)  (x) = (unsigned long*)tracked; tracked += 4
#define PACKET_ASSERT(x) if(!(x)) {goto PARSE_ERROR;}

void interpretCommandBuffer( unsigned char* payload, unsigned short rx_len, unsigned char* tx_payload, unsigned short* tx_len )
{
	struct pHeader *rx_header, *tx_header;
	unsigned short *ra, *rl, *wa, *wl;
	unsigned char *tracked, *tracked_tx;
	
	// Load and check RX header
	tracked   = payload;
	rx_header = (struct pHeader*)tracked;
	tracked  += sizeof(struct pHeader);
	//Check the magic word
	PACKET_ASSERT(rx_header->magic_word == 0x69);
	
	// We've received a valid packet.  Reset the ticks counter
	nticks_since_recv = 0;
	
	//Point TX header appropriately
	tracked_tx  = tx_payload;
	tx_header   = (struct pHeader*)tracked_tx;
	tracked_tx += sizeof(struct pHeader);
	// Load TX header and
	// Swap MAC addresses
	tx_header->src_addr   = rx_header->dst_addr;
	tx_header->dst_addr   = rx_header->src_addr;
	tx_header->magic_word = rx_header->magic_word;
	tx_header->cmd_id     = rx_header->cmd_id;
	tx_header->packet_id  = rx_header->packet_id;
	
	switch( rx_header->cmd_id )
	{
	case CMD_GENERIC_READWRITE:
		TRACK_SHORT(ra);
		TRACK_SHORT(rl);
		TRACK_SHORT(wa);
		TRACK_SHORT(wl);
		// Tracked now points to the payload to be written to interface
		// Check to make sure the commands respect the bounds of the memory map
		PACKET_ASSERT(*ra + *rl < INTERFACE_L);
		PACKET_ASSERT(*wa + *wl < INTERFACE_L);
		// READ FROM MEMORY MAP
		memcpy(tracked_tx, interface_buff_g + *ra, *rl);
		*tx_len = sizeof(struct pHeader) + *rl;
		// WRITE TO MEMORY MAP
		memcpy(interface_buff_g + *wa, tracked, *wl);
		break;
	case CMD_WRITE_TO_FLASH:
		writeInterfaceToFlash();
		// Send response with a char indicating success
		*tracked_tx = 1;
		*tx_len = sizeof(struct pHeader) + 1;
		break;
	case CMD_RESET:
		// FIXME: DOESN'T WORK.  Can't find a good way to reset.
		mcf5xxx_reset();
	default:
		PARSE_ERROR:
		// Something bad happened.  Send empty response with normal header.
		*tx_len = sizeof(struct pHeader);
		break;
	}
	return;
}

#undef TRACK_CHAR
#undef TRACK_SHORT
#undef TRACK_LONG
#undef PACKET_ASSERT

void setDutyCycle(uint16 new_val)
{
	TPM1C2V = new_val;
}

void setDriveDir( int8 dir )
{
	if(dir>0)
	{
		PTEDD_PTEDD4 = 0; // Coil 0 on
		PTEDD_PTEDD3 = 1; // Coil 1 off
		return;
	}
	if(dir<0)
	{
		PTEDD_PTEDD4 = 1; // Coil 0 off
		PTEDD_PTEDD3 = 0; // Coil 1 on
		return;
	}
	// Inhibit both sides
	PTEDD_PTEDD4 = 1;
	PTEDD_PTEDD3 = 1;
}

void interrupt VectorNumber_Vrtc TickISR( void )
{
	//unsigned portLONG ulSavedInterruptMask;
	unsigned char i;
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
		spi_send_receive_waiting( 	SPI1_PORT,
									SPI_DONTCARE,
									(unsigned char*)(spi_receive_array + i));
	}
	// Deassert CS
	PTCD_PTCD4 = 1;
	
	//Protect from interruption
	Cpu_DisableInt();
	
	// Have we timed out?  If we haven't received a command packet in too long, shut the valve
	if(nticks_since_recv > TICKS_TO_SAFE_MODE)
	{
		interface_struct_g->valve_power = 0;
	} else {
		nticks_since_recv++;
	}
	
	// SERVICE THE VALVE DRIVER
	setDriveDir (interface_struct_g->valve_dir);
	setDutyCycle(interface_struct_g->valve_power);
	// COPY NEW DATA IN TO INTERFACE BUFFER
	memcpy(interface_struct_g->mag_enc, spi_receive_array, 3);
	Cpu_EnableInt();
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
	Cpu_DisableInt();
    /*FSL: independent platform standard init*/
    MCU_startup();
    
    // Load interface and default values from flash
    loadInterfaceFromFlash();
    
    // Initialize network interface
    MAC_init(&(interface_struct_g->mac_addr));
    
    // PWM Init 
	// Set up the inhibit pins
	// Start with both coils inhibited
    // Set the pin values to 0.  This will always be the case.
    // We allow the current driver to function by changing the pins to 
    // INPUTS, not by changing the value at the pin directly
	PTED_PTED3   = 0;
	PTED_PTED4   = 0;
	// Set the pins to be outputs.  This inhibits the driver
	PTEDD_PTEDD3 = 1;
	PTEDD_PTEDD4 = 1;

	
	/* TPM1SC: TOF=0,TOIE=0,CPWMS=0,CLKSB=0,CLKSA=0,PS2=0,PS1=0,PS0=0 */
	TPM1SC = 0x00;              /* Disable device */ 
	/* TPM1C2SC: CH2F=0,CH2IE=0,MS2B=1,MS2A=1,ELS2B=1,ELS2A=0,??=0,??=0 */
	TPM1C2SC = 0x38;            /* Set up PWM mode with output signal level low */ 
	// 0x00FF MODULO ends up generating 96kHz PWM - good!
	/* TPM1MOD: BIT15=1,BIT14=1,BIT13=1,BIT12=1,BIT11=1,BIT10=1,BIT9=1,BIT8=1,BIT7=1,BIT6=1,BIT5=1,BIT4=1,BIT3=1,BIT2=1,BIT1=1,BIT0=1 */
	TPM1MOD = 0x00FF;          /* Set modulo register */ 
	/* TPM1SC: TOF=0,TOIE=0,CPWMS=0,CLKSB=0,CLKSA=1,PS2=0,PS1=0,PS0=0 */
	TPM1SC = 0x08;              /* Run the counter (set CLKSB:CLKSA) */ 
	/* PTEPF1: E5=3 */
	PTEPF1 |= 0x0C;
	
	// PWM Enable
	/* TPM1SC: TOF=0,TOIE=0,CPWMS=0,CLKSB=0,CLKSA=1,PS2=0,PS1=0,PS0=0 */
	TPM1SC = 0x08;              /* Run the counter (set CLKSB:CLKSA) */ 
	/* PTEPF1: E5=3 */
	PTEPF1 |= 0x0C;

	// SPI Init
	spi_init( 	SPI1_PORT, 
				BAUD_1000, 
				serIDLEshigh, 
				serMiddleSample, 
				serMaster
			  );
	spi_disable_tx_interrupt (SPI1_PORT);
	/**********************FSL: low level start-up****************************/

	// Set GPIO direction
	PTCD_PTCD4 = 0;
	PTCDD_PTCDD4 = 1;
	
	// Setup the core ticker
	/* 1KHz clock. */
	RTCSC |= 8;
	
#define TICK_RATE_HZ          ( ( u32_t ) 2000 )
#define RTC_CLOCK_HZ		  ( ( u32_t ) 1000 )
	
	RTCMOD = RTC_CLOCK_HZ / TICK_RATE_HZ;
	
	/* Enable the RTC to generate interrupts - interrupts are already disabled
	when this code executes. */
	RTCSC_RTIE = 1;
	
	Cpu_EnableInt()
    
    /* please make sure that you never leave main */
    for(;;)
    ;
}
