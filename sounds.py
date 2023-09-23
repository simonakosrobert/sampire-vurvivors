import pygame

class Sounds():
    def __init__(self, path: str, volume: float) -> None:
        '''Volume should be in the range of 0.0 and 1 (both inclusive)'''
        self.path = path
        self.is_playing = False
        self.sound = pygame.mixer.Sound(path)
        self.sound.set_volume(volume)

    def play_sound(self, repetition: int):
        if not self.is_playing:
            self.sound.play(repetition)
            self.is_playing = True

    def stop_sound(self):
        if self.is_playing:
            self.sound.stop()
            self.is_playing = False
            
Main_music = Sounds('Music/munka.mp3', 0.2)
