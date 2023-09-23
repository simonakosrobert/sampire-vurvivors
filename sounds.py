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
            
Main_music = Sounds('music/munka.mp3', 0.2)
Stage_1_music = Sounds('music/munka_2.mp3', 0.2)

music_list = [Main_music, Stage_1_music]
