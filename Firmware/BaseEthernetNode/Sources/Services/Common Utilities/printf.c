/*
 * File:		printk.c
 * Purpose:		The standard C library routine printf(), but without
 *				all the baggage.
 */

#include "stdarg.h"
#include "stdlib.h"
#include "cf_board.h"
#include "io.h"

//#define UNIX_DEBUG   1

#ifdef dprintf
#undef dprintf
#endif

#ifdef printf
#undef printf
#endif

/********************************************************************/

typedef struct
{
	INT	dest;
	void (*func)(CHAR);
	CHAR *loc;
} PRINTK_INFO;

INT 
printk (PRINTK_INFO *, const CHAR *, va_list);

/********************************************************************/

#define DEST_CONSOLE	(1)
#define DEST_STRING		(2)

#define FLAGS_MINUS		(0x01)
#define FLAGS_PLUS		(0x02)
#define FLAGS_SPACE		(0x04)
#define FLAGS_ZERO		(0x08)
#define FLAGS_POUND		(0x10)

#define IS_FLAG_MINUS(a)	(a & FLAGS_MINUS)
#define IS_FLAG_PLUS(a)		(a & FLAGS_PLUS)
#define IS_FLAG_SPACE(a)	(a & FLAGS_SPACE)
#define IS_FLAG_ZERO(a)		(a & FLAGS_ZERO)
#define IS_FLAG_POUND(a)	(a & FLAGS_POUND)

#define LENMOD_h		(0x01)
#define LENMOD_l		(0x02)
#define LENMOD_L		(0x04)

#define IS_LENMOD_h(a)	(a & LENMOD_h)
#define IS_LENMOD_l(a)	(a & LENMOD_l)
#define IS_LENMOD_L(a)	(a & LENMOD_L)

#define FMT_d	(0x0001)
#define FMT_o	(0x0002)
#define FMT_x	(0x0004)
#define FMT_X	(0x0008)
#define FMT_u	(0x0010)
#define FMT_c	(0x0020)
#define FMT_s	(0x0040)
#define FMT_p	(0x0080)
#define FMT_n	(0x0100)

#define IS_FMT_d(a)		(a & FMT_d)
#define IS_FMT_o(a)		(a & FMT_o)
#define IS_FMT_x(a)		(a & FMT_x)
#define IS_FMT_X(a)		(a & FMT_X)
#define IS_FMT_u(a)		(a & FMT_u)
#define IS_FMT_c(a)		(a & FMT_c)
#define IS_FMT_s(a)		(a & FMT_s)
#define IS_FMT_p(a)		(a & FMT_p)
#define IS_FMT_n(a)		(a & FMT_n)

/********************************************************************/
static void
printk_putc (INT c, INT *count, PRINTK_INFO *info)
{
	switch (info->dest)
	{
		case DEST_CONSOLE:
			info->func((CHAR)c);
			break;
		case DEST_STRING:
			*(info->loc) = (UCHAR)c;
			++(info->loc);
			break;
		default:
			break;
	}
	*count += 1;
}

/********************************************************************/
static INT
printk_mknumstr (CHAR *numstr, void *nump, INT neg, INT radix)
{
	INT a,b,c;
	UINT ua,ub,uc;

	INT nlen;
	CHAR *nstrp;

	nlen = 0;
	nstrp = numstr;
	*nstrp++ = '\0';

	if (neg)
	{
		a = *(INT *)nump;
		if (a == 0)
		{
			*nstrp = '0';
			++nlen;
			goto done;
		}
		while (a != 0)
		{
			b = (INT)a / (INT)radix;
			c = (INT)a - ((INT)b * (INT)radix);
			if (c < 0)
			{
				c = ~c + 1 + '0';
			}
			else
			{
				c = c + '0';
			}
			a = b;
			*nstrp++ = (CHAR)c;
			++nlen;
		}
	}
	else
	{
		ua = *(UINT *)nump;
		if (ua == 0)
		{
			*nstrp = '0';
			++nlen;
			goto done;
		}
		while (ua != 0)
		{
			ub = (UINT)ua / (UINT)radix;
			uc = (UINT)ua - ((UINT)ub * (UINT)radix);
			if (uc < 10)
			{
				uc = uc + '0';
			}
			else
			{
				uc = uc - 10 + 'A';
			}
			ua = ub;
			*nstrp++ = (CHAR)uc;
			++nlen;
		}
	}
	done:
	return nlen;
}

/********************************************************************/
static void
printk_pad_zero (INT curlen, INT field_width, INT *count, PRINTK_INFO *info)
{
	INT i;

	for (i = curlen; i < field_width; i++)
	{
		printk_putc('0',count, info);
	}
}

/********************************************************************/
static void
printk_pad_space (INT curlen, INT field_width, INT *count, PRINTK_INFO *info)
{
	INT i;

	for (i = curlen; i < field_width; i++)
	{
		printk_putc(' ', count, info);
	}
}

/********************************************************************/
INT
printk (PRINTK_INFO *info, const CHAR *fmt, va_list ap)
{
	/* va_list ap; */
	CHAR *p;
	INT c;

	CHAR vstr[33];
	CHAR *vstrp;
	INT vlen;

	INT done;
	INT count = 0;

	INT	flags_used;
	INT	field_width;
#if 0
	INT	precision_used;
	INT	precision_width;
	INT	length_modifier;
#endif

	INT	ival;
	INT schar, dschar;
	INT *ivalp;
	CHAR *sval;
	INT cval;
	UINT uval;

	/*
	 * Start parsing apart the format string and display appropriate
	 * formats and data.
	 */
	for (p = (CHAR *)fmt; (c = *p) != 0; p++)
	{
		/*
		 * All formats begin with a '%' marker.  Special chars like
		 * '\n' or '\t' are normally converted to the appropriate
		 * character by the __compiler__.  Thus, no need for this
		 * routine to account for the '\' character.
		 */
		if (c != '%')
		{
			/*
			 * This needs to be replaced with something like
			 * 'out_char()' or call an OS routine.
			 */
#ifndef UNIX_DEBUG
			if (c != '\n')
			{
				printk_putc(c, &count, info);
			}
			else
			{
				printk_putc(0x0D /* CR */, &count, info);
				printk_putc(0x0A /* LF */, &count, info);
			}
#else
			printk_putc(c, &count, info);
#endif

			/*
			 * By using 'continue', the next iteration of the loop
			 * is used, skipping the code that follows.
			 */
			continue;
		}

		/*
		 * First check for specification modifier flags.
		 */
		flags_used = 0;
		done = FALSE;
		while (!done)
		{
			switch (/* c = */ *++p)
			{
				case '-':
					flags_used |= FLAGS_MINUS;
					break;
				case '+':
					flags_used |= FLAGS_PLUS;
					break;
				case ' ':
					flags_used |= FLAGS_SPACE;
					break;
				case '0':
					flags_used |= FLAGS_ZERO;
					break;
				case '#':
					flags_used |= FLAGS_POUND;
					break;
				default:
					/* we've gone one char too far */
					--p;
					done = TRUE;
					break;
			}
		}

		/*
		 * Next check for minimum field width.
		 */
		field_width = 0;
		done = FALSE;
		while (!done)
		{
			switch (c = *++p)
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
					field_width = (field_width * 10) + (c - '0');
					break;
				default:
					/* we've gone one char too far */
					--p;
					done = TRUE;
					break;
			}
		}

		/*
		 * Next check for the width and precision field separator.
		 */
		if (/* (c = *++p) */ *++p == '.')
		{
			/* precision_used = TRUE; */

			/*
			 * Must get precision field width, if present.
			 */
			/* precision_width = 0; */
			done = FALSE;
			while (!done)
			{
				switch (/* c = uncomment if used below */ *++p)
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
#if 0
						precision_width = (precision_width * 10) +
							(c - '0');
#endif
						break;
					default:
						/* we've gone one char too far */
						--p;
						done = TRUE;
						break;
				}
			}
		}
		else
		{
			/* we've gone one char too far */
			--p;
#if 0
			precision_used = FALSE;
			precision_width = 0;
#endif
		}

		/*
		 * Check for the length modifier.
		 */
		/* length_modifier = 0; */
		switch (/* c = */ *++p)
		{
			case 'h':
				/* length_modifier |= LENMOD_h; */
				break;
			case 'l':
				/* length_modifier |= LENMOD_l; */
				break;
			case 'L':
				/* length_modifier |= LENMOD_L; */
				break;
			default:
				/* we've gone one char too far */
				--p;
				break;
		}

		/*
		 * Now we're ready to examine the format.
		 */
		switch (c = *++p)
		{
			case 'd':
			case 'i':
				ival = (INT)va_arg(ap, INT);
				vlen = printk_mknumstr(vstr,&ival,TRUE,10);
				vstrp = &vstr[vlen];

				if (ival < 0)
				{
					schar = '-';
					++vlen;
				}
				else
				{
					if (IS_FLAG_PLUS(flags_used))
					{
						schar = '+';
						++vlen;
					}
					else
					{
						if (IS_FLAG_SPACE(flags_used))
						{
							schar = ' ';
							++vlen;
						}
						else
						{
							schar = 0;
						}
					}
				}
				dschar = FALSE;
			
				/*
				 * do the ZERO pad.
				 */
				if (IS_FLAG_ZERO(flags_used))
				{
					if (schar)
						printk_putc(schar, &count, info);
					dschar = TRUE;
			
					printk_pad_zero (vlen, field_width, &count, info);
					vlen = field_width;
				}
				else
				{
					if (!IS_FLAG_MINUS(flags_used))
					{
						printk_pad_space (vlen, field_width, &count, info);
			
						if (schar)
							printk_putc(schar, &count, info);
						dschar = TRUE;
					}
				}
			
				/* the string was built in reverse order, now display in */
				/* correct order */
				if (!dschar && schar)
				{
					printk_putc(schar, &count, info);
				}
				goto cont_xd;

			case 'x':
			case 'X':
				uval = (UINT)va_arg(ap, UINT);
				vlen = printk_mknumstr(vstr,&uval,FALSE,16);
				vstrp = &vstr[vlen];

				dschar = FALSE;
				if (IS_FLAG_ZERO(flags_used))
				{
					if (IS_FLAG_POUND(flags_used))
					{
						printk_putc('0', &count, info);
						printk_putc('x', &count, info);
						/*vlen += 2;*/
						dschar = TRUE;
					}
					printk_pad_zero (vlen, field_width, &count, info);
					vlen = field_width;
				}
				else
				{
					if (!IS_FLAG_MINUS(flags_used))
					{
						if (IS_FLAG_POUND(flags_used))
						{
							vlen += 2;
						}
						printk_pad_space (vlen, field_width, &count, info);
						if (IS_FLAG_POUND(flags_used))
						{
							printk_putc('0', &count, info);
							printk_putc('x', &count, info);
							dschar = TRUE;
						}
					}
				}

				if ((IS_FLAG_POUND(flags_used)) && !dschar)
				{
					printk_putc('0', &count, info);
					printk_putc('x', &count, info);
					vlen += 2;
				}
				goto cont_xd;

			case 'o':
				uval = (UINT)va_arg(ap, UINT);
				vlen = printk_mknumstr(vstr,&uval,FALSE,8);
				goto cont_u;
			case 'b':
				uval = (UINT)va_arg(ap, UINT);
				vlen = printk_mknumstr(vstr,&uval,FALSE,2);
				goto cont_u;
			case 'p':
				uval = (UINT)va_arg(ap, void *);
				vlen = printk_mknumstr(vstr,&uval,FALSE,16);
				goto cont_u;
			case 'u':
				uval = (UINT)va_arg(ap, UINT);
				vlen = printk_mknumstr(vstr,&uval,FALSE,10);

				cont_u:
					vstrp = &vstr[vlen];

					if (IS_FLAG_ZERO(flags_used))
					{
						printk_pad_zero (vlen, field_width, &count, info);
						vlen = field_width;
					}
					else
					{
						if (!IS_FLAG_MINUS(flags_used))
						{
							printk_pad_space (vlen, field_width, &count, info);
						}
					}

				cont_xd:
					while (*vstrp)
						printk_putc(*vstrp--, &count, info);

					if (IS_FLAG_MINUS(flags_used))
					{
						printk_pad_space (vlen, field_width, &count, info);
					}
				break;

			case 'c':
				cval = (CHAR)va_arg(ap, UINT);
				printk_putc(cval,&count, info);
				break;
			case 's':
				sval = (CHAR *)va_arg(ap, CHAR *);
				if (sval)
				{
					vlen = strlen(sval);
					if (!IS_FLAG_MINUS(flags_used))
					{
						printk_pad_space (vlen, field_width, &count, info);
					}
					while (*sval)
						printk_putc(*sval++,&count, info);
					if (IS_FLAG_MINUS(flags_used))
					{
						printk_pad_space (vlen, field_width, &count, info);
					}
				}
				break;
			case 'n':
				ivalp = (INT *)va_arg(ap, INT *);
				*ivalp = count;
				break;
			default:
				printk_putc(c,&count, info);
				break;
		}
	}
	return count;
}

/********************************************************************/
INT
printf (const CHAR *fmt, ...)
{
	va_list ap;
	INT rvalue;
	PRINTK_INFO info;


	info.dest = DEST_CONSOLE;
	info.func = &out_char;
	/*
	 * Initialize the pointer to the variable length argument list.
	 */
	va_start(ap, fmt);
  //#warning "Add a MUTEX here if multiple tasks use printf function"
	rvalue = printk(&info, fmt, ap);
	//#warning "MUTEX ends"
	/*
	 * Cleanup the variable length argument list.
	 */
	va_end(ap);            
	return rvalue;
}

/********************************************************************/
INT
sprintf (CHAR *s, const CHAR *fmt, ...)
{
	va_list ap;
	INT rvalue = 0;
	PRINTK_INFO info;

	/*
	 * Initialize the pointer to the variable length argument list.
	 */
	if (s != 0)
	{
		info.dest = DEST_STRING;
		info.loc = s;
		va_start(ap, fmt);
		rvalue = printk(&info, fmt, ap);
		*info.loc = '\0';
		va_end(ap);
	}
	return rvalue;
}

/********************************************************************/
INT
dprintf (const CHAR *fmt, ...)
{
	va_list ap;
	INT rvalue;
	PRINTK_INFO info;


	info.dest = DEST_CONSOLE;
	info.func = &out_char;
	/*
	 * Initialize the pointer to the variable length argument list.
	 */
	va_start(ap, fmt);
	rvalue = printk(&info, fmt, ap);
	/*
	 * Cleanup the variable length argument list.
	 */
	va_end(ap);
	return rvalue;
}

/********************************************************************/

