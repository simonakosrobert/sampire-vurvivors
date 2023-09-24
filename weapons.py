import pygame
import settings
import random as rn
import math
import utilities

class PlayerWeapons():   
    def __init__(self, image_name: str, dmg: int, fire_rate:int, speed: int, image_count: int):
        self.image_name = image_name
        self.dmg = dmg
        self.fire_rate = fire_rate
        self.speed = speed
        self.dict = {}
        for i in range(0, image_count):
            image = pygame.image.load(utilities.resource_path(f'{image_name}_{i}.png')).convert_alpha()
            setattr(PlayerWeapons, f'image_{i}', pygame.transform.scale(image, (image.get_width()*((settings.SCREEN_HEIGHT+settings.SCREEN_WIDTH)/500), image.get_height()*((settings.SCREEN_HEIGHT+settings.SCREEN_WIDTH)/500))))
            
    def use_weapon(self, screen, player, tick, weapon_list, closest_enemy, enemy_list):
        image_to_blit = rn.randint(0, 3)
        
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
                    weapon.dict[f'{weapon.image_name}-{tick}'] = [player.pos[0], player.pos[1], weapon.speed, dx, dy, image_to_blit]
                
                for item in weapon.dict.items():
                    screen.blit(getattr(self, f'image_{item[1][5]}'), (item[1][0], item[1][1]))
                    item[1][0] += -item[1][3] * item[1][2]
                    item[1][1] += -item[1][4] * item[1][2]
            


            
