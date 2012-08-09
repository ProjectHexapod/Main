/*
 * File:
 *
 * Notes:       
 *              
 */
#include "cf_board.h"
#include "uart.h"
#include "gpio.h"

//global variable to contain callbacks for UART tx/rx:
static SCI_CallbackType sci_callback[2];//0: rx, 1: tx

/**
 * Start SCI controller in UART mode
 * @param port number
 * @param baudrate   
 * @param parity
 * @param number of bits
 * @param number of stop bits
 * @param flow control: hw, sw or none 
 * @return none
 */
void 
uart_init(uint8 port, uint32 baud, uint8 parity, uint8 bits, uint8 stop_bit, uint8 flow_control) 
{
	/*
	 * Initialize all three UARTs for serial communications
	 */
	register uint16 ubgs;
	   
  switch(port)
  {
    case SCI1_PORT:
      //Enable pins:
      
      /*SCI function*/
      UART1_TX_RX_INIT;

      /*starting SCI clock*/
      SCGC1_SCI1 = 1;

    	/*
    	 * Calculate baud settings
    	 */
    	ubgs = (uint16)((SYSTEM_CLOCK)/(baud * 16));
    	    	 
    	SCI1BDH = (uint8)((ubgs & 0xFF00) >> 8);
    	SCI1BDL = (uint8)(ubgs & 0x00FF);
    
      /*clearing register*/
      SCI1C1 = NULL;

      /*parity*/
      if(!parity )
      {
        /*parity disabled*/      
        SCI1C1_PE = 0;
      }
      else
      {
        /*parity enabled*/      
        SCI1C1_PE = 1;
        
        if(parity==1)//odd
        {
          SCI1C1_PT = 1;
        }
        else //even
        {
          SCI1C1_PT = 0;
        }
      }
      
      /*bits length*/
      if(bits == 4)
      {
         /*9 bits */
         SCI1C1_M = 1; 
      }
      else//8 bits
      {
         SCI1C1_M = 0;
      }
            
      /*stop bit*/
      /*not available on Lasko*/      
      
      /*flow control*/
      if(flow_control == FLOW_CONTROL_HARDWARE)
      {         
         DEMO_SELECTOR_ON;/*startup line*/
         
         //CTS:
         UART1_CTS_INIT;
         //RTS:
         UART1_RTS_INIT;
      }
      
      /* Receiver interrupt enable. Transmitter and receiver enable */
      SCI1C2 = (0
               | SCI1C2_TE_MASK
               | SCI1C2_RE_MASK
               );
      /* Enable all errors interrupts */  
      SCI1C3 = 0;//SCI1C3_ORIE_MASK | SCI1C3_NEIE_MASK | SCI1C3_FEIE_MASK | SCI1C3_PEIE_MASK;

    	break;
    case SCI2_PORT:
      //Enable pins:
      
      /*SCI function*/
      UART2_TX_RX_INIT;    

      /*starting SCI clock*/
      SCGC1_SCI2 = 1;

    	/*
    	 * Calculate baud settings
    	 */
    	ubgs = (uint16)((SYSTEM_CLOCK)/(baud * 16));
    	    	 
    	SCI2BDH = (uint8)((ubgs & 0xFF00) >> 8);
    	SCI2BDL = (uint8)(ubgs & 0x00FF);
    
      /*clearing register*/
      SCI2C1 = NULL;

      /*parity*/
      if(!parity )
      {
        /*parity disabled*/      
        SCI2C1_PE = 0;
      }
      else
      {
        /*parity enabled*/      
        SCI2C1_PE = 1;
        
        if(parity==1)//odd
        {
          SCI2C1_PT = 1;
        }
        else //even
        {
          SCI2C1_PT = 0;
        }
      }
      
      /*bits length*/
      if(bits == 4)
      {
         /*9 bits */
         SCI2C1_M = 1; 
      }
      else//8 bits
      {
         SCI2C1_M = 0;
      }
            
      /*stop bit*/
      /*not available on Lasko*/      

      /*flow control*/
      if(flow_control == FLOW_CONTROL_HARDWARE)
      {
         //init HW pins to use, this will be needed!!
         /*FSL: not supported on this HW*/ 
      }
      
      /* Receiver interrupt enable. Transmitter and receiver enable */
      SCI2C2 = (0
               | SCI2C2_TE_MASK
               | SCI2C2_RE_MASK
               );
      /* Enable all errors interrupts */  
      SCI2C3 = 0;//SCI2C3_ORIE_MASK | SCI2C3_NEIE_MASK | SCI2C3_FEIE_MASK | SCI2C3_PEIE_MASK;

    	break;
    case SCI3_PORT:
      /*SCI function*/
      UART3_TX_RX_INIT;    

      /*starting SCI clock*/
      SCGC2_SCI3 = 1;

      /*disabling SCI3 interrupt ORing*/
      INTC_ORMR |= (0x20);

    	/*
    	 * Calculate baud settings
    	 */
    	ubgs = (uint16)((SYSTEM_CLOCK)/(baud * 16));
    	    	 
    	SCI3BDH = (uint8)((ubgs & 0xFF00) >> 8);
    	SCI3BDL = (uint8)(ubgs & 0x00FF);
    
      /*clearing register*/
      SCI3C1 = NULL;

      /*parity*/
      if(!parity )
      {
        /*parity disabled*/      
        SCI3C1_PE = 0;
      }
      else
      {
        /*parity enabled*/      
        SCI3C1_PE = 1;
        
        if(parity==1)//odd
        {
          SCI3C1_PT = 1;
        }
        else //even
        {
          SCI3C1_PT = 0;
        }
      }
      
      /*bits length*/
      if(bits == 4)
      {
         /*9 bits */
         SCI3C1_M = 1; 
      }
      else//8 bits
      {
         SCI3C1_M = 0;
      }
            
      /*stop bit*/
      /*not available on Lasko*/      

      /*flow control*/
      if(flow_control == FLOW_CONTROL_HARDWARE)
      {
         //init HW pins to use, this will be needed!!
         /*FSL: not supported on this HW*/ 
      }
      
      /* Receiver interrupt enable. Transmitter and receiver enable */
      SCI3C2 = (0
               | SCI3C2_TE_MASK
               | SCI3C2_RE_MASK
               );
      /* Enable all errors interrupts */  
      SCI3C3 = 0;//SCI3C3_ORIE_MASK | SCI3C3_NEIE_MASK | SCI3C3_FEIE_MASK | SCI3C3_PEIE_MASK;     

    	break;  
  }
}

/**
 * Assign ISR Callback
 * @param port number  
 * @param callback function
 * @return none
 */
void 
uart_assign_call_back(uint8 number, void (*func)(CHAR))
{
    sci_callback[number] = func;
}

/**
 * Get character in while mode with timeout support
 * @param port number  
 * @param returned character
 * @return zero for OK, 1 for timeout return
 */
uint8 
uart_getchar_wait (uint8 channel, int8 *character)
{
 vuint16 timeout = 0x1FF;
 
 switch(channel)
 {
    case SCI1_PORT:
       /* Wait until character has been received */
       while(!SCI1S1_RDRF)
       {
         if(!(timeout--)){return (uint8)-1;}
       }/*wait*/
       *character = SCI1D;
       break;
    case SCI2_PORT:
       /* Wait until character has been received */
       while(!SCI2S1_RDRF)
       {
         if(!(timeout--)){return (uint8)-1;}
       }/*wait*/
       *character = SCI2D;
       break;  
    case SCI3_PORT:
       /* Wait until character has been received */
       while(!SCI3S1_RDRF)
       {
         if(!(timeout--)){return (uint8)-1;}
       }/*wait*/
       *character = SCI3D;
       break;  
 }
 
 return 0;/*no timeout*/
}

/**
 * Get character directly from HW buffer without waiting
 * @param port number  
 * @return returned character
 */
int8 
uart_getchar (uint8 channel)
{
 switch(channel)
 {
    case SCI1_PORT:
       (void)SCI1S1;
       return SCI1D;
       break;
    case SCI2_PORT:
       (void)SCI2S1;
       return SCI2D;
       break;  
    case SCI3_PORT:
       (void)SCI3S1;
       return SCI3D;
       break;  
 }
}

/**
 * Put a character directly to HW buffer without waiting
 * @param port number
 * @param character to send   
 * @return none
 */ 
void 
uart_putchar (uint8 channel, CHAR ch)
{    
 switch(channel)
 {
    case SCI1_PORT:
       (void)SCI1S1; 
       SCI1D = (uint8)ch;               /* Send a character by SCI */
       break;
    case SCI2_PORT:
       (void)SCI2S1;
       SCI2D = (uint8)ch;               /* Send a character by SCI */
       break; 
    case SCI3_PORT:
       (void)SCI3S1;
       SCI3D = (uint8)ch;               /* Send a character by SCI */
       break;  
 }    
}

/********************************************************************/

/**
 * Enable SCI TX interrupts
 * @param port number   
 * @return none
 */ 
void 
uart_enable_tx_interrupt (uint8 channel)
{    
 switch(channel)
 {
    case SCI1_PORT:
       SCI1C2_TIE = 1;
       break;
    case SCI2_PORT:
       SCI2C2_TIE = 1;
       break; 
    case SCI3_PORT:
       SCI3C2_TIE = 1;
       break;  
 } 
}

/**
 * Disable SCI TX interrupts
 * @param port number   
 * @return none
 */ 
void 
uart_disable_tx_interrupt (uint8 channel)
{
 switch(channel)
 {
    case SCI1_PORT:
       SCI1C2_TIE = 0;
       break;
    case SCI2_PORT:
       SCI2C2_TIE = 0;
       break; 
    case SCI3_PORT:
       SCI3C2_TIE = 0;
       break;  
 } 
}

/********************************************************************/

/**
 * Enable SCI RX interrupts
 * @param port number   
 * @return none
 */
void 
uart_enable_rx_interrupt (uint8 channel)
{    
 switch(channel)
 {
    case SCI1_PORT:
       SCI1C2_RIE = 1;
       break;
    case SCI2_PORT:
       SCI2C2_RIE = 1;
       break; 
    case SCI3_PORT:
       SCI3C2_RIE= 1;
       break;  
 } 
}

/**
 * Disable SCI RX interrupts
 * @param port number   
 * @return none
 */
void 
uart_disable_rx_interrupt (uint8 channel)
{    
 switch(channel)
 {
    case SCI1_PORT:
       SCI1C2_RIE = 0;
       break;
    case SCI2_PORT:
       SCI2C2_RIE = 0;
       break; 
    case SCI3_PORT:
       SCI3C2_RIE = 0;
       break;  
 } 
}

/*********************************************************************/

/**
 * Get CTS signal state
 * @param port number   
 * @return none
 */
uint8
uart_get_CTS_state(uint8 port)
{
   if(port == SCI1_PORT)/*only supported for SCI1*/
   {
     return UART1_CTS;/*return CTS state: 0: OK ; 1:stop Tx*/
   }
   else
   {
     return 0; //always OK for the rest of the ports
   }   
}

/**
 * Send stop signal (XOFF or RTS) to stop communication
 * @param port number
 * @param flow control: hw or sw 
 * @return none
 */
void
uart_send_tx_stop(uint8 port, uint8 flow_control)
{
   if( flow_control == FLOW_CONTROL_SOFTWARE )
   {
      uart_putchar(port,UART_XOFF);
   }
   else//FLOW_CONTROL_HARDWARE
   {
      //under construction!!!
      if(port == SCI1_PORT)/*only supported for SCI1*/
      {
         UART1_RTS=1;/*RTS not allowing more data*/
      }  
   }
}

/**
 * Send go signal (XON or RTS) to start communication
 * @param port number
 * @param flow control: hw or sw 
 * @return none
 */
void
uart_send_tx_go(uint8 port, uint8 flow_control)
{
   if( flow_control == FLOW_CONTROL_SOFTWARE )
   {
      uart_putchar(port,UART_XON);
   }
   else//FLOW_CONTROL_HARDWARE
   {
      //under construction!!!
      if(port == SCI1_PORT)/*only supported for SCI1*/
      {
         UART1_RTS=0;/*RTS allowing more data*/
      }      
   }  
}

/*********************************************************************/

#if 0

/**
 * SCI1 ISR Error Processing
 * @param none
 * @return none
 */
static void 
sci_error1_processing(void)
{
   uint8 status;   
   /*clear it*/
   status = SCI1S1;
   /*FSL:no error handling*/
   status = SCI1D;
}

/**
 * SCI2 ISR Error Processing
 * @param none
 * @return none
 */
static void 
sci_error2_processing(void)
{
   uint8 status;   
   /*clear it*/
   status = SCI2S1;
   /*FSL:no error handling*/
   status = SCI2D;
}

/**
 * SCI3 ISR Error Processing
 * @param none
 * @return none
 */
static void 
sci_error3_processing(void)
{
   uint8 status;   
   /*clear it*/
   status = SCI3S1;
   /*FSL:no error handling*/
   status = SCI3D;
}

#endif

/***************  ISRs for RTOS **************/

/**
 * SCI1 ISR TX
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci1tx 
uart1_tx_irq( void )
{
    sci_callback[SCI_TX](SCI1_PORT);
}

/**
 * SCI2 ISR TX
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci2tx 
uart2_tx_irq( void )
{
    sci_callback[SCI_TX](SCI2_PORT);
}

/**
 * SCI3 ISR TX
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci3tx 
uart3_tx_irq( void )
{
    sci_callback[SCI_TX](SCI3_PORT);
}

/***************************** RX ************************************/
/**
 * SCI1 ISR RX
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci1rx
uart1_rx_irq( void )
{
    sci_callback[SCI_RX](SCI1_PORT);
}

/**
 * SCI2 ISR RX
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci2rx
uart2_rx_irq( void )
{
    sci_callback[SCI_RX](SCI2_PORT);
}

/**
 * SCI3 ISR RX
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci3rx 
uart3_rx_irq( void )
{
    sci_callback[SCI_RX](SCI3_PORT);
}

#if 0

/***************************** Error *********************************/
/**
 * SCI1 ISR Error
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci1err 
uart1_error_irq( void )
{
    /* This ISR can cause a context switch, so the first statement must be
     * a call to the portENTER_SWITCHING_ISR() macro.
     */
    sci_error1_processing();
}

/**
 * SCI2 ISR Error
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci2err 
uart2_error_irq( void )
{
    /* This ISR can cause a context switch, so the first statement must be
     * a call to the portENTER_SWITCHING_ISR() macro.
     */
    jsr sci_error2_processing();
}

/**
 * SCI3 ISR Error
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vsci3err 
uart3_error_irq( void )
{
    /* This ISR can cause a context switch, so the first statement must be
     * a call to the portENTER_SWITCHING_ISR() macro.
     */

    jsr sci_error3_processing();                                                  
}

#endif