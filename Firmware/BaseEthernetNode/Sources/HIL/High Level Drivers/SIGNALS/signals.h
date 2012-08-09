#ifndef _SIGNALS_H_
#define _SIGNALS_H_

#include "gpio.h"

#define LED_toogle_init()        LED_VALUE_INIT;
#define LED_toggle()             LED_VALUE = ~LED_VALUE;

#endif