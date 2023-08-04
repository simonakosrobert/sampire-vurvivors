import pygame
import math

#Local
import settings

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


class Character():
    def __init__(self, speed:int, pos:int, image_name:str, spawn_list:list, xp:int, point:int):
        self.speed = speed
        self.spawn_list = spawn_list
        self.dict = {}
        self.xp = xp
        self.pos = pos
        self.point = point
        self.image = pygame.image.load(f'images\{image_name}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (settings.SCREEN_WIDTH/10, settings.SCREEN_HEIGHT/10))

panda = Character(5, [0, 0], 'panda', [], 0, 0)
#Panda initial starting point
panda.pos = [(settings.SCREEN_WIDTH-panda.image.get_width())/2, (settings.SCREEN_HEIGHT-panda.image.get_height())/2]

snow_leopard = Character(2, [0, 0], 'snow_leopard', [], 0, 0)
snow_leopard.pos = [settings.SCREEN_WIDTH/4, settings.SCREEN_HEIGHT/4]



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

        clock.tick(settings.FPS)
        tick += 1
        screen.fill(0)
        screen.blit(background, (0,0))

        screen.blit(panda.image, panda.pos)

        move_towards_player(snow_leopard, panda)
        screen.blit(snow_leopard.image, snow_leopard.pos)

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_s]:
            panda.pos[1] += panda.speed
        if keys[pygame.K_w]:
            panda.pos[1] -= panda.speed
        if keys[pygame.K_d]:
            panda.pos[0] += panda.speed
        if keys[pygame.K_a]:
            panda.pos[0] -= panda.speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False             

        pygame.display.update()
    