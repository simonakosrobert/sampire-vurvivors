import pygame
import settings 

class Stage():
    def __init__(self, image_name: str, image_count: int, has_border: bool, borders: tuple = (0, 0, 0, 0)):
        self.image_name = image_name
        self.has_border = has_border
        self.borders = borders
        self.dict = {f'{self.image_name}_0': [0, 0]}
        for i in range(0, image_count):
            image = pygame.image.load(f'images\\{image_name}_{i}.jpg').convert_alpha()
            setattr(Stage, f'image_{i}', pygame.transform.scale(image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)))
        
    def spawn_despawn(self, tick):
        for item in tuple(self.dict.keys()):
            #LEFT
            if self.dict[item][0] > settings.SCREEN_WIDTH:
                self.dict[f'{self.image_name}_{tick}'] = [0, self.dict[item][1]]
                del self.dict[item]
            #UP
            elif self.dict[item][1] > settings.SCREEN_HEIGHT:
                self.dict[f'{self.image_name}_{tick}'] = [self.dict[item][0], 0]
                del self.dict[item]
            #RIGHT
            elif self.dict[item][0] <= -settings.SCREEN_WIDTH:
                self.dict[f'{self.image_name}_{tick}'] = [settings.SCREEN_WIDTH, self.dict[item][1]]
                del self.dict[item]
            elif self.dict[item][1] <= -settings.SCREEN_HEIGHT:
                self.dict[f'{self.image_name}_{tick}'] = [self.dict[item][0], settings.SCREEN_HEIGHT]
                del self.dict[item]                

    def blit_bg(self, screen):
        for key, value in self.dict.items():
            screen.blit(self.image_0, value)

            #Left 
            screen.blit(self.image_0, (value[0] - settings.SCREEN_WIDTH, value[1]))
            #Rigth
            screen.blit(self.image_0, (value[0] + settings.SCREEN_WIDTH, value[1]))
            #Top
            screen.blit(self.image_0, (value[0], value[1] - settings.SCREEN_HEIGHT))
            #Bottom
            screen.blit(self.image_0, (value[0], value[1] + settings.SCREEN_HEIGHT))

            #Top Left 
            screen.blit(self.image_0, (value[0] - settings.SCREEN_WIDTH, value[1] - settings.SCREEN_HEIGHT))
            #Top Right
            screen.blit(self.image_0, (value[0] + settings.SCREEN_WIDTH, value[1] - settings.SCREEN_HEIGHT))
            #Bottom Left
            screen.blit(self.image_0, (value[0] - settings.SCREEN_WIDTH, value[1] + settings.SCREEN_HEIGHT))
            #Bottom Right
            screen.blit(self.image_0, (value[0] + settings.SCREEN_WIDTH, value[1] + settings.SCREEN_HEIGHT))

office_stage = Stage('office_stage', 1, False)