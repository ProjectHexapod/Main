#ifndef _MAG_ENC_
#define _MAG_ENC_

#define SPI_BUFFER_LIMIT 			16
#define MAG_ENC_TASK_PRIORITY      ( tskIDLE_PRIORITY + 4 )
#define VALVE_TASK_PRIORITY      ( tskIDLE_PRIORITY + 4 )

/**
 * Mag Enc task
 *
 * @param none  
 * @return none
 */
void
MAG_ENC_Task( void *pvParameters );

#endif