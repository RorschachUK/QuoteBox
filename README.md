QuoteBox - a small Arduino-based device which displays quotes on demand

Step one - program EEPROM.  Get a 256k chip and program it with
quotes in the following format:
Address		Purpose
0x0000-0x0001	Number of entries (16 bit int)
0x0002-0x0005	Address of first entry (32 bit long)
0x0006-0x0007	Length of first entry (16 bit int)
0x0010-0x0012	Address of second entry (32 bit long)
0x0013-0x0014	Length of second entry (16 bit int)
...
{Address 1}	Quote 1's text, whose length has been stated
{Address 2}	Quote 2's text
... etc
