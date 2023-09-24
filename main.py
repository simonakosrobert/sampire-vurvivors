import pygame
import settings #Local settings
import utilities #Local utilities

progress_count = 6
loading_bar_size = (800, 30)
loading_bar_pos = (settings.SCREEN_WIDTH/2 - loading_bar_size[0]/2, settings.SCREEN_HEIGHT/5 - loading_bar_size[1]/2)

loading_bg = pygame.image.load('images/loading_screen_bg.jpg')
loading_bg = pygame.transform.scale(loading_bg, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Sampire Vurvivors")
screen.fill(0)
screen.blit(loading_bg, (0, 0))
utilities.DrawBar(screen, loading_bar_pos, loading_bar_size, (255, 255, 255), (255, 0, 0), 0/progress_count)
pygame.display.update()

import math
import random as rn
from decimal import Decimal, getcontext
import cv2

utilities.DrawBar(screen, loading_bar_pos, loading_bar_size, (255, 255, 255), (255, 0, 0), 1/progress_count)
pygame.display.update()

#Local

import weapons
import characters
import sounds
import button
import stages
import texts
import controls

utilities.DrawBar(screen, loading_bar_pos, loading_bar_size, (255, 255, 255), (255, 0, 0), 2/progress_count)
pygame.display.update()

clock = pygame.time.Clock()

tick = 0
last_mouse_y = 0

icon = pygame.image.load(utilities.resource_path('icon.png'))
pygame.display.set_icon(icon)

#pygame.event.set_grab(True)

cap = cv2.VideoCapture(utilities.resource_path('unseated.mp4'))
success, img = cap.read()
shape = img.shape[1::-1]

utilities.DrawBar(screen, loading_bar_pos, loading_bar_size, (255, 255, 255), (255, 0, 0), 3/progress_count)
pygame.display.update()

run = True

main_menu_bg = pygame.image.load(utilities.resource_path(r'main_menu.jpg'))
main_menu_bg = pygame.transform.scale(main_menu_bg, (main_menu_bg.get_width() * (settings.SCREEN_HEIGHT/main_menu_bg.get_height()), settings.SCREEN_HEIGHT))

getcontext().prec = 3

utilities.DrawBar(screen, loading_bar_pos, loading_bar_size, (255, 255, 255), (255, 0, 0), 4/progress_count)
pygame.display.update()

enemies_dict = {}

pebble = weapons.PlayerWeapons('pebble', 10, 3, 8, 4)   #Name - dmg - fire rate - speed - image count
weapons_list = [pebble]

elvira = characters.Character(1, [0, 0], 'elvira', [], 0, 0, 50, 0.1, settings.SCALE)
enemies_list = [elvira]

imre = characters.Character(3, [0, 0], 'imre', [], 0, 0, 100, 0, settings.SCALE)
#Panda initial starting point
imre.pos = [(settings.SCREEN_WIDTH-imre.image.get_width())/2, (settings.SCREEN_HEIGHT-imre.image.get_height())/2]

utilities.DrawBar(screen, loading_bar_pos, loading_bar_size, (255, 255, 255), (255, 0, 0), 5/progress_count)
pygame.display.update()

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
                        texts.dmg_to_list(weapon.dmg, tick, [enemy.dict[e_key][0] + enemy.image.get_width()/2, enemy.dict[e_key][1]])
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
video_playing = True       
video_frame = None

utilities.DrawBar(screen, loading_bar_pos, loading_bar_size, (255, 255, 255), (255, 0, 0), 6/progress_count)
pygame.display.update()
                                            
if __name__ == '__main__':

    while run:

        pygame.event.get()
        clock.tick(settings.FPS)
        tick += 1
        screen.fill(0)

        if main_menu:

            sounds.Main_music.play_sound(-1)

            if video_playing:
                success, img = cap.read()

                if img is None:
                    video_playing = False
                    # # ------------- FOR LOOPING
                    # cap = cv2.VideoCapture('videos/unseated.mp4')
                    # success, img = cap.read()
                    # video_frame = pygame.image.frombuffer(img.tobytes(), shape, "BGR")
                    # video_frame = pygame.transform.scale(video_frame, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
                    # # ------------- FOR LOOPING
                    screen.blit(video_frame, (0,0))
                else:
                    video_frame = pygame.image.frombuffer(img.tobytes(), shape, "BGR")
                    video_frame = pygame.transform.scale(video_frame, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
                    screen.blit(video_frame, (0, 0))         
            else:        
                screen.blit(video_frame, (0,0))

            if button.resume_button.draw(screen):
                sounds.Main_music.stop_sound()
                main_menu = False
            if button.options_button.draw(screen):
                pass
            if button.quit_button.draw(screen):
                run = False        
        else:

            sounds.Stage_1_music.play_sound(-1)

            stages.office_stage.spawn_despawn(tick)
            stages.office_stage.blit_bg(screen)

            screen.blit(imre.image, imre.pos)  
                    
            for enemy in enemies_list:            
                characters.Character.move_towards_player(player=imre, enemy=enemy)
                characters.Character.collision_detection(player=imre, enemy=enemy)
                characters.Character.enemy_spawner(tick=tick, spawn_rate = 2, enemy=enemy)
                
            for enemy in enemies_list:
                enemies_dict.update(enemy.dict) #[f'{enemy.image_name}-{tick}'] = [x, y, max_health, speed, enemy]
                        
            enemies_dict = dict(sorted(enemies_dict.items(), key=lambda item: item[1][1]))
            characters.Character.enemy_blit(screen=screen, enemy=enemies_dict)         
                
            enemy_push(enemy_list=enemies_list)
                
            closest_enemy = closest_enemy_calc(imre, enemies_list)
            
            pebble.use_weapon(screen, imre, tick, weapons_list, closest_enemy=closest_enemy, enemy_list=enemies_list)
            weapon_hit(weapons_list, enemies_list, enemy_dict=enemies_dict)

            texts.dmg_txt_list = texts.blit_dmg(screen, texts.dmg_txt_list, tick)
            
            health_percentage = float(imre.health) / float(imre.max_health)

            if imre.health < imre.max_health:
                utilities.DrawBar(screen, (imre.pos[0], imre.pos[1] + imre.image.get_height() + 3), (40 * settings.SCALE, 4 * settings.SCALE), (0, 0, 0), (255, 0, 0), health_percentage)

            # KEYBOARD MOVEMENT P1 ---------------------------------
            if controls.num_joysticks == 0:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_s]:
                    
                    #Background moving
                    for key, value in stages.office_stage.dict.items():
                        value[1] -= imre.speed
                    #Enemy moving
                    for key, value in enemies_dict.items():
                        value[1] -= imre.speed
                    #Weapons moving
                    for weapon in weapons_list:
                        for key, value in weapon.dict.items(): #[f'{weapon.image_name}-{tick}'] = [x, y, weapon.speed, dx, dy, image_to_blit]
                            value[1] -= imre.speed
                    #Text moving
                    for item in texts.dmg_txt_list:
                        item[2][1] -= imre.speed

                if keys[pygame.K_w]:

                    #Background moving
                    for key, value in stages.office_stage.dict.items():
                        value[1] += imre.speed
                    #Enemy moving
                    for key, value in enemies_dict.items():
                        value[1] += imre.speed
                    #Weapons moving
                    for weapon in weapons_list:
                        for key, value in weapon.dict.items(): #[f'{weapon.image_name}-{tick}'] = [x, y, weapon.speed, dx, dy, image_to_blit]
                            value[1] += imre.speed
                    #Text moving
                    for item in texts.dmg_txt_list:
                        item[2][1] += imre.speed

                if keys[pygame.K_d]:

                    #Background moving
                    for key, value in stages.office_stage.dict.items():
                        value[0] -= imre.speed
                    #Enemy moving
                    for key, value in enemies_dict.items():
                        value[0] -= imre.speed
                    #Weapons moving
                    for weapon in weapons_list:
                        for key, value in weapon.dict.items(): #[f'{weapon.image_name}-{tick}'] = [x, y, weapon.speed, dx, dy, image_to_blit]
                            value[0] -= imre.speed
                    #Text moving
                    for item in texts.dmg_txt_list:
                        item[2][0] -= imre.speed
                    
                if keys[pygame.K_a]:

                    #Background moving
                    for key, value in stages.office_stage.dict.items():
                        value[0] += imre.speed
                    #Enemy moving
                    for key, value in enemies_dict.items():
                        value[0] += imre.speed
                    #Weapons moving
                    for weapon in weapons_list:
                        for key, value in weapon.dict.items(): #[f'{weapon.image_name}-{tick}'] = [x, y, weapon.speed, dx, dy, image_to_blit]
                            value[0] += imre.speed
                    #Text moving
                    for item in texts.dmg_txt_list:
                        item[2][0] += imre.speed
            # CONTROLLER MOVEMENT P1 ---------------------------------
            else: 
                if controls.p1_controller.get_axis(1) > 0.1:
                    
                    moving_speed = imre.speed * abs(controls.p1_controller.get_axis(1))

                    #Background moving
                    for key, value in stages.office_stage.dict.items():
                        value[1] -= moving_speed
                    #Enemy moving
                    for key, value in enemies_dict.items():
                        value[1] -= moving_speed
                    #Weapons moving
                    for weapon in weapons_list:
                        for key, value in weapon.dict.items(): #[f'{weapon.image_name}-{tick}'] = [x, y, weapon.speed, dx, dy, image_to_blit]
                            value[1] -= moving_speed
                    #Text moving
                    for item in texts.dmg_txt_list:
                        item[2][1] -= moving_speed

                if controls.p1_controller.get_axis(1) < -0.1:
                    
                    moving_speed = imre.speed * abs(controls.p1_controller.get_axis(1))

                    #Background moving
                    for key, value in stages.office_stage.dict.items():
                        value[1] += moving_speed
                    #Enemy moving
                    for key, value in enemies_dict.items():
                        value[1] += moving_speed
                    #Weapons moving
                    for weapon in weapons_list:
                        for key, value in weapon.dict.items(): #[f'{weapon.image_name}-{tick}'] = [x, y, weapon.speed, dx, dy, image_to_blit]
                            value[1] += moving_speed
                    #Text moving
                    for item in texts.dmg_txt_list:
                        item[2][1] += moving_speed

                if controls.p1_controller.get_axis(0) > 0.1:

                    moving_speed = imre.speed * abs(controls.p1_controller.get_axis(0))

                    #Background moving
                    for key, value in stages.office_stage.dict.items():
                        value[0] -= moving_speed
                    #Enemy moving
                    for key, value in enemies_dict.items():
                        value[0] -= moving_speed
                    #Weapons moving
                    for weapon in weapons_list:
                        for key, value in weapon.dict.items(): #[f'{weapon.image_name}-{tick}'] = [x, y, weapon.speed, dx, dy, image_to_blit]
                            value[0] -= moving_speed
                    #Text moving
                    for item in texts.dmg_txt_list:
                        item[2][0] -= moving_speed
                    
                if controls.p1_controller.get_axis(0) < -0.1:

                    moving_speed = imre.speed * abs(controls.p1_controller.get_axis(0))

                    #Background moving
                    for key, value in stages.office_stage.dict.items():
                        value[0] += moving_speed
                    #Enemy moving
                    for key, value in enemies_dict.items():
                        value[0] += moving_speed
                    #Weapons moving
                    for weapon in weapons_list:
                        for key, value in weapon.dict.items(): #[f'{weapon.image_name}-{tick}'] = [x, y, weapon.speed, dx, dy, image_to_blit]
                            value[0] += moving_speed
                    #Text moving
                    for item in texts.dmg_txt_list:
                        item[2][0] += moving_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not main_menu:
                        for music in sounds.music_list:
                            music.stop_sound()
                        cap = cv2.VideoCapture(utilities.resource_path('unseated.mp4'))
                        video_playing = True
                    main_menu = True
            
        if controls.p1_controller and controls.p1_controller.get_button(7):
            if not main_menu:
                for music in sounds.music_list:
                    music.stop_sound()
                cap = cv2.VideoCapture(utilities.resource_path('unseated.mp4'))
                video_playing = True
            main_menu = True

        pygame.display.update()
        
        # if tick % settings.FPS/3 == 0:
        #     print(clock.get_fps())