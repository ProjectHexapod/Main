/* ------------------------ Platform includes ----------------------------- */
#include "cf_board.h"
#include "gpio.h"

/**
 * Configure FEC pins to selected pins
 * @param none  
 * @return none
 */
void 
GPIO_FECPinsInit(void)
{
  /*FSL:FEC init*/
  
  //Enable MII TX[0:3] TX_EN, MDC and MDIO pins to full drive.
  PTBDS = 0b00000110; /* Output Drive Enable for Port A*/
  PTBDS = 0b11110100; /* Output Drive Enable for Port B*/

  //Turn off input filtering: first Si
  PTAIFE = 0;
  PTBIFE = 0;
  PTCIFE = 0;
    
  //port A
  PTAPF1 = 0b01010101;
  PTAPF2 = 0b01010100;
  //port B
  PTBPF1 = 0b01010101;
  /*Note for EVB, Tower and copacabana*/
  PTBPF2 = 0b01000101;//PTB2 is not used for MII_TX_ER: available for GPIO
  //port C
  PTCPF2_C0 = 0b01;
  PTCPF2_C1 = 0b01;
  PTCPF2_C2 = 0b01;

#if MCU_FED_PHY_CLK
  /*PHY clock generator*/
  PTAPF2_A0 = 0b01;   // PHY clk pin out
  SOPT3_PCS = 0b01;   //OSC out: PHY feeds from OSC output
#endif
}

/**
 * Configure ADC pins to selected pin
 * @param adc channel 
 * @return none
 */
void
GPIO_ADCPinsInit(uint8 adc_channel)
{
  switch(adc_channel)
  {
    case 0:
     PTEPF2_E2 = 3;//ADP0
     break;
    case 1:
     PTEPF2_E1 = 3;//ADP1
     break;
    case 2:
     PTEPF2_E0 = 3;//ADP2
     break;
    case 3:
     PTDPF1_D7 = 3;//ADP3
     break;
    case 4:
     PTDPF2_D3 = 3;//ADP4
     break;
    case 5:
     PTDPF2_D2 = 3;//ADP5
     break;
    case 6:
     PTDPF2_D1 = 3;//ADP6
     break;
    case 7:
     PTDPF2_D0 = 3;//ADP7
     break;
    case 8:
     PTCPF1_C7 = 3;//ADP8
     break;
    case 9:
     PTCPF1_C6 = 3;//ADP9
     break;
    case 10:
     PTCPF1_C5 = 3;//ADP10
     break;
    case 11:
     PTCPF1_C4 = 3;//ADP11
     break;  
  }
}

/**
 * Configure MCU pins to low power mode
 * @param none  
 * @return none
 */
void 
GPIO_MCUPinsInit()
{   
    //disable pull up
    PTAPE = PTBPE = PTCPE = PTDPE = PTEPE = PTFPE = PTGPE = PTHPE = PTJPE = 0x00;
     
    //disable slew control
    PTASE = PTBSE = PTCSE = PTDSE = PTESE = PTFSE = PTGSE = PTHSE = PTJSE = 0x00;
    
    //enable low drive strength
    PTADS = PTBDS = PTCDS = PTDDS = PTEDS = PTFDS = PTGDS = PTHDS = PTJDS = 0x00;    
    
    //Turn off input filtering
    PTAIFE = PTBIFE = PTCIFE = PTDIFE = PTEIFE = PTFIFE = PTGIFE = PTHIFE = PTJIFE = 0;
    
    //set all I/O in general I/O mode
    PTAPF1 = PTAPF2 = PTBPF1 = PTBPF2 = PTCPF1 = PTCPF2 = PTDPF1 = PTDPF2 = PTEPF1 = 0;
    PTEPF2 = PTFPF1 = PTFPF2 = PTGPF1 = PTGPF2 = PTHPF1 = PTHPF2 = PTJPF1 = PTJPF2 = 0;
    
    //set all pin in output mode
    PTADD = PTBDD = PTCDD = PTDDD = PTEDD = PTFDD = PTGDD = PTHDD = PTJDD = 0xFF;
    
    //clear output
    PTAD = PTBD = PTCD = PTDD = PTED = PTFD = PTGD = PTHD = PTJD = 0x00;
}