import pygame
import math
import random as rn
from decimal import Decimal, getcontext

#Local
import settings
import utilities
import weapons

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
        self.image_name = image_name
        self.image = pygame.image.load(f'images\{self.image_name}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*((settings.SCREEN_HEIGHT+settings.SCREEN_WIDTH)/500), self.image.get_height()*((settings.SCREEN_HEIGHT+settings.SCREEN_WIDTH)/500)))

pebble = weapons.PlayerWeapons('pebble', 10, 5, 10, 4)   #Name - dmg - fire rate - speed - image count
weapons_list = [pebble]

elvira = Character(1, [0, 0], 'elvira', [], 0, 0, 50, 0.1)
enemies_list = [elvira]

imre = Character(3, [0, 0], 'imre', [], 0, 0, 100, 0)
#Panda initial starting point
imre.pos = [(settings.SCREEN_WIDTH-imre.image.get_width())/2, (settings.SCREEN_HEIGHT-imre.image.get_height())/2]

def move_towards_player(player, enemies):
        # Find direction vector (dx, dy) between enemy and player.
        for enemy in enemies:
            for item in enemy.dict.items():
                dx, dy = player.pos[0] - item[1][0], player.pos[1] - item[1][1]
                dist = math.hypot(dx, dy)
                dx, dy = dx / dist, dy / dist  # Normalize.
                # Move along this normalized vector towards the player at current speed.
                item[1][0] += dx * item[1][3]
                item[1][1] += dy * item[1][3]
        
def collision_detection(player, enemies):
    for enemy in enemies:
        for item in enemy.dict.items():
            if player.pos[0] + 10 < item[1][0] + enemy.image.get_width() and player.pos[0] + player.image.get_width() - 10 > item[1][0] and player.pos[1] + 10 < item[1][1] + enemy.image.get_height() and player.pos[1] + player.image.get_height() - 10 > item[1][1]:
                item[1][3] = 0.2 #Speed
                player.health -= enemy.dmg
            else:
                item[1][3] = 1 #Speed
                        
def enemy_spawner(tick, spawn_rate, enemies):
    spawn_rate = 1 / spawn_rate
    for enemy in enemies:
        if tick % math.floor(settings.FPS * spawn_rate) == 0:
            dice = rn.randint(0,1)
            start_point = -40
            if dice == 0:
                start_point = -40
            else:
                start_point = settings.SCREEN_WIDTH + 40
            enemy.dict[f'{enemy.image_name}-{tick}'] = [start_point, rn.randint(0, settings.SCREEN_HEIGHT), enemy.max_health, enemy.speed]
            
def enemy_blit(screen, *enemies):
    for enemy in enemies:
        for item in enemy.dict.items():
            screen.blit(enemy.image, (item[1][0], item[1][1]))

def closest_enemy_calc(player, enemies):
    
    dist = {}
    
    for enemy in enemies:
        for item in enemy.dict.items():
            dx, dy = player.pos[0] - item[1][0], player.pos[1] - item[1][1]
            dist[item[0]] = (math.hypot(dx, dy), item[1][0]-enemy.image.get_width()/2, item[1][1]-enemy.image.get_height()/2)
    
    closest = ('', 1000000, 0, 0)
    
    for item in dist.items():
        if item[1][0] < closest[1]:
            closest = (item[0], item[1][0], item[1][1], item[1][2]) #Name, hypot, x, y
    return closest

def use_weapon(screen, player, tick, weapon_list, closest_enemy, enemy_list):
    pebble_to_shoot = rn.randint(0, 3)
    
    enemy_count = 0
    for enemy in enemies_list:
        for item in enemy.dict.items():
            enemy_count += 1
    
    if enemy_count > 0:
        for weapon in weapon_list:
            if tick % math.floor(settings.FPS / weapon.fire_rate) == 0:
                dx, dy = player.pos[0] - closest_enemy[2], player.pos[1] - closest_enemy[3]
                dist = math.hypot(dx, dy)
                dx, dy = dx / dist, dy / dist  # Normalize.
                weapon.dict[f'{weapon.image_name}-{tick}'] = [imre.pos[0], imre.pos[1], weapon.speed, dx, dy, pebble_to_shoot]
            
            for item in weapon.dict.items():
                screen.blit(getattr(pebble, f'image_{item[1][5]}'), (item[1][0], item[1][1]))
                item[1][0] += -item[1][3] * item[1][2]
                item[1][1] += -item[1][4] * item[1][2]
            
        
def weapon_hit(weapon_list, enemy_list):
    for enemy in enemy_list:
        for e_key in tuple(enemy.dict.keys()):
            for weapon in weapon_list:
                for w_key in tuple(weapon.dict.keys()):
                    if enemy.dict[e_key][0]+20 < weapon.dict[w_key][0] + weapon.image_0.get_width() and enemy.dict[e_key][0] + enemy.image.get_width()-20 > weapon.dict[w_key][0] and enemy.dict[e_key][1]+20 < weapon.dict[w_key][1] + weapon.image_0.get_height() and enemy.dict[e_key][1] + enemy.image.get_height()-20 > weapon.dict[w_key][1]:
                        del weapon.dict[w_key]
                        enemy.dict[e_key][2] -= weapon.dmg
                        
                        if enemy.dict[e_key][2] <= 0:
                            del enemy.dict[e_key]
                            break
                        
#def enemy_push(enemy_list)          

if __name__ == '__main__':

    while run:

        current_health = imre.health

        clock.tick(settings.FPS)
        tick += 1
        screen.fill(0)
        screen.blit(background, (0,0))

        screen.blit(imre.image, imre.pos)
        
        enemy_spawner(tick, 1, enemies_list)

        move_towards_player(imre, enemies_list)
        enemy_blit(screen, elvira)
        
        closest_enemy = closest_enemy_calc(imre, enemies_list)
        
        use_weapon(screen, imre, tick, weapons_list, closest_enemy=closest_enemy, enemy_list=enemies_list)
        weapon_hit(weapons_list, enemies_list)
        collision_detection(imre, enemies_list)
        
        health_percentage = float(imre.health) / float(imre.max_health)

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
    