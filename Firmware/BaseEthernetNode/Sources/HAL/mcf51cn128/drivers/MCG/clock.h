/*
  clock.h
*/

#ifndef __CLOCK_H__
#define __CLOCK_H__

#include "cf_board.h"

enum low_power_modes
{
    RUN_MODE,
    LPRUN,
    WAIT,
    LPWAIT,
    NON_STOP,
    STOP4,
    STOP3,
    STOP2
};

#define ENABLE_MUX_CONTROL     SCGC4_MC = 1;//enable
/*write code that changes pin function HERE!!!*/
#define DISABLE_MUX_CONTROL    //////SCGC4_MC = 0;//disable
//#warning "Turn-off-mux-control definition is turned off to have compatibility 
//between all the tests, uncomment it to have a real low power approach!!!"


/**
 * Generic MCU Low Level Init
 * @param none
 * @return none
 */
void 
MCU_init();

/**
 * Reset MCF51CN128
 * @param none
 * @return none
 */
MCU_low_level_reset();

/**
 * Disable modules clocks
 * @param none
 * @return none
 */
void 
disable_all_clocks();

/**
 * Low Power Init
 * @param low power mode enumeration
 * @return none
 */
void 
low_power_init(enum low_power_modes mode);
/********************************************************************/
/*                        Setup for system clock                     /
/********************************************************************/
static void 
prvSetupInternal_32kHzOsc (void);

/********************************************************************/
/*            Setup for system clock External 25MHz PHY clock       /
/********************************************************************/
/**** Moving from FEI (FLL engaged internal) to 
                  PEE (PLL engaged external) mode. */ 
static void 
prvSetupExternal_25MHzOsc (void);

/********************************************************************/
/*            Setup for system clock External 25MHz Crystal          /
/********************************************************************/
/**** Moving from FEI (FLL engaged internal) to 
                  PEE (PLL engaged external) mode. */ 
static void 
prvSetupExternal_25MHzCrystal (void);

/*******************************************************************/
/*            Setup for system clock External 32kHz Crystal          /
/********************************************************************/
/**** Moving from FEI (FLL engaged internal) to 
                  PEE (PLL engaged external) mode. */ 
static void 
prvSetupExternal_32kHzCrystal (void);

#endif