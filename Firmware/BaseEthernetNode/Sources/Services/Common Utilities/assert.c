/*
 * File:        assert.c
 * Purpose:     Provide macro for software assertions
 *
 * Notes:       ASSERT macro defined in assert.h calls assert_failed()
 */

#include "cf_board.h"

const CHAR ASSERT_FAILED_STR[] = "Assertion failed in %s at line %d\n";

/*FSL:printf prototype*/
INT
printf (const CHAR *fmt, ...);

/********************************************************************/
void
assert_failed(CHAR *file, INT line)
{
    printf(ASSERT_FAILED_STR, file, line);

    while (1)
    {}
}
/********************************************************************/
