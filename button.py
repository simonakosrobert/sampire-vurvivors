import pygame
import settings

class Button():
    def __init__(self, image, scale, width_offset, height_offset):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.height_offset = height_offset * scale
        self.width_offset = width_offset
        self.rect.topleft = (settings.SCREEN_WIDTH/2 - self.image.get_width()/2 + self.width_offset, settings.SCREEN_HEIGHT/2 - self.image.get_height()/2 + self.height_offset)
        self.clicked = False

    def draw(self, surface):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):

            self.image

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
resume_img = pygame.image.load('images/buttons/button_resume.png').convert_alpha()
options_img = pygame.image.load('images/buttons/button_options.png').convert_alpha()
quit_img = pygame.image.load('images/buttons/button_quit.png').convert_alpha()

resume_button = Button(resume_img, settings.SCALE, settings.SCREEN_WIDTH/3, -100)
options_button = Button(options_img, settings.SCALE, settings.SCREEN_WIDTH/3, 0)
quit_button = Button(quit_img, settings.SCALE, settings.SCREEN_WIDTH/3, 100)