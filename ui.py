import pygame
from settings import *
#Fonctions d'interface utilisateur
click_released = True

def render_text(text, font, color, x, y, screen):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_button(screen, text, x, y, width, height, color, font, action=None):
    global click_released
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect)
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BLUE, rect, 3)
        if mouse_click[0] and action and click_released:
            action()
            click_released = False
    else:
        pygame.draw.rect(screen, BLACK, rect, 3)
    if not mouse_click[0]:
        click_released = True
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
import math
from settings import *

def draw_trajectory(start_pos, velocity, camera_x=0, steps=100, dt=0.1):
    pos = pygame.Vector2(start_pos)
    vel = pygame.Vector2(velocity)
    points = []

    for step in range(steps):
        t = step * dt
        x = pos.x + vel.x * t
        y = pos.y + vel.y * t + 0.5 * GRAVITY * (t ** 2)
#
        screen_x = int(x - camera_x)
        screen_y = int(y)
        if screen_y > HEIGHT:  # Ne pas dessiner en dehors de l'écran
            break
        points.append((screen_x, screen_y))

    for point in points:
        pygame.draw.circle(pygame.display.get_surface(), (255, 255,0),point,2)

def draw_direction_arrow(screen, start_pos, velocity, camera_x=0):
    end_pos = start_pos + velocity * 10  # Multiplier pour allonger la flèche
    pygame.draw.line(screen, BLUE, (start_pos.x - camera_x, start_pos.y),
                     (end_pos.x - camera_x, end_pos.y), 3)

    # Tête de flèche
    angle = math.atan2(velocity.y, velocity.x)
    arrow_size = 10
    left = (end_pos.x - camera_x - arrow_size * math.cos(angle - 0.5),
            end_pos.y - arrow_size * math.sin(angle - 0.5))
    right = (end_pos.x - camera_x - arrow_size * math.cos(angle + 0.5),
             end_pos.y - arrow_size * math.sin(angle + 0.5))
    pygame.draw.polygon(screen, BLUE, [(end_pos.x - camera_x, end_pos.y), left, right])

def draw_parabolic_arrow(screen, start_pos, velocity, camera_x=0, steps=100, dt=0.1):
    """
    Dessine une flèche représentant la trajectoire parabolique de l'araignée,
    prenant en compte la montée et la descente de la balle.
    """
    pos = pygame.Vector2(start_pos)
    vel = pygame.Vector2(velocity)
    points = []

    # Calculer les points de la trajectoire parabolique
    for step in range(steps):
        t = step * dt
        x = pos.x + vel.x * t
        y = pos.y + vel.y * t + 0.5 * GRAVITY * (t ** 2)

        # Arrêter si la balle atteint le sol
        if y > HEIGHT:
            break

        # Calculer les points de la flèche
        screen_x = int(x - camera_x)
        screen_y = int(y)
        points.append((screen_x, screen_y))

    # Dessiner la trajectoire sous forme de parabole (une série de points reliés)
    for i in range(len(points) - 1):
        pygame.draw.line(screen, BLUE, points[i], points[i + 1], 3)  # Relier les points par des lignes

    # Optionnel : Dessiner un petit cercle au point d'origine pour bien visualiser le départ
    pygame.draw.circle(screen, BLUE,points[0],5)