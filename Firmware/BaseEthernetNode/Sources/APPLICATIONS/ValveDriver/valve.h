#ifndef _VALVE_
#define _VALVE_

// This is the value at which the PWM wraps.
// Period of PWM becomes 41ns*PWM_MODULO_COUNT
#define PWM_MODULO_COUNT 0x0800
#define RECV_BUFFSIZE 32
#define NO_DATA_TICKS_THRESHOLD 50

/**
 * Valve task
 *
 * @param none  
 * @return none
 */
void
VALVE_Task( void *pvParameters );

#endif