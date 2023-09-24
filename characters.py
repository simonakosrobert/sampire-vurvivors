import pygame
from decimal import Decimal
import math
import random as rn
import utilities

#Local
import settings

class Character():
    def __init__(self, speed:int, pos:int, image_name:str, spawn_list:list, xp:int, point:int, health: Decimal, dmg: Decimal, scale: float):
        self.speed = speed * scale
        self.spawn_list = spawn_list
        self.dict = {}
        self.xp = xp
        self.pos = pos
        self.point = point
        self.max_health = Decimal(health)
        self.health = Decimal(health)
        self.dmg = Decimal(dmg)
        self.image_name = image_name
        self.image = pygame.image.load(utilities.resource_path(f'{self.image_name}.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*((settings.SCREEN_HEIGHT+settings.SCREEN_WIDTH)/500), self.image.get_height()*((settings.SCREEN_HEIGHT+settings.SCREEN_WIDTH)/500)))
    
    @classmethod
    def move_towards_player(self, player, enemy):
        # Find direction vector (dx, dy) between enemy and player.
        for item in enemy.dict.items():
            dx, dy = player.pos[0] - item[1][0], player.pos[1] - item[1][1]
            dist = math.hypot(dx, dy)
            dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            item[1][0] += dx * item[1][3]
            item[1][1] += dy * item[1][3]
            
    @classmethod
    def collision_detection(self, player, enemy):
        for item in enemy.dict.items():
            if player.pos[0] + 10 < item[1][0] + enemy.image.get_width() and \
                player.pos[0] + player.image.get_width() - 10 > item[1][0] and \
                player.pos[1] + 10 < item[1][1] + enemy.image.get_height() and \
                player.pos[1] + player.image.get_height() - 10 > item[1][1]:
                    item[1][3] = 0.2 #Speed
                    player.health -= enemy.dmg
            else:
                item[1][3] = enemy.speed #Speed
                
    @classmethod
    def enemy_spawner(self, tick, spawn_rate, enemy):
        spawn_rate = 1 / spawn_rate
        if tick % math.floor(settings.FPS * spawn_rate) == 0:
            dice = rn.randint(0,1)
            start_point = -40
            if dice == 0:
                start_point = -40
            else:
                start_point = settings.SCREEN_WIDTH + 40
            enemy.dict[f'{enemy.image_name}-{tick}'] = [start_point, rn.randint(0, settings.SCREEN_HEIGHT), enemy.max_health, enemy.speed, enemy]
            
    @classmethod
    def enemy_blit(self, screen, enemy):
        if len(enemy) > 0:
            for key, value in enemy.items():
                screen.blit(value[4].image, (value[0], value[1]))