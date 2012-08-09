
/*
 * File:	defines.h
 * Purpose:	Define constants used by CodeWarrior Preprocessor
 *
 * Notes:	Use this as a prefix file for the CodeWarrior assembler and compiler
 *
 */

/* DEBUG = 1 turns on debug print information */
#define DEBUG	0

/*FSL: avoid inserting additional return from carriage, etc*/
#define UNIX_DEBUG

/* CodeWarrior looks for an underscore prepended to C function names */
#define _UNDERSCORE_

/* Define a constant to inform files we are using CodeWarrior */
#ifndef _MWERKS_
#define _MWERKS_
#endif

/* Modify the define constant directive to work with CodeWarrior */
#define	dc.l	.dc.l

/* FSL: handy for strings!!! */
#pragma pointers_in_D0

#if 1

/***********************************************************************/
/*
 * The basic data types
 */

typedef unsigned char		uint8;  /*  8 bits */
typedef unsigned short int	uint16; /* 16 bits */
typedef unsigned long int	uint32; /* 32 bits */

typedef signed char			int8;   /*  8 bits */
typedef signed short int	int16;  /* 16 bits */
typedef signed long int		int32;  /* 32 bits */

typedef volatile uint8		vuint8;  /*  8 bits */
typedef volatile uint16		vuint16; /* 16 bits */
typedef volatile uint32		vuint32; /* 32 bits */

/*FSL: more basic types*/

typedef char CHAR;
typedef unsigned char UCHAR;
typedef signed char SCHAR;
typedef int INT;
typedef unsigned int UINT;

/*FSL: even more typedefs!*/
/* Typedefs */
typedef unsigned char     UINT8;  		/*unsigned 8 bit definition */
typedef unsigned short    UINT16; 		/*unsigned 16 bit definition*/
typedef unsigned long     UINT32; 		/*unsigned 32 bit definition*/
typedef signed char       INT8;   		/*signed 8 bit definition */
typedef short      		    INT16;  		/*signed 16 bit definition*/
typedef long int    	    INT32;  		/*signed 32 bit definition*/

/* TypeDefs */
typedef union
{
	UINT8  bytes[4];
	UINT32 lword;		
}T32_8;

typedef union
{
	UINT8  u8[2];
	UINT16 u16;		
}T16_8;

#else

#define CHAR char
#define UCHAR unsigned char
#define SCHAR signed char
#define INT
#define UINT unsigned int

#endif
/* 
 * Define custom sections for relocating code, data, and constants 
 */
#pragma define_section relocate_code ".relocate_code" far_absolute RX
#pragma define_section relocate_data ".relocate_data" far_absolute RW
#pragma define_section relocate_const ".relocate_const" far_absolute R
#define __relocate_code__   __declspec(relocate_code)
#define __relocate_data__   __declspec(relocate_data)
#define __relocate_const__  __declspec(relocate_const)

/*
 * Memory map definitions from linker command files
 */
extern unsigned char __CUSTOM_ROM[];
extern unsigned char __CUSTOM_ROM_SIZE[];

extern unsigned char __FLASH_ADDRESS[]; 
extern unsigned char __FLASH_SIZE[];
 
#define CUSTOM_ROM_ADDRESS      (unsigned long int)__CUSTOM_ROM
#define CUSTOM_ROM_SIZE         (unsigned long int)__CUSTOM_ROM_SIZE

#define ROM_ADDRESS             (unsigned long int)__FLASH_ADDRESS
#define ROM_SIZE                (unsigned long int)__FLASH_SIZE

/********************************************************************/
