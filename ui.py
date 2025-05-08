import pygame
from settings import *
#functions that are usefull for the user interface are contained in this file


click_released = True

def render_text(text, font, color, x, y, screen):
    #render text on the screen
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_button(screen, text, x, y, width, height, color, font, action=None):
    #function that draws a button on the screen
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
    #function used to draw a projectile's trajectory (here the ball)
    pos = pygame.Vector2(start_pos)
    vel = pygame.Vector2(velocity)
    points = []

    for step in range(steps):
        #compute the position of the ball at each step

        t = step * dt
        x = pos.x + vel.x * t
        y = pos.y + vel.y * t + 0.5 * GRAVITY * (t ** 2)


        screen_x = int(x - camera_x)
        screen_y = int(y)
        if screen_y > HEIGHT:  #do not print out of the screen
            break
        points.append((screen_x, screen_y))

    for point in points:
        #draw all the points one by one
        pygame.draw.circle(pygame.display.get_surface(), (255, 255,0),point,2)

def draw_direction_arrow(screen, start_pos, velocity, camera_x=0):
    #function that draws the directionnal arrow of the projectile
    end_pos = start_pos + velocity * 10  #longen the arrow
    pygame.draw.line(screen, BLUE, (start_pos.x - camera_x, start_pos.y),
                     (end_pos.x - camera_x, end_pos.y), 3)

