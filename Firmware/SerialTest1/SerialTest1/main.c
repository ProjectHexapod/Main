//----------------------------------------------------------------------------
// C main line
//----------------------------------------------------------------------------

#include <m8c.h>        // part specific constants and macros
#include "PSoCAPI.h"    // PSoC API definitions for all User Modules

unsigned char target_address;
unsigned char bytes_received = 0;
unsigned char expected_bytes;

unsigned char ext_mem_locked = 0;
unsigned char m_to_s_offset = 0;
/********
m_to_s_memory map
0:  Desired PWM duty cycle
********/
unsigned char m_to_s_mem[32];
/********
s_to_m_memory map
0:  Low  byte, ADC in
1:  High byte, ADC in
********/
unsigned char s_to_m_mem[32];

extern BYTE DELSIG8_bfStatus;
extern BYTE DELSIG8_cResult;

void main(void)
{
	// Insert your main routine code here.
	unsigned char c = 0;
	M8C_EnableGInt;
	UART_EnableInt();
	UART_Start(UART_PARITY_NONE);
	PGA_1_Start(PGA_1_HIGHPOWER);
	//DELSIG8_Start( DELSIG8_HIGHPOWER );
	//DELSIG8_StartAD();
	ADCINC_Start(ADCINC_HIGHPOWER); // Apply power to the SC Block
	ADCINC_GetSamples(0);
	PWM8_DisableInt();
	PWM8_Start();
	for(;;)
	{
		PWM8_WritePulseWidth(m_to_s_mem[0]);
		//if ( DELSIG8_bfStatus ) {
		//	DELSIG8_bfStatus = 0;
		//	s_to_m_mem[0] = DELSIG8_cResult;
		//}
		//ADCINC_GetSamples(1);
		//while(ADCINC_fIsDataAvailable() == 0);
		//s_to_m_mem[0] = ADCINC_bClearFlagGetData(); 
	}
	//mainloop:
	//	UART_SendData(temp++);
		//while( ++temp2 );
	//goto mainloop;
}
