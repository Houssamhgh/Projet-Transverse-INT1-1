import pygame

class SoundManager:
    def __init__(self):

        pygame.mixer.init()

        self.sounds = {
            'starting_sound': pygame.mixer.Sound('start_game_sound.wav'),
            'gameover_sound': pygame.mixer.Sound('game_over_sound.wav'),
            'hanging_sound': pygame.mixer.Sound('rope_sound.wav'),
            'levelup_sound': pygame.mixer.Sound('level_up_sound.wav'),
            'win_sound': pygame.mixer.Sound('end_game_sound.wav'),
        }


        self.music_tracks = {
            'track1': 'track1.wav',
            'track2': 'track2.wav',
            'track3': 'track3.wav',
        }

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def play_music(self, track_name, loop=True):
        if track_name in self.music_tracks:
            pygame.mixer.music.load(self.music_tracks[track_name])
            pygame.mixer.music.set_volume(0.5)  # volume entre 0.0 et 1.0
            pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()
