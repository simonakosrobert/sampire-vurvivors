import pygame
from decimal import Decimal, getcontext

getcontext().prec = 3

def DrawBar(screen, pos:tuple, size:tuple, borderC:tuple, barC:tuple, progress:float):

    '''screen = screen to draw on\n
    pos = Position of the bar\n
    size = size of the bar\n
    borderC = color of the border\n
    barC = color of the bar'''

    pygame.draw.rect(screen, borderC, (*pos, *size), 1)
    innerPos  = (pos[0], pos[1])
    innerSize = ((size[0]-1) * progress, size[1]-1)
    pygame.draw.rect(screen, barC, (*innerPos, *innerSize))

def levelUp():
    pass