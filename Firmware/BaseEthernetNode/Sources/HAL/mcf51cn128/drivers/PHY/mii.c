/*
 * File:    mii.c
 * Purpose:     
 *
 * Notes:       
 */
#include "cf_board.h"
#include "mii.h"

/*FSL:printf prototype*/
INT
printf (const CHAR *fmt, ...);

/********************************************************************/

#if PHY_ON_CHIP

//FSL MII_write only used in SoftEthernetNegotiation() function
//FSL MII_read used in the Int_handlers.c, for status information
//FSL 	and SoftEthernetNegotiation() function

/**
 * Start internal PHY module
 * @param none  
 * @return none
 */
void 
PHY_init(void)
{
	uint32 		myctr; 					//generic counter variable
	uint16 		mymrdata, mymwdata;    	//temp variable for MII read/write data
  uint16		reg0, reg1, reg4;


	//FSL replace function call	fec_mii_init((SYSTEM_CLOCK));
    /*
     * Configure MII interface speed. Must be <= 2.5MHz
     *
     * Desired MII clock is 2.5MHz
     * MII Speed Setting = System_Clock_Bus_Speed / (2.5MHz * 2)
     */
    /*already configured*/
    //MCF_FEC_MSCR = MCF_FEC_MSCR_MII_SPEED((uint32)(SYS_CLK_MHZ/5));

  	// set phy address to zero
  	EPHYCTL1 = EPHYCTL1_PHYADD(FEC_PHY0);

  	//Enable EPHY module with PHY clocks disabled
  	//Do not turn on PHY clocks until both FEC and EPHY are completely setup (see Below)
  	EPHYCTL0 = (uint8)(EPHYCTL0  & ~(EPHYCTL0_DIS100 | EPHYCTL0_DIS10)); 

  	//Disable auto_neg at start-up
  	EPHYCTL0 = (uint8)(EPHYCTL0 | (EPHYCTL0_ANDIS));

  	//Enable EPHY module
  	EPHYCTL0 = (uint8)(EPHYCTL0_EPHYEN | EPHYCTL0);

		// Force ePHY to manual, 100mbps, Half Duplexe
		(void)MII_read(0, 0, &reg0);
		reg0 |= 0x2000;								// 100Mbps
		reg0 &= ~0x0100;							// Half Duplexe
		reg0 &= ~0x1000;							// Manual Mode	
		(void)MII_write( 0, 0, reg0 );
//		(void)MII_write( 0, 0, (reg0|0x0200) ); // Force re-negotiate

	for (myctr=10000; myctr >0; myctr--)
	; /*delay*/

	//*****************************************************************************
	//
	// Work-around for bug in hardware autonegotiation.
	// Attempt to connect at 100Mbps - Half Duplexe
	// Wait for seconds
	// Attempt to connect at 10Mbps - Half Duplexe
	// 
	// Returns 10, or 100 on success, 0 on failure
	//*****************************************************************************

	// Force ePHY to manual, 100mbps, Half Duplex
	while( !MII_read(0, 0, &reg0) )
	;
	reg0 |= 0x2000;									// 100Mbps
	reg0 &= ~0x0100;								// Half Duplexe
	reg0 &= ~0x1000;								// Manual Mode	
	while( !MII_write( 0, 0, reg0 ) ){};
	while( !MII_write( 0, 0, (reg0|0x0200) )){};// Force re-negotiate 
	
	for( myctr=400000; myctr; myctr-- )
	{
		(void)MII_read(0, 1, &reg1);
		if( reg1 & 0x0004 )
		{
//			printf( "\nLink UP - 100 HD" );				
			return;
		}
	}
	
	// Force ePHY to manual, 10mbps, Half Duplexe
	while( !MII_read(0, 0, &reg0) )
	;
	reg0 &= ~0x2000;								// 10Mbps
	reg0 &= ~0x0100;								// Half Duplexe
	reg0 &= ~0x1000;								// Manual Mode	
	while( !MII_write( 0, 0, reg0 ) )
	;
	while( !MII_write( 0, 0, (reg0|0x0200) ))
	;/*Force re-negotiate*/
	
//	printf("\nLink DOWN" );
	
	return;
}

#endif

/********************************************************************/
/*
 * Write a value to a PHY's MII register.
 *
 * Parameters:
 *  phy_addr    Address of the PHY.
 *  reg_addr    Address of the register in the PHY.
 *  data        Data to be written to the PHY register.
 *
 * Return Values:
 *  0 on failure
 *  1 on success.
 *
 * Please refer to your PHY manual for registers and their meanings.
 * mii_write() polls for the FEC's MII interrupt event and clears it. 
 * If after a suitable amount of time the event isn't triggered, a 
 * value of 0 is returned.
 */
uint8
MII_write(int phy_addr, int reg_addr, int data)
{
    int timeout;
    uint32 eimr;

    /* Clear the MII interrupt bit */
    EIR_MII = 1;

    /* Mask the MII interrupt */
    eimr = EIMR;
    EIMR_MII = 0;

    /* Write to the MII Management Frame Register to kick-off the MII write */
    MMFR = (vuint32)(0
        | FEC_MMFR_ST_01
        | FEC_MMFR_OP_WRITE
        | FEC_MMFR_PA(phy_addr)
        | FEC_MMFR_RA(reg_addr)
        | FEC_MMFR_TA_10
        | FEC_MMFR_DATA(data));

    /* Poll for the MII interrupt (interrupt should be masked) */
    for (timeout = 0; timeout < FEC_MII_TIMEOUT; timeout++)
    {
        if (EIR_MII)
            break;
    }
    if(timeout == FEC_MII_TIMEOUT)
        return 0;

    /* Clear the MII interrupt bit */
    EIR_MII = 1;

    /* Restore the EIMR */
    EIMR = eimr;

    return 1;
}
/********************************************************************/
/*
 * Read a value from a PHY's MII register.
 *
 * Parameters:
 *  phy_addr    Address of the PHY.
 *  reg_addr    Address of the register in the PHY.
 *  data        Pointer to storage for the Data to be read
 *              from the PHY register (passed by reference)
 *
 * Return Values:
 *  0 on failure
 *  1 on success.
 *
 * Please refer to your PHY manual for registers and their meanings.
 * mii_read() polls for the FEC's MII interrupt event and clears it. 
 * If after a suitable amount of time the event isn't triggered, a 
 * value of 0 is returned.
 */
uint8
MII_read(int phy_addr, int reg_addr, uint16* data)
{
    int timeout;
    uint32 eimr;

    /* Clear the MII interrupt bit */
    EIR_MII = 1;

    /* Mask the MII interrupt */
    eimr = EIMR;
    EIMR_MII = 0;

    /* Write to the MII Management Frame Register to kick-off the MII read */
    MMFR = (vuint32)(0
        | FEC_MMFR_ST_01
        | FEC_MMFR_OP_READ
        | FEC_MMFR_PA(phy_addr)
        | FEC_MMFR_RA(reg_addr)
        | FEC_MMFR_TA_10);

    /* Poll for the MII interrupt (interrupt should be masked) */
    for (timeout = 0; timeout < FEC_MII_TIMEOUT; timeout++)
    {
        if (EIR_MII)
            break;
    }

    if(timeout == FEC_MII_TIMEOUT)
        return 0;

    /* Clear the MII interrupt bit */
    EIR_MII = 1;

    /* Restore the EIMR */
    EIMR = eimr;

    *data = (uint16)(MMFR & 0x0000FFFF);

    return 1;
}
/********************************************************************/