/*
  Low_Power.c
*/

#include <hidef.h> /* for EnableInterrupts macro */
#include "cf_board.h"
#include "clock.h"
#include "gpio.h"

/**
 * Generic MCU Low Level Init
 * @param none
 * @return none
 */
void 
MCU_init()
{
  /* Is this Reset an exit from Stop 2? */
  if(SPMSC2_PPDF)
  {
     SPMSC2_PPDACK = 1;
  }

  /*off-chip accesses are disalowed by minibus*/
  /*stop not enabled*/
  /*wait not enabled*/
  /*cop enabled with 1KHz clock. Timeout = 256ms*/
  
  /*FSL: regular start-up*/
  low_power_init(RUN_MODE);
  
  /*FSL:turning off pins*/
  //GPIO_MCUPinsInit();

  /*FSL:quick fix for the P&E pod at high freq: 1st Si*/
  BKGD_WORKAROUND;
  
  //CLOCK_OSC_OUT_INIT;
  
#ifndef EXTERNAL_CLOCK
  prvSetupInternal_32kHzOsc();
#else  
  prvSetupExternal_25MHzCrystal();
#endif
    
  DEMO_SELECTOR_INIT;/*startup line*/
  
  /*FSL: disable all system clocks*/
  //disable_all_clocks();
  
  /*FSL: avoid reset on exceptions at runtime*/
  /*reset wont occur if using BDM tool*/ 
//#warning "reset disabled"
  //mcf5xxx_wr_cpucr(0xC0000000);

  EnableInterrupts; /* enable interrupts */
}

/**
 * Reset MCF51CN128
 * @param none
 * @return none
 */
MCU_low_level_reset()
{
   /*MCF51CN128 doesn't have a direct reset asm by software*/
   mcf5xxx_reset();
   //SRS = 0;
   //asm("loop:  bra loop");
}

/**
 * Disable modules clocks
 * @param none
 * @return none
 */
void 
disable_all_clocks()
{
    /*turning off unused peripherals*/
    SCGC1=0x00;       
    SCGC2=0x00; 
    SCGC3=0x00;
    SCGC4=0x00;
}

/**
 * Low Power Init
 * @param low power mode enumeration
 * @return none
 */
void 
low_power_init(enum low_power_modes mode)
{
    switch(mode)
    {
      case RUN_MODE:
           /*enable watchdog*/
           SOPT1 = 0/*|SOPT1_COPT1_MASK|SOPT1_COPT0_MASK*/;/*COP off, Minibus access off*///ATX:SOPT1_STOPE_MASK
           SPMSC1 = 0;/*turn off low voltage stuff*/
           SPMSC2 = 0;
        break;
      case LPRUN:
           SOPT1 = 0;/*COP off, Minibus access off*///ATX:SOPT1_STOPE_MASK 
           SPMSC1 = 0;/*turn off low voltage stuff*/
           SPMSC2 = 0 | SPMSC2_LPR_MASK;
        break;             
      case LPWAIT:
           SOPT1 = 0 | SOPT1_WAITE_MASK;/*COP off, Minibus access off, WAIT mode*/
           SPMSC1 = 0 | SPMSC1_LVDE_MASK;
           SPMSC2 = 0 | SPMSC2_LPR_MASK;
        break;
      case NON_STOP:
           SOPT1 = 0;/*COP off, Minibus access off*/
           SPMSC1 = 0 | SPMSC1_LVDE_MASK | SPMSC1_LVDSE_MASK;
           SPMSC2 = 0;
        break;
      /*low power modes needed with stop asm instruction*/  
      case WAIT:
           SOPT1 = 0;/*COP off, Minibus access off, WAIT mode*///ATX: SOPT1_WAITE_MASK
           SPMSC1 = 0 | SPMSC1_LVDE_MASK | SPMSC1_LVDSE_MASK;//ATX:0
           SPMSC2 = 0;
        break;         
      case STOP4:
           SOPT1 = 0 | SOPT1_STOPE_MASK;/*COP off, Minibus access off, STOP mode*/
           SPMSC1 = 0;/*turn off low voltage stuff*///ATX: 0x0C
           SPMSC2 = 0;//ATX: 0x02
        break;
      case STOP3:
           /* Disable Reset Pin */
           /* Disable BKGD Pin to turn off the debugger */
           /* Enable the stop instruction */
           SOPT1 = SOPT1_STOPE_MASK;//this must be the first line of code           
           /* Disable LVD to get lowest power mode */
           SPMSC1 = SPMSC1_LVDE_MASK;
           /* Enable Partial Power Down (select stop2) */
           SPMSC2_PPDC = 0;
        break;
      case STOP2:
           /* Disable Reset Pin */
           /* Disable BKGD Pin to turn off the debugger */
           /* Enable the stop instruction */
           SOPT1 = SOPT1_STOPE_MASK;//this must be the first line of code      
           /* Disable LVD to get lowest power mode */
           //SPMSC1 = SPMSC1_LVDE_MASK;
           SPMSC1_LVDE = 0;
           /* Enable Partial Power Down (select stop2) */
           //SPMSC2 = SPMSC2_PPDE_MASK|SPMSC2_PPDC_MASK;
           SPMSC2_PPDE = 1;
           SPMSC2_PPDC = 1;          
        break;                               
    }
}

/********************************************************************/
/*            Setup for system clock internal 32kHz Osc              /
/********************************************************************/
/**** Moving from FEI (FLL engaged internal) */ 

static void 
prvSetupInternal_32kHzOsc (void)
{
    MCGC2 = 0;   // clear Bdiv bit

    /* Select the internal 32768Hz reference clock. */
    MCGC1 = (0b01<<6)           // CLKS = 01 -> internal reference clock
          | (1 << 2)
          | MCGC1_IRCLKEN_MASK  // IRCLK to RTC enabled
          ;
      
    /* switch from FEI to FBI (FLL bypassed Internal) */ 
    while( !MCGSC_IREFST )      // wait for Reference Status bit to update
    ;
    /* 50.3MHz. */
    
    MCGC4 = (0b10<<0);      // 0b10 = FLL by 1536 = 50331648 Hz
    while( MCGC4_DRST_DRS | MCGSC_LOCK )// wait for DCO to effect
    ;                                   // and for FLL to lock
    
    /* Select FLL output. */
    MCGC1_CLKS  = 0b00;
    while( MCGSC_CLKST != 0x00 )
    ;
    // FEI mode entered again with new freq.
}
/********************************************************************/
/*            Setup for system clock External 25MHz PHY clock       /
/********************************************************************/
/**** Moving from FEI (FLL engaged internal) to 
                  PEE (PLL engaged external) mode. */ 

static void 
prvSetupExternal_25MHzOsc (void)
{

    EXTAL_PIN_INIT;

    /* switch from FEI to FBE (FLL bypassed external) */ 
    /* enable external clock source */

    MCGC2 = MCGC2_ERCLKEN_MASK  // activate external reference clock
          | MCGC2_RANGE_MASK;   // high range  
            
    /* select clock mode */
    MCGC1 = (0b10<<6)           // CLKS = 10 -> external reference clock
          | (0b100<<3)          // RDIV = 2^4 -> 25MHz/16 = 1.5625 MHz
          | MCGC1_IRCLKEN_MASK; // IRCLK to RTC enabled
          // also clear IREFs
      
    /* wait for mode change to be done */
    while (MCGSC_IREFST | (MCGSC_CLKST != 0b10)) // wait for Reference Status bit to update
    ;                                            // and for clock status bits to update 

    /* switch from FBE to PBE (PLL bypassed internal) mode */
    MCGC3 =  (0b1000<<0)        // set PLL multi 50MHz
          |  MCGC3_PLLS_MASK;   // select PLL

    while (!MCGSC_PLLST | !MCGSC_LOCK) /* wait for PLL status bit to update */
    ;   /* Wait for LOCK bit to set */

    /* Now running PBE Mode */
    /* finally switch from PBE to PEE (PLL enabled external mode) */
    MCGC1_CLKS  = 0b00; // PLL clock to system (MCGOUT)

    /* Wait for clock status bits to update */
    while (MCGSC_CLKST != 0b11)           
    ;
}
/********************************************************************/
/*            Setup for system clock External 25MHz Crystal          /
/********************************************************************/
/**** Moving from FEI (FLL engaged internal) to 
                  PEE (PLL engaged external) mode. */ 

static void 
prvSetupExternal_25MHzCrystal (void)
{

    EXTAL_PIN_INIT;
    XTAL_PIN_INIT;

  /* switch from FEI to FBE (FLL bypassed external) */ 
  /* enable external clock source */

    MCGC2 = MCGC2_ERCLKEN_MASK  // activate external reference clock
          | MCGC2_EREFS_MASK    // because crystal is being used
          | MCGC2_RANGE_MASK;   // high range  
            
    /* select clock mode */
    MCGC1 = (0b10<<6)           // CLKS = 10 -> external reference clock
          | (0b100<<3)          // RDIV = 2^4 -> 25MHz/16 = 1.5625 MHz
          | MCGC1_IRCLKEN_MASK; // IRCLK to RTC enabled
          // also clear IREFs
      
    /* wait for mode change to be done */
    while (MCGSC_IREFST | (MCGSC_CLKST != 0b10)) // wait for Reference Status bit to update
    ;                                            // and for clock status bits to update 

    /* switch from FBE to PBE (PLL bypassed internal) mode */
    MCGC3 =  (0b1000<<0)        // set PLL multi 50MHz
          |  MCGC3_PLLS_MASK;   // select PLL

    while (!MCGSC_PLLST | !MCGSC_LOCK) /* wait for PLL status bit to update */
    ;   /* Wait for LOCK bit to set */

    /* Now running PBE Mode */
    /* finally switch from PBE to PEE (PLL enabled external mode) */
    MCGC1_CLKS  = 0b00; // PLL clock to system (MCGOUT)

    /* Wait for clock status bits to update */
    while (MCGSC_CLKST != 0b11)           
    ;
}
/********************************************************************/
/*            Setup for system clock External 32kHz Crystal          /
/********************************************************************/
/**** Moving from FEI (FLL engaged internal) to 
                  PEE (PLL engaged external) mode. */ 

static void 
prvSetupExternal_32kHzCrystal (void)
{

    EXTAL_PIN_INIT;
    XTAL_PIN_INIT;

  /* switch from FEI to FBE (FLL bypassed external) */ 
  /* enable external clock source */

    MCGC2 = MCGC2_ERCLKEN_MASK  // activate external reference clock
          | MCGC2_EREFS_MASK;    // because crystal is being used
          
  
    /* select clock mode */
    MCGC1 = (0b10<<6);           // CLKS = 10 -> external reference clock
      
    /* wait for mode change to be done */
    while (MCGSC_IREFST | (MCGSC_CLKST != 0b10)) // wait for Reference Status bit to update
    ;                                            // and for clock status bits to update 

    MCGC4 = (0b10<<0);           // 0b10 = FLL by 1536 = 50331648 Hz

    while (MCGC4_DRST_DRS | MCGSC_LOCK)  // wait for DCO to effect
     ;                                   // and for FLL to lock
    MCGC1_CLKS  = 0b00;   // switch to FLL
    ;   /* Wait for LOCK bit to set */

}
/*-----------------------------------------------------------*/
