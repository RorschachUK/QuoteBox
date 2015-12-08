QuoteBox - a small Arduino-based device which displays quotes on demand

Step one - program EEPROM.  

Get a 256k chip and program it withquotes in the following format:

* Address		Purpose
* 0x0000-0x0001	Number of entries (16 bit int)
* 0x0002-0x0005	Address of first entry (32 bit long)
* 0x0006-0x0007	Length of first entry (16 bit int)
* 0x0010-0x0012	Address of second entry (32 bit long)
* 0x0013-0x0014	Length of second entry (16 bit int)
* ...
* {Address 1}	Quote 1's text, whose length has been stated
* {Address 2}	Quote 2's text
* ... etc

To do this we'll start with a human-readable quotes file and use some Python to process it and construct the more machine-friendly index file, then use a Raspberry Pi to blast this in to the EEPROM.

Step two - read EEPROM, extract quote

The next phase of programming will shift across to an Arduino to try to interface to the EEPROM and manage to access a random quote by:
* Getting the int from the first 2 bytes to find the number of entries
* Picking a random entry up to that number
* Going to the index at address 2 + entry * 3
* Reading the address (32 bit long) and length (16 bit int) from the index
* Going to that address and reading that many bytes into a string

Step three - draw quote on screen nicely

Interface with a small (160x128?) SPI screen and figure out how to draw our quote nicely, and what to do if it's too large (scroll slowly I expect)
