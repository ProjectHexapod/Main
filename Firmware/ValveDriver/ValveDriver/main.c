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
2:  Desired PWM duty cycle, channel 2
3:  Desired PWM duty cycle, channel 3
4:  Desired PWM duty cycle, channel 4
5:  Desired PWM duty cycle, channel 5
********/
unsigned char m_to_s_mem[32];
/********
s_to_m_memory map

********/
unsigned char s_to_m_mem[32];

extern BYTE DELSIG8_bfStatus;
extern BYTE DELSIG8_cResult;

#define PWM_0_PORT	PRT0DR
#define PWM_0_PIN	0x80
#define NOTPWM_0_PIN 0x7F
#define SET_PWM_0   PWM_0_PORT |= PWM_0_PIN
#define UNSET_PWM_0 PWM_0_PORT &= NOTPWM_0_PIN
#define PWM_1_PORT	PRT0DR
#define PWM_1_PIN	0x20
#define PWM_2_PORT	PRT0DR
#define PWM_2_PIN	0x08
#define PWM_3_PORT	PRT0DR
#define PWM_3_PIN	0x02
#define PWM_4_PORT	PRT2DR
#define PWM_4_PIN	0x80
#define PWM_5_PORT	PRT2DR
#define PWM_5_PIN	0x20

unsigned char pwm_count;

void main(void)
{
	// Insert your main routine code here.
	unsigned char c = 0;
	M8C_EnableGInt;
	UART_EnableInt();
	UART_Start(UART_PARITY_NONE);
	for(pwm_count = 0; 1; pwm_count++)
	{
		if( pwm_count < m_to_s_mem[0] )
			PWM_0_PORT |=  PWM_0_PIN;
		else
			PWM_0_PORT &= ~PWM_0_PIN;
		if( pwm_count < m_to_s_mem[1] )
			PWM_1_PORT |=  PWM_1_PIN;
		else
			PWM_1_PORT &= ~PWM_1_PIN;
		if( pwm_count < m_to_s_mem[2] )
			PWM_2_PORT |=  PWM_2_PIN;
		else
			PWM_2_PORT &= ~PWM_2_PIN;
		if( pwm_count < m_to_s_mem[3] )
			PWM_3_PORT |=  PWM_3_PIN;
		else
			PWM_3_PORT &= ~PWM_3_PIN;
		if( pwm_count < m_to_s_mem[4] )
			PWM_4_PORT |=  PWM_4_PIN;
		else
			PWM_4_PORT &= ~PWM_4_PIN;
		if( pwm_count < m_to_s_mem[5] )
			PWM_5_PORT |=  PWM_5_PIN;
		else
			PWM_5_PORT &= ~PWM_5_PIN;
		if(pwm_count == 16)
			pwm_count = 0; 
	}
}
