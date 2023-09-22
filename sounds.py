import pygame

Game_volume = 0.0

class Sounds:
           
    class Music:
        Music = pygame.mixer.Sound('Music\munka.mp3')
        Music.set_volume(Game_volume)