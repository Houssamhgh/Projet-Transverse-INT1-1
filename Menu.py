import pygame
import math
from Constants import WIDTH, HEIGHT, WHITE, BLUE, small_font
from Settings import screen

def draw_spider_web():
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    num_lines = 10
    for i in range(1, num_lines + 1):
        pygame.draw.circle(screen, WHITE, (center_x, center_y), i * 40, 2)

    for i in range(0, 360, 30):
        x1 = center_x + 40 * num_lines * math.cos(math.radians(i))
        y1 = center_y + 40 * num_lines * math.sin(math.radians(i))
        pygame.draw.line(screen, WHITE, (center_x, center_y), (x1, y1), 2)


def render_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, width, height, color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect)

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BLUE, button_rect, 3)
        if mouse_click[0] == 1 and action is not None:
            pygame.time.delay(100)
            action()

    text_surface = small_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)


