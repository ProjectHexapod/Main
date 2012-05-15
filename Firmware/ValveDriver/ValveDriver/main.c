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
0:  Desired PWM duty cycle, channel 0
1:  Desired PWM duty cycle, channel 1
********/
unsigned char m_to_s_mem[32];
/********
s_to_m_memory map

********/
unsigned char s_to_m_mem[32];

void main(void)
{
	M8C_EnableGInt;
	UART_EnableInt();
	UART_Start(UART_PARITY_NONE);
	PWM8_1_DisableInt();
	PWM8_1_Start();
	PWM8_2_DisableInt();
	PWM8_2_Start();
	while(1)
	{
		PWM8_1_WritePulseWidth(m_to_s_mem[0]);
		PWM8_2_WritePulseWidth(m_to_s_mem[1]);
	}
}
