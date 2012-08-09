#ifndef __MCU_INIT_H__
#define __MCU_INIT_H__

/**
 * set stack state
 *
 * @param TRUE if ready, otherwise FALSE 
 * @return none
 */
void 
set_lwip_ready(uint8 ready);

/**
 * get stack state
 *
 * @param none
 * @return TRUE if ready, otherwise FALSE
 */
uint8 
get_lwip_ready(void);

/**
 * get interface state, if ip is already configured
 *
 * @param none 
 * @return 1 if interface is up, otherwise zero
 */
uint8 
lwip_interface_is_up(void);

/**
 * starts lwip tcp/ip stack
 *
 * @param none 
 * @return none
 */
void
vlwIPInit( void );

/**
 * Low level call to init hardware
 *
 * @param none 
 * @return none
 */
void 
MCU_startup();

/**
 * set targeted MCU
 *
 * @param none
 * @return none
 */
void
MCU_reset(void);

#endif