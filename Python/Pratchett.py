# Quotebox Loader - RorschachUK Dec 2015
# This program reads a quotes file and produces a hex file to program an EEPROM

from itertools import chain
import pygame, sys, os, random
from pygame.locals import *
os.environ["SDL_FBDEV"] = "/dev/fb1"

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

def GetRandomQuote():
    return getQuote(random.choice(range(len(quotes))))
    
def PrintRandomQuote():
    q = GetRandomQuote()
    print(q)   

def getQuote(idx):
    return quotes[idx].replace('\n',' ').replace('         ','\n')

def truncline(text, font, maxwidth):
    real=len(text)       
    stext=text           
    l=font.size(text)[0]
    cut=0
    a=0                  
    done=1
    old = None
    while l > maxwidth:
        a=a+1
        n=text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext= n[:-cut]
        else:
            stext = n
        l=font.size(stext)[0]
        real=len(stext)               
        done=0                        
    return real, done, stext             
        
def wrapline(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped
 
 
def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)    

def DrawText(msg, font, width):
    lines = wrapline(msg, font, width)
    height = font.size(msg)[1]
    y = 1
    for line in lines:
        print line
        msgSurf = font.render(line, False, BLACK)
        msgRect = msgSurf.get_rect()
        msgRect.topleft = (1, y)
        DISPLAYSURF.blit(msgSurf, msgRect)
        y += height

PrintRandomQuote()

pygame.init()

keepGoing = True

# set up the window
DISPLAYSURF = pygame.display.set_mode((128, 160), 0, 32)
pygame.display.set_caption('Drawing')

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

# draw on the surface object
DISPLAYSURF.fill(WHITE)

fontObj = pygame.font.Font('freesans.ttf', 6)

DrawText(GetRandomQuote(), fontObj, 126)

# run the game loop
while keepGoing:
    try:
        for event in pygame.event.get():
            if event.type == QUIT:
                keepGoing = False
    except KeyboardInterrupt:
        keepGoing = False
    pygame.display.update()

pygame.quit()
sys.exit()

