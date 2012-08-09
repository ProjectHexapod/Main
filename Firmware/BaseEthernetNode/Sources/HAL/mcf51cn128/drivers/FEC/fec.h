#ifndef _FEC_H_
#define _FEC_H_

#define RX_ERROR_ALL_FLAGS   (RX_BD_LG | RX_BD_NO | RX_BD_CR | RX_BD_OV)
#define RX_ERROR_LENGTH_FLAG RX_BD_LG
#define RX_ERROR_OTHER_FLAG  (RX_BD_NO | RX_BD_OV)
#define RX_ERROR_CHKSM_FLAG  RX_BD_CR 

#define MCF_FEC_INT_LEVEL       ( 6 )
#define MCF_FEC_INT_PRIORITY    ( 1 )
#define MCF_FEC_VEC_RXF         ( 64 + FEC_INT_RX_NUMBER )

/* ------------------------ Defines --------------------------------------- */

#define NBUF_RX                 ( 1 )
#define NBUF_TX                 ( 0 )

typedef void(*FEC_CallbackType)(void);

/* We set the receiver buffers to the maximum size the FEC supports ( See
 * MCF5235 reference manual 19.2.5.1.2 - Driver/DMA Operation with Receive
 * BDs). This gives us the benefit that any frame fits into one buffer. A
 * maximum size of 2047 is guaranteed by the FEC and 2048 is therefore a
 * safe value.
 * Note: The value MUST be dividable by 16!
 */
#define RX_BUFFER_SIZE          ( 1520/*fsl:2048*/ )

/* Size of the transmit buffers. If you set this value to small all frames
 * greater than this size will be dropped. The value 1520 was choosen because
 * it is bigger than the FEC MTU (1518) and is dividable by 16.
 * Note: The value MUST be dividable by 16! */
#define TX_BUFFER_SIZE          ( 1520 )

/* Number of Receive and Transmit Buffers and Buffer Descriptors */
#define NUM_RXBDS               ( 2 )
/*FSL: workaround to send duplicate messages*/
#define NUM_TXBDS               ( 2 )   /*FSL:tentative value*/

/* ------------------------ Defines ( Buffer Descriptor Flags )------------ */

#define TX_BD_R                 ( 0x8000 )
#define TX_BD_INUSE             ( 0x4000 )
#define TX_BD_TO1               ( 0x4000 )
#define TX_BD_W                 ( 0x2000 )
#define TX_BD_TO2               ( 0x1000 )
#define TX_BD_L                 ( 0x0800 )
#define TX_BD_TC                ( 0x0400 )
#define TX_BD_DEF               ( 0x0200 )
#define TX_BD_HB                ( 0x0100 )
#define TX_BD_LC                ( 0x0080 )
#define TX_BD_RL                ( 0x0040 )
#define TX_BD_UN                ( 0x0002 )
#define TX_BD_CSL               ( 0x0001 )
                                 
#define RX_BD_E                 ( 0x8000 )
#define RX_BD_INUSE             ( 0x4000 )
#define RX_BD_R01               ( 0x4000 )
#define RX_BD_W                 ( 0x2000 )
#define RX_BD_R02               ( 0x1000 )
#define RX_BD_L                 ( 0x0800 )
#define RX_BD_M                 ( 0x0100 )
#define RX_BD_BC                ( 0x0080 )
#define RX_BD_MC                ( 0x0040 )
#define RX_BD_LG                ( 0x0020 )
#define RX_BD_NO                ( 0x0010 )
#define RX_BD_SH                ( 0x0008 )
#define RX_BD_CR                ( 0x0004 )
#define RX_BD_OV                ( 0x0002 )
#define RX_BD_TR                ( 0x0001 )

/* ------------------------ Type definitions ------------------------------ */
typedef struct
{
    uint16          status;     /* control and status */
    uint16          length;     /* transfer length */
    uint8          *data;       /* buffer address */
} nbuf_t;

/* ------------------------ Prototypes ------------------------------------ */

/**
 * Init network buffer descriptor ring
 * @param none
 * @return none
 */
void
NBUF_init(  );

/**
 * Return the address of the first buffer descriptor in the ring.
 * This routine is needed by the FEC of the MPC860T , MCF5282, and MCF523x
 * in order to write the Rx/Tx descriptor ring start registers
 * @param zero for rx, one for tx
 * @return pointer to buffer index
 */
uint32
NBUF_GetStartBufferPointer( uint8 direction );

/**
 * Allocate a rx buffer indisde buffer descriptor ring
 * @param none
 * @return pointer to buffer to get. NULL for no buffer available
 */
nbuf_t *
NBUF_AllocRX( );

/**
 * Allocate a tx buffer indisde buffer descriptor ring
 * @param none
 * @return pointer to buffer to get. NULL for no buffer available
 */
nbuf_t *
NBUF_AllocTX(  );

/**
 * Release a rx buffer for internal processing
 * @param pointer to buffer
 * @return none
 */
void
NBUF_ReleaseRX( nbuf_t * pNbuf );

/**
 * Release a tx buffer for internal processing
 * @param pointer to buffer
 * @return none
 */
void
NBUF_ReleaseTX( nbuf_t * pNbuf );

/**
 * Release a tx buffer inside buffer descriptor ring
 * @param pointer to buffer
 * @return none
 */
void
NBUF_ReadyTx( nbuf_t * pNbuf );

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
NBUF_ReadyRX(  );

/********************************************************************/

/**
 * ACK FEC module at low level during rx
 * @param none
 * @return none
 */
void
FEC_ReadyTx(void);

/**
 * FEC controller is ready to use more packets
 * @param none
 * @return none
 */
void
FEC_ReadyRX(void);

/**
 * Does FEC module have an available packet?
 * @param none
 * @return 1 for an available packet, otherwise not
 */
uint32 
FEC_GetAvailableReadyRX(void);

/**
 * ACK FEC module at low level during rx
 * @param none
 * @return none
 */
void
FEC_ackRX(void);

/**
 * Sets the function to be called when a receive interrupt occurs
 * @param function that the FEC will call in the interrupt
 * @return none
 */
void 
FEC_SetRxCallback(FEC_CallbackType Callback);

/**
 * FEC RX ISR
 * @param none
 * @return none
 */
void interrupt VectorNumber_Vfecrxf 
FEC_IsrRX( void );

#if 0/*FSL: no longer needed*/
void interrupt VectorNumber_Vfecbabr
FEC_IsrError(void);
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
FEC_HashAddress( const uint8* addr );

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
FEC_SetAddress( const uint8 *pa );

/**
 * Brings FEC interface up
 * @param MAC address to use for this interface
 * @return none
 */
void
FEC_ResetProcessing(const uint8 *pa);

/**
 * Enable FEC module
 * @param none
 * @return none
 */
void
FEC_LowLevelEnable(void);

/**
 * Disable FEC module
 * @param none
 * @return none
 */
void
FEC_LowLevelDisable(void);
#endif