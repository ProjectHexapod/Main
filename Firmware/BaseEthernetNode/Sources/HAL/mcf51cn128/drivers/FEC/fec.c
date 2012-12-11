/* ------------------------ Platform includes ----------------------------- */
#include "cf_board.h"
#include "fec.h"
#include "gpio.h"


FEC_CallbackType fec_Callback;

/* ------------------------ Static variables ------------------------------ */

/* Buffer descriptor indexes */
static uint8    tx_bd_idx;
static uint8    rx_bd_idx;

/* Buffer Descriptors -- must be aligned on a 4-byte boundary but a
 * 16-byte boundary is recommended. */
/*FSL*/
/*__relocate_data__*/ static uint8 unaligned_tx_nbuf[(sizeof(nbuf_t)*NUM_TXBDS) + 16];
/*__relocate_data__*/ static uint8 unaligned_rx_nbuf[(sizeof(nbuf_t)*NUM_RXBDS) + 16];

/* Data Buffers -- must be aligned on a 16-byte boundary. */
/*__relocate_data__*/ static uint8  unaligned_rx_buf[(RX_BUFFER_SIZE * NUM_RXBDS) + 16];
/*FSL: workaround to only use 1 tx buffer with two buffer rings*/
/*__relocate_data__*/ static uint8  unaligned_tx_buf[(TX_BUFFER_SIZE * 1) + 16];
/*FSL:variables holding BDs*/

static nbuf_t *tx_nbuf;
static nbuf_t *rx_nbuf;

static uint8  *rx_buf;
static uint8  *tx_buf;

/* ------------------------ Start implementation -------------------------- */

/**
 * Init network buffer descriptor ring
 * @param none
 * @return none
 */
void
NBUF_init(  )
{
  uint8 i;

    /*FSL:init Rx BD ring*/
	rx_nbuf = (nbuf_t *)((uint32)(unaligned_rx_nbuf + 16) & 0xFFFFFFF0);
	rx_buf = (uint8 *)((uint32)(unaligned_rx_buf + 16) & 0xFFFFFFF0);
	
	tx_nbuf = (nbuf_t *)((uint32)(unaligned_tx_nbuf + 16) & 0xFFFFFFF0);
	tx_buf = (uint8 *)((uint32)(unaligned_tx_buf + 16) & 0xFFFFFFF0);

  /* Initialize receive descriptor ring */
  for( i = 0; i < NUM_RXBDS; i++ )
  {
      rx_nbuf[i].status = RX_BD_E;
      rx_nbuf[i].length = 0;
      rx_nbuf[i].data = &rx_buf[i * RX_BUFFER_SIZE];
  }

  /* Set the Wrap bit on the last one in the ring */
  rx_nbuf[NUM_RXBDS - 1].status |= RX_BD_W;

  /* Initialize transmit descriptor ring */
  for( i = 0; i < NUM_TXBDS; i++ )
  {
      tx_nbuf[i].status = TX_BD_L | TX_BD_TC;
      tx_nbuf[i].length = 0;
      tx_nbuf[i].data = &tx_buf[/*FSL: i * TX_BUFFER_SIZE*/0];/*FSL:workaround*/
  }

  /* Set the Wrap bit on the last one in the ring */
  tx_nbuf[NUM_TXBDS - 1].status |= TX_BD_W;

  /* Initialize the buffer descriptor indexes */
  tx_bd_idx = rx_bd_idx = 0;

    return;
}

/**
 * Return the address of the first buffer descriptor in the ring.
 * This routine is needed by the FEC of the MPC860T , MCF5282, and MCF523x
 * in order to write the Rx/Tx descriptor ring start registers
 * @param zero for rx, one for tx
 * @return pointer to buffer index
 */
uint32
NBUF_GetStartBufferPointer( uint8 direction )
{
    switch ( direction )
    {
    case NBUF_RX:
        return ( uint32 ) rx_nbuf;
    case NBUF_TX:
    default:
        return ( uint32 ) tx_nbuf;
    }
}

/**
 * Allocate a rx buffer indisde buffer descriptor ring
 * @param none
 * @return pointer to buffer to get. NULL for no buffer available
 */
nbuf_t         *
NBUF_AllocRX( )
{
    /* This routine alters shared data. Disable interrupts! */
    uint8 old_ipl = asm_set_ipl( 6 );

    /* Return a pointer to the next empty Rx Buffer Descriptor */
    uint8 i = rx_bd_idx;

    /* Check to see if the ring of BDs is full */
    if( rx_nbuf[i].status & RX_BD_INUSE )
    {
		/* Restore previous IPL */
    	asm_set_ipl( old_ipl );
    	return NULL;
    }

    /* Mark the buffer as in use */
    rx_nbuf[i].status |= RX_BD_INUSE;

    /* increment the circular index */
    rx_bd_idx = ( uint8 ) ( ( rx_bd_idx + 1 ) % NUM_RXBDS );

    /* Restore previous IPL */
    asm_set_ipl( old_ipl );
	
    return &rx_nbuf[i];
}

/**
 * Allocate a tx buffer indisde buffer descriptor ring
 * @param none
 * @return pointer to buffer to get. NULL for no buffer available
 */
nbuf_t         *
NBUF_AllocTX(  )
{
    /* This routine alters shared data. Disable interrupts! */
    uint8 old_ipl = asm_set_ipl( 6 );

    /* Return a pointer to the next empty Tx Buffer Descriptor */
    uint8 i = tx_bd_idx;

    /* Check to see if ring of BDs is full */
    if( ( tx_nbuf[i].status & TX_BD_INUSE ) || ( tx_nbuf[i].status & TX_BD_R ) )
    {
    	/* Restore previous IPL */
    	asm_set_ipl( old_ipl );
    	return NULL;
    }
        
    /* Mark the buffer as Ready (in use) */
    /* FEC must set R bit in transmit routine */
    tx_nbuf[i].status |= TX_BD_INUSE;

    /* increment the circular index */
    tx_bd_idx = ( uint8 ) ( ( tx_bd_idx + 1 ) % NUM_TXBDS );

    /* Restore previous IPL */
    asm_set_ipl( old_ipl );

    return &tx_nbuf[i];
}


/**
 * Release a rx buffer for internal processing
 * @param pointer to buffer
 * @return none
 */
void
NBUF_ReleaseRX( nbuf_t * pNbuf )
{
    /* This routine alters shared data. Disable interrupts! */
    uint8             old_ipl = asm_set_ipl( 6 );

    /* Mark the buffer as empty and not in use */
    pNbuf->status |= RX_BD_E;
    pNbuf->status &= ~RX_BD_INUSE;

    /* Restore previous IPL */
    asm_set_ipl( old_ipl );
}

/**
 * Release a tx buffer for internal processing
 * @param pointer to buffer
 * @return none
 */
void
NBUF_ReleaseTX( nbuf_t * pNbuf )
{
    /* This routine alters shared data. Disable interrupts! */
    uint8 old_ipl = asm_set_ipl( 6 );

    /* Mark the buffer as not in use */
    pNbuf->status &= ~TX_BD_INUSE;

    /* Restore previous IPL */
    asm_set_ipl( old_ipl );
}

/**
 * Release a tx buffer inside buffer descriptor ring
 * @param pointer to buffer
 * @return none
 */
void
NBUF_ReadyTx( nbuf_t * pNbuf )
{
    /* This routine alters shared data. Disable interrupts! */
    uint8 old_ipl = asm_set_ipl( 6 );

    /* Mark the buffer as not in use */
    pNbuf->status |= TX_BD_R;

    /* Restore previous IPL */
    asm_set_ipl( old_ipl );
}

/**
 * This function checks the EMPTY bit of the next Rx buffer to be
 * allocated. If the EMPTY bit is cleared, then the next buffer in
 * the ring has been filled by the FEC and has not already been
 * allocated and passed up the stack. In this case, the next buffer
 * in the ring is ready to be allocated. Otherwise, the  buffer is
 * either empty or not empty but still in use by a higher level
 * protocol. The FEC receive routine uses this function to determine
 * if multiple buffers where filled by the FEC during a single interrupt
 * event
 * @param none
 * @return buffer index
 */
uint8
NBUF_ReadyRX(  )
{
    return ( !( rx_nbuf[rx_bd_idx].status & RX_BD_E ) );
}

/********************************************************************/

/**
 * ACK FEC module at low level during rx
 * @param none
 * @return none
 */
void
FEC_ReadyTx(void)
{
    TDAR = 1;
}

/**
 * FEC controller is ready to use more packets
 * @param none
 * @return none
 */
void
FEC_ReadyRX(void)
{
    RDAR = 1;
}

/**
 * Does FEC module have an available packet?
 * @param none
 * @return 1 for an available packet, otherwise not
 */
uint32 
FEC_GetAvailableReadyRX(void)
{
    return (EIR & ( EIR_RXB_MASK | EIR_RXF_MASK ));
}

/**
 * ACK FEC module at low level during rx
 * @param none
 * @return none
 */
void
FEC_ackRX(void)
{
    EIR = ( EIR_RXB_MASK | EIR_RXF_MASK );
}

/**
 * Sets the function to be called when a receive interrupt occurs
 * @param function that the FEC will call in the interrupt
 * @return none
 */
void 
FEC_SetRxCallback(FEC_CallbackType Callback)
{
  fec_Callback = Callback;  
}

/**
 * FEC RX ISR
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vfecrxf 
FEC_IsrRX( void )
{
    /* This ISR can cause a context switch, so the first statement must be
     * a call to the portENTER_SWITCHING_ISR() macro.
     */    
    fec_Callback();
}

#if 0/*FSL: no longer needed*/
void interrupt VectorNumber_Vfecbabr
FEC_IsrError(void)
{
    /* This ISR can cause a context switch, so the first statement must be
     * a call to the portENTER_SWITCHING_ISR() macro.
     */
     
	  /*FSL: error, packet beyond of 1520 Bytes*/
	  /*increase RX Buffer. Memory corruption*/
	  for(;;)
	  ;/*infinite loop*/	
}
#endif

/********************************************************************/
/*
 * Generate the hash table settings for the given address
 *
 * Parameters:
 *  addr    48-bit (6 byte) Address to generate the hash for
 *
 * Return Value:
 *  The 6 most significant bits of the 32-bit CRC result
 */
static uint8 
FEC_HashAddress( const uint8* addr )
{
uint32 crc;
uint8 u8Var;
uint8 i, j;

	crc = 0xFFFFFFFF;
	for(i=0; i<6; ++i)
	{
		u8Var = addr[i];
		for(j=0; j<8; ++j)
		{
			if((u8Var & 0x01)^(crc & 0x01))
			{
				crc >>= 1;
				crc = crc ^ 0xEDB88320;
			}
			else
			{
				crc >>= 1;
			}

			u8Var >>= 1;
		}
	}

	return (uint8)(crc >> 26);
}

/********************************************************************/
/*
 * Set the Physical (Hardware) Address and the Individual Address
 * Hash in the selected FEC
 *
 * Parameters:
 *  ch  FEC channel
 *  pa  Physical (Hardware) Address for the selected FEC
 */
static void 
FEC_SetAddress( const uint8 *pa )
{
	uint8 crc;

	/*
	* Set the Physical Address
	*/
	PALR = (uint32)((pa[0]<<24) | (pa[1]<<16) | (pa[2]<<8) | pa[3]);
	PAUR = (uint32)((pa[4]<<24) | (pa[5]<<16));

	/*
	* Calculate and set the hash for given Physical Address
	* in the  Individual Address Hash registers
	*/
	crc = FEC_HashAddress(pa);
	if(crc >= 32)
	{
		IAUR |= (uint32)(1 << (crc - 32));
	}
	else
	{
		IALR |= (uint32)(1 << crc);
	}
}

/**
 * Brings FEC interface up
 * @param MAC address to use for this interface
 * @return none
 */
void
FEC_ResetProcessing(const uint8 *pa)
{
    extern uint32 __VECTOR_RAM[];
    
    /*FEC pins configuration*/
    GPIO_FECPinsInit();
    
    /* Reset the FEC - equivalent to a hard reset */
    ECR = ECR_RESET_MASK;

    /* Wait for the reset sequence to complete */
    while( ECR & ECR_RESET_MASK )
    ;

    /* Disable all FEC interrupts by clearing the EIMR register */
    EIMR = 0;

    /* Clear any interrupts by setting all bits in the EIR register */
    EIR = 0xFFFFFFFFUL;

#ifdef COPY_VECTOR_TABLE_ROM2RAM

    /* Configure Interrupt vectors. */
    __VECTOR_RAM[VEC_RXF] = (uint32)FEC_IsrRX;
    
    __VECTOR_RAM[FEC_INT_RX_ERROR] = (uint32)FEC_IsrError;

#endif

    FEC_SetAddress( pa);

    /* Set Receive Buffer Size */
#if RX_BUFFER_SIZE < 1520
#error "RX_BUFFER_SIZE must be set to 1520 for safe FEC operation."
#endif
    EMRBR = RX_BUFFER_SIZE - 1;

    /* Point to the start of the circular Rx buffer descriptor queue */
    ERDSR = NBUF_GetStartBufferPointer( NBUF_RX );

    /* Point to the start of the circular Tx buffer descriptor queue */
    /*FSL:ETDSR*/ETSDR = NBUF_GetStartBufferPointer( NBUF_TX );

    /*FSL:reset the register first*/
    RCR = 0;

    /* Set the tranceiver interface to MII mode */
    RCR_MAX_FL = RX_BUFFER_SIZE-2;//1518 
    
    RCR_MII_MODE = 1;

    /* Set MII Speed Control Register for 2.5Mhz */
    MSCR_MII_SPEED = ( SYSTEM_CLOCK / ( 2UL * 2500000UL ) );

    /* Only operate in half-duplex, no heart beat control */
    TCR = 0;
}

/**
 * Enable FEC module
 * @param none
 * @return none
 */
void
FEC_LowLevelEnable(void)
{
    /* Allow interrupts by setting IMR register */
    /* FSL: BABR interrupt disabled*/
    EIMR = EIMR_RXF_MASK;/* | EIMR_BABR_MASK;*/

   	/* Fix max Rx length value */
	  EMRBR = RX_BUFFER_SIZE;

    /* Enable FEC */
    ECR = ECR_ETHER_EN_MASK;

    /* Indicate that there have been empty receive buffers produced */
    RDAR = 1;
}

/**
 * Disable FEC module
 * @param none
 * @return none
 */
void
FEC_LowLevelDisable(void)
{
    /* Set the Graceful Transmit Stop bit */
    TCR = ( TCR | TCR_GTS_MASK );

    /* Wait for the current transmission to complete */
    while( !( EIR & EIR_GRA_MASK ) )
    ;

    /* Clear the GRA event */
    EIR = EIR_GRA_MASK;

    /* Disable the FEC */
    ECR = 0;

    /* Disable all FEC interrupts by clearing the IMR register */
    EIMR = 0;

    /* Clear the GTS bit so frames can be tranmitted when restarted */
    TCR = ( TCR & ~TCR_GTS_MASK );
}


