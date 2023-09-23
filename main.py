import pygame
import math
import random as rn
from decimal import Decimal, getcontext

#Local
import settings

pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Sampire Vurvivors")

import utilities
import weapons
import characters
import sounds
import button

clock = pygame.time.Clock()

tick = 0
last_mouse_y = 0



# img = pygame.image.load('gfx_new\game_icon.png')
# pygame.display.set_icon(img)

#pygame.event.set_grab(True)

run = True

background = pygame.image.load(r'images\background.jpg')
background = pygame.transform.scale(background, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

main_menu_bg = pygame.image.load(r'images\main_menu.jpg')
main_menu_bg = pygame.transform.scale(main_menu_bg, (main_menu_bg.get_width() * (settings.SCREEN_HEIGHT/main_menu_bg.get_height()), settings.SCREEN_HEIGHT))

getcontext().prec = 3

enemies_dict = {}

pebble = weapons.PlayerWeapons('pebble', 10, 3, 8, 4)   #Name - dmg - fire rate - speed - image count
weapons_list = [pebble]

elvira = characters.Character(1, [0, 0], 'elvira', [], 0, 0, 50, 0.1, settings.SCALE)
enemies_list = [elvira]

imre = characters.Character(3, [0, 0], 'imre', [], 0, 0, 100, 0, settings.SCALE)
#Panda initial starting point
imre.pos = [(settings.SCREEN_WIDTH-imre.image.get_width())/2, (settings.SCREEN_HEIGHT-imre.image.get_height())/2]

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))
                                            
def closest_enemy_calc(player, enemies):
    
    dist = {}
    
    for enemy in enemies:
        for item in enemy.dict.items():
            dx, dy = player.pos[0] - item[1][0], player.pos[1] - item[1][1]
            dist[item[0]] = (math.hypot(dx, dy), item[1][0], item[1][1])
    
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
        
def weapon_hit(weapon_list, enemy_list, enemy_dict):
    for enemy in enemy_list:
        for e_key in tuple(enemy.dict.keys()):
            for weapon in weapon_list:
                for w_key in tuple(weapon.dict.keys()):
                    if enemy.dict[e_key][0]+20 < weapon.dict[w_key][0] + weapon.image_0.get_width() and enemy.dict[e_key][0] + enemy.image.get_width()-20 > weapon.dict[w_key][0] and enemy.dict[e_key][1]+20 < weapon.dict[w_key][1] + weapon.image_0.get_height() and enemy.dict[e_key][1] + enemy.image.get_height()-20 > weapon.dict[w_key][1]:
                        del weapon.dict[w_key]
                        enemy.dict[e_key][2] -= weapon.dmg
                        
                        if enemy.dict[e_key][2] <= 0:
                            del enemy.dict[e_key]
                            del enemy_dict[e_key]
                            break
                        
def enemy_push(enemy_list):
        
    for main_index, main_enemy in enumerate(enemy_list):
        for target_index, target_enemy in enumerate(enemy_list):
            for main_key, main_value in main_enemy.dict.items():
                for target_key, target_value in target_enemy.dict.items():
                    
                    
                    if main_key != target_key and \
                        main_value[0] + 10 < target_value[0] + target_enemy.image.get_width() and \
                        main_value[0] + main_enemy.image.get_width() - 10 > target_value[0] and \
                        main_value[1] + 30 < target_value[1] + target_enemy.image.get_height() and \
                        main_value[1] + main_enemy.image.get_height() - 30 > target_value[1]:
                        
                        #First enemy
                        dx, dy = main_value[0] - target_value[0], main_value[1] - target_value[1]
                        dist = math.hypot(dx, dy)
                        dx, dy = dx / dist, dy / dist  # Normalize.
                        # Move along this normalized vector towards the player at current speed.
                        main_value[0] += dx * main_value[3]
                        main_value[1] += dy * main_value[3]
                        
                        #Second enemy
                        dx, dy = target_value[0] - main_value[0], target_value[1] - main_value[1]
                        dist = math.hypot(dx, dy)
                        dx, dy = dx / dist, dy / dist  # Normalize.
                        # Move along this normalized vector towards the player at current speed.
                        target_value[0] += dx * main_value[3]
                        target_value[1] += dy * main_value[3]

main_menu = True                
                                            
if __name__ == '__main__':

    while run:

        pygame.event.get()
        clock.tick(settings.FPS)
        tick += 1
        screen.fill(0)

        if main_menu:

            sounds.Main_music.play_sound(-1)
            screen.blit(main_menu_bg, (0,0))

            if button.resume_button.draw(screen):
                sounds.Main_music.stop_sound()
                main_menu = False
            if button.options_button.draw(screen):
                pass
            if button.quit_button.draw(screen):
                run = False        
        else:
            screen.blit(background, (0,0))

            screen.blit(imre.image, imre.pos)  
                    
            for enemy in enemies_list:            
                characters.Character.move_towards_player(player=imre, enemy=enemy)
                characters.Character.collision_detection(player=imre, enemy=enemy)
                characters.Character.enemy_spawner(tick=tick, spawn_rate = 2, enemy=enemy)
                
            for enemy in enemies_list:
                enemies_dict.update(enemy.dict)
                        
            enemies_dict = dict(sorted(enemies_dict.items(), key=lambda item: item[1][1]))
            characters.Character.enemy_blit(screen=screen, enemy=enemies_dict)         
                
            enemy_push(enemy_list=enemies_list)
                
            closest_enemy = closest_enemy_calc(imre, enemies_list)
            
            pebble.use_weapon(screen, imre, tick, weapons_list, closest_enemy=closest_enemy, enemy_list=enemies_list)
            weapon_hit(weapons_list, enemies_list, enemy_dict=enemies_dict)
            
            health_percentage = float(imre.health) / float(imre.max_health)

            if imre.health < imre.max_health:
                utilities.DrawBar(screen, (imre.pos[0], imre.pos[1] + imre.image.get_height() + 3), (40 * settings.SCALE, 4 * settings.SCALE), (0, 0, 0), (255, 0, 0), health_percentage)

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
                    main_menu = True           

        pygame.display.update()
        
        # if tick % settings.FPS/3 == 0:
        #     print(clock.get_fps())