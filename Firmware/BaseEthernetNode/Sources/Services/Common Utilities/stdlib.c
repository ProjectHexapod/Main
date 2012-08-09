/* FILENAME: stdlib.c
 *
 * Functions normally found in a standard C lib.
 *
 * 12/28/2005 - added memcmp and memmove
 *
 * Notes: These functions support ASCII only!!!
 */

#include "cf_board.h"
#include "stdlib.h"
#include "stdarg.h"

/****************************************************************/
INT
isspace (INT ch)
{
	if ((ch == ' ') || (ch == '\t'))	/* \n ??? */
		return TRUE;
	else
		return FALSE;
}

/****************************************************************/
INT
isalnum (INT ch)
{
	/* ASCII only */
	if (((ch >= '0') && (ch <= '9')) ||
		((ch >= 'A') && (ch <= 'Z')) ||
		((ch >= 'a') && (ch <= 'z')))
		return TRUE;
	else
		return FALSE;
}

/****************************************************************/
INT
isdigit (INT ch)
{
	/* ASCII only */
	if ((ch >= '0') && (ch <= '9'))
		return TRUE;
	else
		return FALSE;
}

/****************************************************************/
INT
isupper (INT ch)
{
	/* ASCII only */
	if ((ch >= 'A') && (ch <= 'Z'))
		return TRUE;
	else
		return FALSE;
}

/****************************************************************/
INT 
tolower(INT ch)
{
	if ( (ch >= 'A') && (ch <= 'Z') ) return (ch - 'A' + 'a');
	return ch;
}

/****************************************************************/
INT 
toupper(INT ch)
{
	if ( (ch >= 'a') && (ch <= 'z') ) return (ch - 'a' + 'A');
	return ch;
}

/****************************************************************/
INT
strcasecmp (const CHAR *s1, const CHAR *s2)
{
	CHAR	c1, c2;
	INT		result = 0;

	while (result == 0)
	{
		c1 = *s1++;
		c2 = *s2++;
		if ((c1 >= 'a') && (c1 <= 'z'))
			c1 = (CHAR)(c1 - ' ');
		if ((c2 >= 'a') && (c2 <= 'z'))
			c2 = (CHAR)(c2 - ' ');
		if ((result = (c1 - c2)) != 0)
			break;
		if ((c1 == 0) || (c2 == 0))
			break;
	}
	return result;
}


/****************************************************************/
INT
stricmp (const CHAR *s1, const CHAR *s2)
{
   return (strcasecmp(s1, s2));
}

/****************************************************************/
INT
strncasecmp (const CHAR *s1, const CHAR *s2, INT n)
{
	CHAR	c1, c2;
	INT		k = 0;
	INT		result = 0;

	while ( k++ < n )
	{
		c1 = *s1++;
		c2 = *s2++;
		if ((c1 >= 'a') && (c1 <= 'z'))
			c1 = (CHAR)(c1 - ' ');
		if ((c2 >= 'a') && (c2 <= 'z'))
			c2 = (CHAR)(c2 - ' ');
		if ((result = (c1 - c2)) != 0)
			break;
		if ((c1 == 0) || (c2 == 0))
			break;
	}
	return result;
}

/****************************************************************/
INT
strnicmp (const CHAR *s1, const CHAR *s2, INT n)
{
   return (strncasecmp(s1, s2, n));
}

/****************************************************************/
uint32
strtoul (CHAR *str, CHAR **ptr, INT base)
{
   unsigned long rvalue = 0;
   INT neg = 0;
   INT c;

   /* Validate parameters */
   if ((str != NULL) && (base >= 0) && (base <= 36))
   {
      /* Skip leading white spaces */
      while (isspace(*str))
      {
         ++str;
	}

	/* Check for notations */
       switch (str[0])
	{
		case '0':
          if (base == 0)
          {
             if ((str[1] == 'x') || (str[1] == 'X'))
				{
					base = 16;
                str += 2;
             }
             else
             {
                base = 8;
                str++;
				}
			}
			break;
    
		case '-':
			neg = 1;
          str++;
          break;

       case '+':
          str++;
			break;

		default:
			break;
	}

	if (base == 0)
		base = 10;

      /* Valid "digits" are 0..9, A..Z, a..z */
      while (isalnum(c = *str))
      {
		/* Convert char to num in 0..36 */
         if ((c -= ('a' - 10)) < 10)         /* 'a'..'z' */
         {
            if ((c += ('a' - 'A')) < 10)     /* 'A'..'Z' */
            {
               c += ('A' - '0' - 10);        /* '0'..'9' */
			}
		}

		/* check c against base */
		if (c >= base)
		{
			break;
		}

		if (neg)
		{
			rvalue = (rvalue * base) - c;
		}
		else
		{
			rvalue = (rvalue * base) + c;
         }

         ++str;
		}
	}

   /* Upon exit, 'str' points to the character at which valid info */
   /* STOPS.  No chars including and beyond 'str' are used.        */

	if (ptr != NULL)
			*ptr = str;
		
		return rvalue;
	}

/****************************************************************/
INT
atoi (const CHAR *str)
{
   CHAR *s = (CHAR *)str;
   
   return ((INT)strtoul(s, NULL, 10));
}

/****************************************************************/
INT
strlen (const CHAR *str)
{
	CHAR *s = (CHAR *)str;
	INT len = 0;

	if (s == NULL)
		return 0;

	while (*s++ != '\0')
		++len;

	return len;
}

/****************************************************************/
CHAR *
strcat (CHAR *dest, const CHAR *src)
{
	CHAR *dp;
	CHAR *sp = (CHAR *)src;

	if ((dest != NULL) && (src != NULL))
	{
		dp = &dest[strlen(dest)];

		while (*sp != '\0')
		{
			*dp++ = *sp++;
		}
		*dp = '\0';
	}
	return dest;
}

/****************************************************************/
CHAR *
strncat (CHAR *dest, const CHAR *src, INT n)
{
	CHAR *dp;
	CHAR *sp = (CHAR *)src;

	if ((dest != NULL) && (src != NULL) && (n > 0))
	{
		dp = &dest[strlen(dest)];

		while ((*sp != '\0') && (n-- > 0))
		{
			*dp++ = *sp++;
		}
		*dp = '\0';
	}
	return dest;
}

/****************************************************************/
CHAR *
strcpy (CHAR *dest, const CHAR *src)
{
	CHAR *dp = (CHAR *)dest;
	CHAR *sp = (CHAR *)src;

	if ((dest != NULL) && (src != NULL))
	{
		while (*sp != '\0')
		{
			*dp++ = *sp++;
		}
		*dp = '\0';
	}
	return dest;
}

/****************************************************************/
CHAR *
strncpy (CHAR *dest, const CHAR *src, INT n)
{
	CHAR *dp = (CHAR *)dest;
	CHAR *sp = (CHAR *)src;

	if ((dest != NULL) && (src != NULL) && (n > 0))
	{
		while ((*sp != '\0') && (n-- > 0))
		{
			*dp++ = *sp++;
		}
		*dp = '\0';
	}
	return dest;
}

/****************************************************************/
INT
strcmp (const CHAR *s1, const CHAR *s2)
{
	/* No checks for NULL */
	CHAR *s1p = (CHAR *)s1;
	CHAR *s2p = (CHAR *)s2;

	while (*s2p != '\0')
	{
		if (*s1p != *s2p)
			break;

		++s1p;
		++s2p;
	}
	return (*s1p - *s2p);
}

/****************************************************************/
INT
strncmp (const CHAR *s1, const CHAR *s2, INT n)
{
	/* No checks for NULL */
	CHAR *s1p = (CHAR *)s1;
	CHAR *s2p = (CHAR *)s2;

	if (n <= 0)
		return 0;

	while (*s2p != '\0')
	{
		if (*s1p != *s2p)
			break;

		if (--n == 0)
			break;

		++s1p;
		++s2p;
	}
	return (*s1p - *s2p);
}

/****************************************************************/
CHAR *
strstr(const CHAR *s1, const CHAR *s2)
{
   CHAR *sp = (CHAR *)s1;
   INT  len1 = strlen(s1);
   INT  len2 = strlen(s2);

   while (len1 >= len2) 
   {
      if (strncmp(sp, s2, len2) == 0)
      {
         return (sp);
      }
      ++sp;
      --len1;
   }

   return (NULL);
}

/****************************************************************/
CHAR *
strchr(const CHAR *str, INT c)
{
   CHAR *sp = (CHAR *)str;
   CHAR  ch = (CHAR)(c & 0xff);

   while (*sp != '\0')
   {
      if (*sp == ch)
      {
         return (sp);
      }
      ++sp;
   }

   return (NULL);
}

/****************************************************************/
CHAR * 
strupr(CHAR *s1)
{
	/* No checks for NULL */
	CHAR *s1p = (CHAR *)s1;

	while (*s1p != '\0')
	{
    *s1p = toupper(*s1p);

		++s1p;
	}

   return (s1);
}

/****************************************************************/
void *
memcpy (void *dest, const void *src, unsigned n)
{
	UCHAR *dbp = (UCHAR *)dest;
	UCHAR *sbp = (UCHAR *)src;

	if ((dest != NULL) && (src != NULL) && (n > 0))
	{
      while (n--)
			*dbp++ = *sbp++;
	}
	return dest;
}

/****************************************************************/
void *
memset (void *s, INT c, unsigned n)
{
	/* Not optimized, but very portable */
	UCHAR *sp = (UCHAR *)s;

	if ((s != NULL) && (n > 0))
	{
		while (n--)
		{
			*sp++ = (UCHAR)c;
		}
	}
	return s;
}

/****************************************************************/
INT
memcmp (const void *s1, const void *s2, unsigned n)
{
   UCHAR *s1p, *s2p;

   if (s1 && s2 && (n > 0))
   {
      s1p = (UCHAR *)s1;
      s2p = (UCHAR *)s2;

      /*FSL:fixed line*/
      while (n-- != 0)
      {
         if (*s1p != *s2p)
            return (*s1p - *s2p);
         ++s1p;
         ++s2p;
      }
   }

   return (0);
}


/****************************************************************/
void *
memmove (void *dest, const void *src, unsigned n)
{
   UCHAR *dbp = (UCHAR *)dest;
   UCHAR *sbp = (UCHAR *)src;
   UCHAR *dend = dbp + n;
   UCHAR *send = sbp + n;

   if ((dest != NULL) && (src != NULL) && (n > 0))
   {
      /* see if a memcpy would overwrite source buffer */
      if ((sbp < dbp) && (dbp < send))
      {
         while (n--)
            *(--dend) = *(--send);
      }
      else
      {
         while (n--)
            *dbp++ = *sbp++;
      }
   }

   return dest;
}

/****************************************************************/

UINT32 
LWordSwap(UINT32 u32DataSwap)
{
#if(BYTE_REVERSE_ON_HARDWARE==0)
    UINT32 u32Temp;
    u32Temp= (u32DataSwap & 0xFF000000) >> 24;
    u32Temp+=(u32DataSwap & 0xFF0000)   >> 8;
    u32Temp+=(u32DataSwap & 0xFF00)     << 8;
    u32Temp+=(u32DataSwap & 0xFF)       << 24;
    return(u32Temp);
#else
    return mcf5xxx_byterev(u32DataSwap);
#endif
}

/****************************************************************/
/****************************************************************/
/****************************************************************/
/****************************************************************/

/*$F*************************************************************************
*
* Copyright (C)pa 2004 Mark Norton
*
* Permission is hereby granted, free of charge, to any person obtaining
* a copy of this software and associated documentation files (the
* "Software"), to deal in the Software without restriction, including
* without limitation the rights to use, copy, modify, merge, publish,
* distribute, sublicense, and/or sell copies of the Software, and to
* permit persons to whom the Software is furnished to do so, subject to
* the following conditions:
*
* The above copyright notice and this permission notice shall be included
* in all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
* EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
* MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
* IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
* CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
* TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
* SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*
* Functional
* Description:  Implementation of sscanf() function for the CCS compiler
*
*****************************************************************************/
INT 
sscanf(CHAR *buf, const CHAR *fmt, ...)
{
  
  CHAR        temp_delim;
  CHAR        done;//b06862
  CHAR        *p;
  INT         size_length;
  CHAR        sign;
  CHAR        *endptr;
  va_list     pArgs;
  /*value to return*/
  CHAR        count = 0;

  va_start (pArgs,fmt);

  while (TRUE)
  {
   /* Gobble up the fmt string */
    while (*buf == *fmt)
    {
      if ((*buf == 0) || (*fmt == 0))
        return (count);
    
      buf++;
      fmt++;
    }

#if 1
    /* Check for the % */
    if (*fmt != '%')
      break;

	/*
	 * FSL:Next check for minimum field width.
	 */
	size_length = 0;
	done = FALSE;
	while (!done)
	{
		switch (temp_delim = *++fmt)
		{
			case '0':
			case '1':
			case '2':
			case '3':
			case '4':
			case '5':
			case '6':
			case '7':
			case '8':
			case '9':
				size_length = (size_length * 10) + (temp_delim - '0');
				break;
			default:
				/* we've gone one char too far */
				//--fmt;
				done = TRUE;
				break;
		}
	}
#endif
    /* fmt should point to our first conversion letter at this point */
    switch (*fmt)
    {
#if 0//ndef NO_FLOAT/*CF:not implemented in MCUs and MPUs at software level*/
      case 'f':
      case 'F':

        /* convert to a number */
        *((float *)va_arg(pArgs,float*)) = atof(buf, &endptr);

        /* Make sure that we succeeded */
        if ( buf == endptr )
          return ( count );       
   
        buf = endptr;

        /* count this one */
        count++;
        break;
#endif
#if 1//SIGNED_INT
      case 'd':
      case 'D':
        /* Get a pointer to this argument */
        p = (/*FSL:cast added*/CHAR *)va_arg(pArgs,CHAR*);

        if (*buf == '-')
        {
          buf++;
          sign = TRUE;
        }
        else
          sign = FALSE;

        if(size_length)
        {
          /*temporal string delimitation*/
          temp_delim = *(buf + size_length);
          *(buf + size_length) = '\0';/*NULL character*/
        }
	    
	    /* convert to a number */
	    *(INT *)p = (int32)strtoul(buf, &endptr, 10);
	    if (sign)
	      *(INT *)p = -(*(int32 *)p);

        if(size_length)/*FSL added*/
        {
          /*return removed character back to buf*/
          *(buf + size_length) = temp_delim;	
        }
        
        /* Make sure that we succeeded */
        if ( buf == endptr )
          return ( count );
      
        buf = endptr;

        /* count this one */
        count++;
        break;
#endif
#if 1 //unsigned INT
      case 'u':
      case 'U':
        /* Get a pointer to this argument */
        p = (/*FSL:cast added*/CHAR *)va_arg(pArgs,CHAR*);

        if(size_length)
        {
          /*temporal string delimitation*/
          temp_delim = *(buf + size_length);
          *(buf + size_length) = '\0';/*NULL character*/
        }
	    
	    /* convert to a number */
	    *(UINT *)p = (int32)strtoul(buf, &endptr, 10);

        if(size_length)/*FSL added*/
        {
          /*return removed character back to buf*/
          *(buf + size_length) = temp_delim;	
        }
        
        /* Make sure that we succeeded */
        if ( buf == endptr )
          return ( count );
      
        buf = endptr;

        /* count this one */
        count++;

        break;
#endif
#if 1//string
      case 's':
        /* Get a pointer to this argument */
        p = (CHAR *) va_arg(pArgs,CHAR *);

        /* copy the chars */
        while (TRUE)
        {
          if ((isspace(*buf)) || (!*buf))
          {
            *p = 0;
            break;
          }
          else
          {
            *p = *buf;
            p++;
            buf++;
          }
        }

        /* count this one */
        count++;
        break;
#endif
#if 1//HEXadecimal number
      case 'x':
      case 'X':
        /* Get a pointer to this argument */
        p = (/*FSL:cast added*/CHAR *)va_arg(pArgs,CHAR*);

        if(size_length)
        {
          /*temporal string delimitation*/
          temp_delim = *(buf + size_length);
          *(buf + size_length) = '\0';/*NULL character*/
        }
	    
	    /* convert to a number */
	    *(UINT *)p = (int32)strtoul(buf, &endptr, 16);

        if(size_length)/*FSL added*/
        {
          /*return removed character back to buf*/
          *(buf + size_length) = temp_delim;	
        }
        
        /* Make sure that we succeeded */
        if ( buf == endptr )
          return ( count );
      
        buf = endptr;

        /* count this one */
        count++;

        break;
#endif
      /* unhandled format specifier */
      default:
        return (count);
    }

    /* Move to the next format char */
    fmt++;
  }
   
  return (count);
}