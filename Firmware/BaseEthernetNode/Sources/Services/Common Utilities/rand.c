/*
 * File:    rand.c
 * Purpose: Pseudo-random number generation from the C standard example 
 *
 * Notes:   Assumes RAND_MAX is 32768
 */

#include "cf_board.h"

/********************************************************************/
static INT next = 1;

INT 
rand(void)
{
  next = next * 1103515245 + 12345;
  return (next>>16) & 0x7FFF;
}

void 
srand(INT seed)
{
  next = seed;
}
/********************************************************************/
