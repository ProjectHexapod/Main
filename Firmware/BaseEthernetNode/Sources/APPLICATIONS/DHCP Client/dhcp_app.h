#ifndef _DHCP_APP_H_
#define _DHCP_APP_H_

#define EMAIL_NOTIFICATION_AFTER_GETTING_IP_ADDRESS   1
#define DHCP_TASK_PRIORITY                            1
#define LED_TASK_PRIORITY                             1

/**
 * DHCP Task: request an IP address after reset
 *
 * @param ethernet descriptor
 * @return none
 */
void
vDHCPClient( void *pvParameters );

/**
 * Toggle LED Task: alive function
 *
 * @param none
 * @return none
 */
void
vToggleLED( void *pvParameters );

#endif

