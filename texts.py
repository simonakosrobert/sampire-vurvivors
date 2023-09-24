import pygame
import settings
import math
import utilities

pygame.font.init()

dmg_font = pygame.font.Font(utilities.resource_path('dmg_font.ttf'), math.floor(20 * settings.SCALE))

dmg_txt_list = []

def dmg_to_list(dmg, tick, pos):
    dmg_txt_list.append([dmg, tick, pos])

def blit_dmg(screen, dmg_list, tick):
    for item in list(dmg_list):
        text_surface = dmg_font.render(str(item[0]), False, (255, 0, 0))
        text_surface.set_alpha(255)
        if tick - item[1] < 64:
            text_surface.set_alpha(255 - (tick - item[1])*4)
            screen.blit(text_surface, (item[2][0] - text_surface.get_width()/2, item[2][1] - (tick - item[1])))
        else:
            dmg_list.remove(item)

    return dmg_list