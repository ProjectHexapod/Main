/*
 * File:		stdlib.h
 * Purpose:		Function prototypes for standard library functions
 *
 * Notes:
 */

#ifndef _STDLIB_H_
#define _STDLIB_H_

/********************************************************************
 * Standard library functions
 ********************************************************************/

INT
isspace (INT);

INT
isalnum (INT);

INT
isdigit (INT);

INT
isupper (INT);

INT 
tolower (INT);

INT 
toupper (INT);

INT
strcasecmp (const CHAR *, const CHAR *);

INT
strncasecmp (const CHAR *, const CHAR *, INT);

unsigned long
strtoul (CHAR *, CHAR **, INT);

INT
strlen (const CHAR *);

CHAR *
strcat (CHAR *, const CHAR *);

CHAR *
strncat (CHAR *, const CHAR *, INT);

CHAR *
strcpy (CHAR *, const CHAR *);

CHAR *
strncpy (CHAR *, const CHAR *, INT);

INT
strcmp (const CHAR *, const CHAR *);

INT
strncmp (const CHAR *, const CHAR *, INT);

CHAR *
strchr(const CHAR *, INT);

CHAR * 
strupr(CHAR *);

void *
memcpy (void *, const void *, unsigned);

void *
memset (void *, INT, unsigned);

void
free (void *);
 
void *
malloc (unsigned);

#define RAND_MAX 32767

INT
rand (void);

void
srand (INT);

/********************************************************************/

/* Prototypes */
UINT32 
LWordSwap(UINT32);

#define ByteSwap(A)     (A=(A<<8)+(A>>8))

INT 
sscanf(CHAR *buf, const CHAR *fmt, ...);

#endif