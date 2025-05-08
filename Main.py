# main.py
import sys
import random
import math
import pygame
from settings import *
from utils import  Ball, generate_rope_chain, generate_platforms, generate_slopes, Rope
from ui import render_text, draw_button, draw_trajectory, draw_direction_arrow

# Initialisation pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spidey Hook")
clock = pygame.time.Clock()


# Etat global
game_state = "menu"
music_on = True
sounds_on = True
selected_music = "Track 1"
input_text = ""
click_released = True
is_aiming = True
gravity = 0.5

# Trajectoire initiale
initial_velocity = pygame.Vector2(8, -5)

# Niveau
current_level_index = 0
camera_x = 0
ball = Ball(100, HEIGHT - 100)
ropes = generate_rope_chain(current_level_index)
platforms = generate_platforms(current_level_index)
slopes = generate_slopes(current_level_index)
finish_line = pygame.Rect(4200, 0, 20, HEIGHT)

# Araignées dans le menu



def set_state(state):
    global game_state
    game_state = state



def toggle_music():
    global music_on
    music_on = not music_on


def toggle_sounds():
    global sounds_on
    sounds_on = not sounds_on

def change_music():
    global selected_music
    selected_music = random.choice(["Track 1", "Track 2", "Track 3"])
    print(f"Musique changée: {selected_music}")

def start_game(difficulty='easy'):
    global current_level_index
    index_map = {'easy': 0, 'medium': 1, 'hard': 2}
    index = index_map.get(difficulty, 0)
    current_level_index = index
    start_game_by_index(index)

def start_game_by_index(index):
    global ball, ropes, platforms, slopes, camera_x, finish_line, game_state, current_level_index, initial_velocity
    current_level_index = index
    ball = Ball(0, HEIGHT - 100)  # Positionnée en bas à gauche de l'écran
    ropes = generate_rope_chain(index)
    platforms = generate_platforms(index)
    slopes = generate_slopes(index)
    finish_line = pygame.Rect(4200, 0, 20, HEIGHT)
    camera_x = 0
    initial_velocity = pygame.Vector2(0, 0)

    # Début avec une vitesse nulle
    game_state = "aiming"  # Lancement directement dans l'écran d'aiming

def menu_screen():

    WIDTH, HEIGHT = 800, 600
    background_img = pygame.image.load("boutons/MENU_NEW.png")  # Changez le nom selon votre fichier
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    screen.blit(background_img, (0, 0))

    draw_button(screen, "Start Game", WIDTH // 2 - 100, 230, 190, 50, GRAY, small_font, lambda: start_game("easy"))
    start_img = pygame.image.load("boutons/START.png").convert_alpha()
    start_img = pygame.transform.scale(start_img, (240, 100))
    start_rect = start_img.get_rect(center=(WIDTH // 2.07, 250))
    screen.blit(start_img, start_rect)

    draw_button(screen, "Load Game", WIDTH // 2 - 100, 350, 190, 50, GRAY, small_font, lambda: set_state("load_game"))
    load_img = pygame.image.load("boutons/LOAD.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (240, 100))
    load_rect = load_img.get_rect(center=(WIDTH // 2.05, 375))
    screen.blit(load_img, load_rect)

    draw_button(screen, "Settings", 20, HEIGHT - 70, 200, 50, GRAY, small_font, lambda: set_state("settings"))
    load_img = pygame.image.load("boutons/SET.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (240, 100))
    load_rect = load_img.get_rect(center=(WIDTH // 6.3, 550))
    screen.blit(load_img, load_rect)


camera_x = 0  # Global

def draw_platforms(camera_x):
    # Cette fonction dessine les plateformes sur l'écran
    for platform in platforms:
        platform.draw(screen, camera_x)  # On suppose que platform.draw utilise .rect

def draw_aiming_arrow(start_pos, direction, color, length=100, segment_length=10):
    # Si la direction est un vecteur nul, on évite la normalisation
    if direction.length() == 0:
        return  # Si la direction est nulle, on ne dessine rien

    # Dessine une flèche discontinue
    for i in range(0, length, segment_length * 2):  # Laisse un espace entre chaque segment
        segment_end = start_pos + direction.normalize() * (i + segment_length)
        pygame.draw.line(screen, color, start_pos + pygame.Vector2(camera_x, 0), segment_end + pygame.Vector2(camera_x, 0), 2)

def aiming_screen():
    global initial_velocity, game_state, ball, camera_x  # Ajout de camera_x ici

    WIDTH, HEIGHT = 800, 600
    background_img = pygame.image.load("boutons/BACKGB.jpeg")  # Changez le nom selon votre fichier
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    screen.blit(background_img, (0, 0))

    render_text("Utilise les flèches pour viser, puis Entrée pour tirer", small_font, RED, WIDTH // 2, 50, screen)

    # Gestion des touches
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        initial_velocity.x -= 0.2
    if keys[pygame.K_RIGHT]:
        initial_velocity.x += 0.2
    if keys[pygame.K_UP]:
        initial_velocity.y -= 0.2
    if keys[pygame.K_DOWN]:
        initial_velocity.y += 0.2

    # Si tir validé
    if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
        ball.velocity = initial_velocity.copy()
        game_state = "playing"

    # Affichage de la flèche de visée discontinue
    draw_aiming_arrow(ball.pos, initial_velocity, GREEN, length=100)

    # Affichage de la flèche de direction (solide et de couleur différente)
    direction = initial_velocity
    pygame.draw.line(screen, WHITE, ball.pos - pygame.Vector2(camera_x, 0), ball.pos + direction * 10 - pygame.Vector2(camera_x, 0), 2)

    # Affichage de la trajectoire
    draw_trajectory(ball.pos, direction, camera_x=camera_x, steps=100, dt=0.1)

    ball.draw(screen, camera_x)
    draw_platforms(camera_x)

    # Mise à jour de la caméra
    camera_x = ball.pos.x - CAMERA_OFFSET


def settings_screen():
    WIDTH, HEIGHT = 800, 600
    background_img = pygame.image.load("boutons/SETBG.png")  # Changez le nom selon votre fichier
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    screen.blit(background_img, (0, 0))

    x = WIDTH // 2 - 100
    draw_button(screen, f"MusicS   {'On' if music_on else 'Off'}", 432, 220 , 50, 45, GRAY, small_font, toggle_music)
    load_img = pygame.image.load("boutons/MUSIC.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (205, 85))
    load_rect = load_img.get_rect(center=(WIDTH // 2.05, 243))
    screen.blit(load_img, load_rect)

    draw_button(screen, f"Sounds : {'On' if sounds_on else 'Off'}", 436, 300, 50, 42, GRAY, small_font, toggle_sounds)
    load_img = pygame.image.load("boutons/SOUND.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (200, 80))
    load_rect = load_img.get_rect(center=(WIDTH // 2, 333))
    screen.blit(load_img, load_rect)

    draw_button(screen, "Change Music", 350, 400, 120, 40, GRAY, small_font, change_music)
    load_img = pygame.image.load("boutons/CHANGE MUSIC.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (220, 80))
    load_rect = load_img.get_rect(center=(WIDTH // 2, 430))
    screen.blit(load_img, load_rect)

    draw_button(screen, "Back", 350, 500, 120, 40, GRAY, small_font, lambda: set_state("menu"))
    load_img = pygame.image.load("boutons/BACK.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (200, 80))
    load_rect = load_img.get_rect(center=(WIDTH // 2, 525))
    screen.blit(load_img, load_rect)
def load_game_screen():
    WIDTH, HEIGHT = 800, 600
    background_img = pygame.image.load("boutons/LEVELMENU.png")  # Changez le nom selon votre fichier
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    screen.blit(background_img, (0, 0))

    draw_button(screen, "Easy", WIDTH // 3 - 150 // 2 - (100 // 2), HEIGHT // 2 - 70 // 2, 150, 50, GRAY, small_font, lambda: start_game("easy"))
    load_img = pygame.image.load("boutons/EASY.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (240, 100))
    load_rect = load_img.get_rect(center=(WIDTH // 4.35, 290))
    screen.blit(load_img, load_rect)

    draw_button(screen, "Normal", WIDTH // 2 - 150 // 2, HEIGHT // 2 - 70 // 2, 150, 50, GRAY, small_font, lambda: start_game("medium"))
    load_img = pygame.image.load("boutons/NORMAL.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (190, 90))
    load_rect = load_img.get_rect(center=(WIDTH // 2, 295))
    screen.blit(load_img, load_rect)

    draw_button(screen, "Hard", 2 * WIDTH // 3 - 130 // 2 + (100 // 2), HEIGHT // 2 - 60 // 2, 150, 50, GRAY, small_font, lambda: start_game("hard"))
    load_img = pygame.image.load("boutons/HARD.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (210, 92))
    load_rect = load_img.get_rect(center=(WIDTH // 1.31599, 299))
    screen.blit(load_img, load_rect)

    draw_button(screen, "Back", WIDTH - 220, HEIGHT - 70, 170, 50, GRAY, small_font, lambda: set_state("menu"))
    load_img = pygame.image.load("boutons/BACK.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (210, 90))
    load_rect = load_img.get_rect(center=(WIDTH // 1.199, 550))
    screen.blit(load_img, load_rect)
def game_screen():
    global camera_x, game_state, current_level_index

    keys = pygame.key.get_pressed()
    ball.update(keys, platforms, slopes, ropes)
    camera_x = ball.pos.x - CAMERA_OFFSET

    if not ball.is_alive or ball.pos.y >= HEIGHT - ball.radius:

        game_state = "game_over"

    if pygame.Rect(ball.pos.x - ball.radius, ball.pos.y - ball.radius, ball.radius * 2, ball.radius * 2).colliderect(finish_line):
        current_level_index += 1
        game_state = "win_level"

    for rope in ropes:
        rope.update(ball)
    if ropes[-1].anchor.x - camera_x < WIDTH:
        ropes.append(Rope(ropes[-1].anchor.x + SPACE_BETWEEN_ROPES, HEIGHT // 4 + random.randint(-50, 50)))

    background = pygame.image.load("boutons/BACKGB.jpeg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))



    for rope in ropes:
        rope.draw(screen, ball, camera_x)
    ball.draw(screen, camera_x)
    for platform in platforms:
        platform.draw(screen, camera_x)
    for slope in slopes:
        slope.draw(screen, camera_x)

    pygame.draw.rect(screen, GREEN, pygame.Rect(finish_line.x - camera_x, finish_line.y, finish_line.width, finish_line.height))
    draw_button(screen, "Menu", WIDTH - 120, 20, 100, 40, GRAY, small_font, lambda: set_state("menu"))

def game_over_screen():
    WIDTH, HEIGHT = 800, 600
    background_img = pygame.image.load("boutons/GAMEOVER.png")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    screen.blit(background_img, (0, 0))


    draw_button(screen, "Play Again", WIDTH // 2 - 100, HEIGHT // 2 + 100, 150, 50, GRAY, small_font, lambda: start_game_by_index(current_level_index))
    load_img = pygame.image.load("boutons/RESTART.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (210, 90))
    load_rect = load_img.get_rect(center=(WIDTH // 2.05, 420))
    screen.blit(load_img, load_rect)

    draw_button(screen, "Menu", WIDTH // 2 - 100, HEIGHT // 2 + 170, 150, 50, GRAY, small_font, lambda: set_state("menu"))
    load_img = pygame.image.load("boutons/MENU.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (210, 90))
    load_rect = load_img.get_rect(center=(WIDTH // 2.05, 500))
    screen.blit(load_img, load_rect)
def win_level_screen():
    WIDTH, HEIGHT = 800, 600
    background_img = pygame.image.load("boutons/CONGRATS.png")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    screen.blit(background_img, (0, 0))

    draw_button(screen, "Play Again", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, small_font, lambda: start_game_by_index(current_level_index))
    load_img = pygame.image.load("boutons/NEXTLVL.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (215, 82))
    load_rect = load_img.get_rect(center=(WIDTH // 2 -4, HEIGHT // 2 +120))
    screen.blit(load_img, load_rect)

    draw_button(screen, "Menu", WIDTH // 2 - 100, HEIGHT // 2 + 170, 200, 50, GRAY, small_font, lambda: set_state("menu"))
    load_img = pygame.image.load("boutons/MENU.png").convert_alpha()
    load_img = pygame.transform.scale(load_img, (220, 93))
    load_rect = load_img.get_rect(center=( WIDTH // 2 -4, HEIGHT // 2 +197))
    screen.blit(load_img, load_rect)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == "load_game" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start_game()
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    # Gestion des différentes scènes du jeu
    if game_state == "menu":
        menu_screen()
    elif game_state == "settings":
        settings_screen()
    elif game_state == "load_game":
        load_game_screen()
    elif game_state == "aiming":
        aiming_screen()  # Affichage de la sélection de la trajectoire
    elif game_state == "playing":
        game_screen()  # Affichage du jeu une fois la trajectoire choisie
    elif game_state == "game_over":
        game_over_screen()
    elif game_state == "win_level":
        win_level_screen()

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
