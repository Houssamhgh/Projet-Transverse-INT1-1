import pygame
from Constants import WIDTH, HEIGHT

# Configuration de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spidey Hook")
clock = pygame.time.Clock()



def toggle_music():
    global music_on
    music_on = not music_on

def toggle_sounds():
    global sounds_on
    sounds_on = not sounds_on

def change_music(track):
    global selected_music
    selected_music = track
    print(f"Musique changée: {selected_music}")


