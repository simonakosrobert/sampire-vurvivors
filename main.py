import pygame
import math
import random as rn
from decimal import Decimal, getcontext
import pymunk

#Local
import settings
import utilities
import weapons
import characters

pygame.init()

clock = pygame.time.Clock()

tick = 0
last_mouse_y = 0

# img = pygame.image.load('gfx_new\game_icon.png')
# pygame.display.set_icon(img)

screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Sampire Vurvivors")

space = pymunk.Space()

#pygame.event.set_grab(True)

run = True

background = pygame.image.load(r'images\background.jpg')
background = pygame.transform.scale(background, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

getcontext().prec = 3

pebble = weapons.PlayerWeapons('pebble', 10, 3, 8, 4)   #Name - dmg - fire rate - speed - image count
weapons_list = [pebble]

elvira = characters.Character(1, [0, 0], 'elvira', [], 0, 0, 50, 0.1)
enemies_list = [elvira]

imre = characters.Character(3, [0, 0], 'imre', [], 0, 0, 100, 0)
#Panda initial starting point
imre.pos = [(settings.SCREEN_WIDTH-imre.image.get_width())/2, (settings.SCREEN_HEIGHT-imre.image.get_height())/2]
                                            
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
    for enemy in enemy_list:
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
                        
def enemy_push(enemy_list):
    for enemy in enemy_list:
        for item in enemy.dict.items():
            pass
                        
if __name__ == '__main__':

    while run:

        current_health = imre.health

        clock.tick(settings.FPS)
        tick += 1
        screen.fill(0)
        screen.blit(background, (0,0))

        screen.blit(imre.image, imre.pos)
                
        for enemy in enemies_list:
            characters.Character.move_towards_player(player=imre, enemy=enemy)
            characters.Character.collision_detection(player=imre, enemy=enemy)
            characters.Character.enemy_spawner(tick=tick, spawn_rate = 1, enemy=enemy)
            characters.Character.enemy_blit(screen=screen, enemy=enemy)
              
        closest_enemy = closest_enemy_calc(imre, enemies_list)
        
        pebble.use_weapon(screen, imre, tick, weapons_list, closest_enemy=closest_enemy, enemy_list=enemies_list)
        weapon_hit(weapons_list, enemies_list)
        
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
        
        space.step(1/settings.FPS)
    