import pygame
from settings import *

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
