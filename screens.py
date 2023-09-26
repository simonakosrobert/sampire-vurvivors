import pygame
import settings

class Screen():
    def __init__(self, image_name: str, extension: str, width: int, height: int):
        self.image_name = image_name
        self.image = pygame.image.load(f'images/{image_name}.{extension}')
        self.image = pygame.transform.scale(self.image, (width, height))


loading_bg = Screen('loading_screen_bg', 'jpg', settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

main_menu_bg = Screen('main_menu', 'jpg', settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

pause_menu_screen = Screen('pause_menu', 'png', settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

