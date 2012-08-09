/*
 * File:		io.h
 * Purpose:		Serial Input/Output routines
 *
 */

#ifndef _IO_H
#define _IO_H

/********************************************************************/

CHAR	
in_char(void);

void
out_char(CHAR);

INT
char_present(void);

INT		
printf(const CHAR *, ... );

INT
sprintf(CHAR *, const CHAR *, ... );

/********************************************************************/

#endif
