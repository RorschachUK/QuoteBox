# Quotebox Loader - RorschachUK Dec 2015
# This program reads a quotes file and produces a hex file to program an EEPROM

from itertools import chain
import pygame, sys, os, random
from pygame.locals import *
os.environ["SDL_FBDEV"] = "/dev/fb1"
fontSize = 12

def readQuotes(filename):
    f = open(filename)
    ret = f.read().replace('\r','').split('\n\n\n')
    f.close
    if '' in ret: ret.remove('')
    return ret

quotes = readQuotes('Pratchett.txt')

def getQuote(idx):
    return quotes[idx].replace('\n',' ').replace('         ','\n')

def GetRandomQuote():
    return getQuote(random.choice(range(len(quotes))))
    
def PrintRandomQuote():
    q = GetRandomQuote()
    print(q)   

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
    lines = wrap_multi_line(msg, font, width)
    if len(lines)>11:
        return False
    height = font.size(msg)[1]
    y = 1
    for line in lines:
        print line
        msgSurf = font.render(line, False, BLACK)
        msgRect = msgSurf.get_rect()
        msgRect.topleft = (1, y)
        DISPLAYSURF.blit(msgSurf, msgRect)
        y += height
    return True
    
#Startup
pygame.init()

pygame.mouse.set_visible(False)
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

fontObj = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', fontSize)

printed = False
while not printed:
    printed = DrawText(GetRandomQuote(), fontObj, 126)

# run the game loop
while keepGoing:
    try:
        for event in pygame.event.get():
            if event.type == QUIT:
                keepGoing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    printed = False
                    while not printed:
                        printed = DrawText(GetRandomQuote(), fontObj, 126)
    except KeyboardInterrupt:
        keepGoing = False
    pygame.display.update()

pygame.quit()
sys.exit()

