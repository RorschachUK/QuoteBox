# Quotebox Loader - RorschachUK Dec 2015
# This program reads a quotes file and produces a hex file to program an EEPROM

import random

def readQuotes(filename):
    f = open(filename)
    ret = f.read().replace('\r','').split('\n\n\n')
    f.close
    if '' in ret: ret.remove('')
    return ret

quotes = readQuotes('Pratchett.txt')

# Used to see how many lines a label will take up on a fixed-width
# display without splitting words over line breaks, for instance on
# a 16x2 display, "salination C-crank sonar" will be displayed on
# two lines, like:
# [salination------]  or  [---salination---] if centred.
# [C-crank sonar---]      [-C-crank sonar--]
# This is used to validate the suitability of generated control names for a
# target 16x2 LCD and action instructions for three lines of a target 20x4
# display.
def countLines(text, width):
    """Count the lines needed to display the supplied text on a screen of given width without breaking words over lines."""
    lines = 1
    linelen=0
    for word in text.split(' '):
        if linelen + len(word) < width:
            linelen += len(word) + 1
        else:
            lines += 1
            linelen = len(word)
    return lines

def PrintRandomQuote():
    q = getQuote(random.choice(range(len(quotes))))
    #q = random.choice(quotes).replace('\n',' ').replace('         ','\n')
    #print(q + '\nwould display in ' + str(countLines(q, 16)) + ' lines')
    print(q)   

def getQuote(idx):
    return quotes[idx].replace('\n',' ').replace('         ','\n')

    
