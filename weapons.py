import pygame
import settings

class PlayerWeapons():   
    def __init__(self, image_name: str, dmg: int, fire_rate:int, speed: int, image_count: int):
        self.image_name = image_name
        self.dmg = dmg
        self.fire_rate = fire_rate
        self.speed = speed
        self.dict = {}
        for i in range(0, image_count):
            image = pygame.image.load(f'images\\{image_name}_{i}.png').convert_alpha()
            setattr(PlayerWeapons, f'image_{i}', pygame.transform.scale(image, (image.get_width()*((settings.SCREEN_HEIGHT+settings.SCREEN_WIDTH)/500), image.get_height()*((settings.SCREEN_HEIGHT+settings.SCREEN_WIDTH)/500))))
            


            
