//----------------------------------------------------------------------------
// C main line
//----------------------------------------------------------------------------

#include <m8c.h>        // part specific constants and macros
#include "PSoCAPI.h"    // PSoC API definitions for all User Modules

unsigned char selected_address;

void processData( unsigned char data_in )
{
	return;
}

void main(void)
{
	// Insert your main routine code here.
	unsigned char temp = 0;
	volatile unsigned short temp2 = 0;
	M8C_EnableGInt ; // Uncomment this line to enable Global Interrupts
	UART_EnableInt();
	UART_Start(UART_PARITY_EVEN);
	while(1);
	//mainloop:
	//	UART_SendData(temp++);
		//while( ++temp2 );
	//goto mainloop;
}
