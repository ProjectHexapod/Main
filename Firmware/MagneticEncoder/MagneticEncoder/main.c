//----------------------------------------------------------------------------
// C main line
//----------------------------------------------------------------------------

#include <m8c.h>        // part specific constants and macros
#include "PSoCAPI.h"    // PSoC API definitions for all User Modules

unsigned char readMagEncConfig(void);

unsigned char target_address;
unsigned char expected_bytes;
unsigned char transfer_offset_valid = 0;
unsigned char transfer_flags, transfer_offset;

unsigned char ext_mem_locked = 0;
/********
m_to_s_memory map
********/
unsigned char m_to_s_mem[32];
/********
s_to_m_memory map
0:  Encoder SIN output bits 8-11
1:  Encoder SIN output bits 0-7
2:  Encoder COS output bits 8-11
3:  Encoder COS output bits 0-7
31: Device type (0xd1=valve driver, 0xe2=angle encoder)
********/
unsigned char s_to_m_mem[32];

#define ANALOG_MUX	AMX_IN	  //  see datasheet pg 103

unsigned char pwm_count;
unsigned int sin_value = 4;
unsigned int cos_value = 5;
unsigned int wait_cycle = 0;

void main(void)
{
    s_to_m_mem[31] = 0xe2;
	
	M8C_EnableGInt;
	UART_EnableInt();
	UART_Start(UART_PARITY_NONE);

	PGA_1_Start(PGA_1_HIGHPOWER);

	//	void  ADCINC_Start (BYTE bPowerSetting)
	ADCINC_1_Start(3);
	ADCINC_1_GetSamples(0);
	s_to_m_mem[0] = 1;
	s_to_m_mem[1] = 2;

	for (;;) {
		//  Set the Analog Mux to SIN
		//  Clear AMX_IN bit 0 to read SIN on P0[1] (header12 pin4)
		ANALOG_MUX &= 0xFE;
		
		//  Read the ADC value
		for(wait_cycle = 0; wait_cycle < 2; wait_cycle++)
		{
			while(ADCINC_1_fIsDataAvailable() == 0)
				;
			sin_value = ADCINC_1_wClearFlagGetData();   //  read garbage data while MUX settles, last one is kept
		}
		
		//  Set the Analog Mux to COS
		//  Set AMX_IN bit 0 to read COS on P0[3] (header12 pin3)
		ANALOG_MUX |= 0x01;
	
		//  Read the ADC value
		for(wait_cycle = 0; wait_cycle < 2; wait_cycle++)
		{
			while(ADCINC_1_fIsDataAvailable() == 0)
				;
			cos_value = ADCINC_1_wClearFlagGetData();   //  read garbage data while MUX settles, last one is kept
		}
	
		s_to_m_mem[0] = (unsigned char)(sin_value >> 8);
		s_to_m_mem[1] = (unsigned char)(sin_value);
		s_to_m_mem[2] = (unsigned char)(cos_value >> 8);
		s_to_m_mem[3] = (unsigned char)(cos_value);
	}
}



/*
unsigned char readMagEncConfig(void)
{
//  read config from AustriaMicroSystems SSI
#define SSI_PORT	PRT1DR  //  Port 1, pins 3, 5 and 7
#define SSI_CS_PIN	0x08
#define SSI_DCLK_PIN	0x20
#define SSI_DIO_PIN	0x80

//	see datasheet pg59			Resistive pullup	Strong Drive
// #define SSI_PORT  PRT1DM2	0					0
// #define SSI_PORT  PRD1DM1	1					0
// #define SSI_PORT  PRD1DM0	1					1

unsigned char clk_counter=0;
unsigned char bitnumber=0;
int counter;
unsigned char DIO_bit_mask = 128;

unsigned char ssi_clk_half_period = 10;
unsigned char read_config = 0b00000111;
unsigned char write_config = 0b00010111;

unsigned char tx_value = 0;

//  raise chip select to begin communicating
//  first clear the clock and IO pins

SSI_PORT &= ~SSI_CS_PIN;
SSI_PORT &= ~SSI_DCLK_PIN;
SSI_PORT &= ~SSI_DIO_PIN;

//  raise the CS pin

SSI_PORT |= SSI_CS_PIN;

//  transmit the "read config" command, the read config code is (I think) 00111

for (counter = 4; counter >= 0; counter--)
	{
	//  set DIO value
	
	DIO_bit_mask = 1 << counter;  // move down through the transmit values

	if (read_config && DIO_bit_mask)
		{
		SSI_PORT |= SSI_DIO_PIN;	// set SSI DIO_PIN;
		}
	else
		{
		SSI_PORT &= ~SSI_DIO_PIN;  // clear SSI_DIO_PIN
		}
			
	//  wait half the clock cycle
	while(clk_counter < ssi_clk_half_period)
		clk_counter++;
	clk_counter = 0;	
	
	//  raise DCLK
	SSI_PORT |= SSI_DCLK_PIN;
	
	//  wait half the clock cycle
	while(clk_counter < ssi_clk_half_period)
		clk_counter++;
	clk_counter = 0;	
	
	//  lower DCLK
	SSI_PORT &= ~SSI_DCLK_PIN;
	
	}


//  the write config code is 10111

//  the remaining 16 bits are read from or written to the peripheral chip


for (counter = 15; counter >= 0; counter--)
	{
	//  clear DIO value, or switch to input mode?
	
	DIO_bit_mask = 1 << counter;  // move down through the transmit values
			
	//  wait half the clock cycle
	while(clk_counter < ssi_clk_half_period)
		clk_counter++;
	clk_counter = 0;	
	
	//  raise DCLK
	SSI_PORT |= SSI_DCLK_PIN;

	if (SSI_PORT && SSI_DIO_PIN)  // if the input value is high, set tx_value bit.
		tx_value |= DIO_bit_mask;
	
	//  wait half the clock cycle
	while(clk_counter < ssi_clk_half_period)
		clk_counter++;
	clk_counter = 0;	
	
	//  lower DCLK
	SSI_PORT &= ~SSI_DCLK_PIN;
	
	}

return tx_value;

}
*/

