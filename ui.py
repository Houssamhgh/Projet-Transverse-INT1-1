import pygame
from settings import *
#functions that are usefull for the user interface are contained in this file


click_released = True

def render_text(text, font, color, x, y, screen):
    #fnction that renders text on the screen
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
        # If the mouse is over the button, change its color
        pygame.draw.rect(screen, BLACK, rect, 3)
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
    #function that draws the trajectory of the projectile
    pos = pygame.Vector2(start_pos)
    vel = pygame.Vector2(velocity)
    points = []
#
    for step in range(steps):
        #here are the equations of trajectories
        t = step * dt
        x = pos.x + vel.x * t
        y = pos.y + vel.y * t + 0.5 * GRAVITY * (t ** 2)

        screen_x = int(x - camera_x)
        screen_y = int(y)
        if screen_y > HEIGHT:  #do not print out of the screen
            break
        points.append((screen_x, screen_y))

    for point in points:
        #draw the trajectory points
        pygame.draw.circle(pygame.display.get_surface(), (255, 255,0),point,2)

def draw_direction_arrow(screen, start_pos, velocity, camera_x=0):
    #function that draws the directionnal arrow of the projectile
    end_pos = start_pos + velocity * 10  #longen the arrow
    pygame.draw.line(screen, BLUE, (start_pos.x - camera_x, start_pos.y),
                     (end_pos.x - camera_x, end_pos.y), 3)

    angle = math.atan2(velocity.y, velocity.x)
    arrow_size = 10
    left = (end_pos.x - camera_x - arrow_size * math.cos(angle - 0.5),
            end_pos.y - arrow_size * math.sin(angle - 0.5))
    right = (end_pos.x - camera_x - arrow_size * math.cos(angle + 0.5),
             end_pos.y - arrow_size * math.sin(angle + 0.5))
    pygame.draw.polygon(screen, BLUE, [(end_pos.x - camera_x, end_pos.y), left, right])

def draw_parabolic_arrow(screen, start_pos, velocity, camera_x=0, steps=100, dt=0.1):
    #function that draws the parabolic arrow of the projectile
    pos = pygame.Vector2(start_pos)
    vel = pygame.Vector2(velocity)
    points = []

    
    for step in range(steps):
        t = step * dt
        x = pos.x + vel.x * t
        y = pos.y + vel.y * t + 0.5 * GRAVITY * (t ** 2)

        #stop if ball reaches the ground
        if y > HEIGHT:
            break

        #calculate the screen position
        screen_x = int(x - camera_x)
        screen_y = int(y)
        points.append((screen_x, screen_y))

    
    for i in range(len(points) - 1):
        pygame.draw.line(screen, BLUE, points[i], points[i + 1], 3)  
    pygame.draw.circle(screen, BLUE,points[0],5)
