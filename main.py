import pygame
import math
import random as rn
from decimal import Decimal, getcontext

#Local
import settings
import utilities

pygame.init()

clock = pygame.time.Clock()

tick = 0
last_mouse_y = 0

# img = pygame.image.load('gfx_new\game_icon.png')
# pygame.display.set_icon(img)

screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Sampire Vurvivors")

#pygame.event.set_grab(True)

run = True

background = pygame.image.load(r'images\background.jpg')
background = pygame.transform.scale(background, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

getcontext().prec = 3

class Character():
    def __init__(self, speed:int, pos:int, image_name:str, spawn_list:list, xp:int, point:int, health: Decimal, dmg: Decimal):
        self.speed = speed
        self.spawn_list = spawn_list
        self.dict = {}
        self.xp = xp
        self.pos = pos
        self.point = point
        self.max_health = Decimal(health)
        self.health = Decimal(health)
        self.dmg = Decimal(dmg)
        self.image = pygame.image.load(f'images\{image_name}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*((settings.SCREEN_HEIGHT+settings.SCREEN_WIDTH)/500), self.image.get_height()*((settings.SCREEN_HEIGHT+settings.SCREEN_WIDTH)/500)))

imre = Character(3, [0, 0], 'imre', [], 0, 0, 100, 0)
#Panda initial starting point
imre.pos = [(settings.SCREEN_WIDTH-imre.image.get_width())/2, (settings.SCREEN_HEIGHT-imre.image.get_height())/2]

elvira = Character(1, [0, 0], 'elvira', [], 0, 0, 50, 0.1)
elvira.pos = [-40, rn.randint(50, 750)]

def move_towards_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.pos[0] += dx * self.speed
        self.pos[1] += dy * self.speed


if __name__ == '__main__':

    while run:

        current_health = imre.health

        clock.tick(settings.FPS)
        tick += 1
        screen.fill(0)
        screen.blit(background, (0,0))

        screen.blit(imre.image, imre.pos)

        move_towards_player(elvira, imre)
        screen.blit(elvira.image, elvira.pos)


        if imre.pos[0] + 10 < elvira.pos[0] + elvira.image.get_width() and imre.pos[0] + imre.image.get_width() - 10 > elvira.pos[0] and imre.pos[1] + 10 < elvira.pos[1] + elvira.image.get_height() and imre.pos[1] + imre.image.get_height() - 10 > elvira.pos[1]:
            imre.health -= elvira.dmg

        health_percentage = float(imre.health) / float(imre.max_health)

        print(health_percentage)


        if imre.health < imre.max_health:
            utilities.DrawBar(screen, (imre.pos[0], imre.pos[1] + imre.image.get_height() + 3), (40, 4), (0, 0, 0), (255, 0, 0), health_percentage)

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_s]:
            imre.pos[1] += imre.speed
        if keys[pygame.K_w]:
            imre.pos[1] -= imre.speed
        if keys[pygame.K_d]:
            imre.pos[0] += imre.speed
        if keys[pygame.K_a]:
            imre.pos[0] -= imre.speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False             

        pygame.display.update()
    