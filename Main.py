import pygame
import pymunk
import pymunk.pygame_util
import math

# Initialisation de Pygame
pygame.init()

# Constantes de l'écran
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Hook")

# Couleurs
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Initialisation du moteur physique Pymunk
space = pymunk.Space()
space.gravity = (0, 1000)

draw_options = pymunk.pygame_util.DrawOptions(screen)

# Création du Stickman (simple cercle)
stickman_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
stickman_body.position = (200, 200)
stickman_shape = pymunk.Circle(stickman_body, 20)
stickman_shape.elasticity = 0.5
stickman_shape.friction = 0.5
space.add(stickman_body, stickman_shape)

grappling = False
rope = None

# Points d'ancrage pour le grappin
anchor_points = [(400, 100), (600, 250), (500, 400)]
anchor_bodies = [pymunk.Body(body_type=pymunk.Body.STATIC) for _ in anchor_points]
for i, anchor in enumerate(anchor_points):
    anchor_bodies[i].position = anchor


def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            closest_anchor, closest_body = min(
                zip(anchor_points, anchor_bodies), key=lambda p: distance(p[0], (x, y))
            )
            if distance(closest_anchor, stickman_body.position) < 200:
                if rope:
                    space.remove(rope)
                rope = pymunk.PinJoint(stickman_body, closest_body, (0, 0), (0, 0))
                space.add(rope)
                grappling = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if rope:
                space.remove(rope)
                rope = None
                grappling = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        stickman_body.apply_force_at_local_point((-5000, 0), (0, 0))
    if keys[pygame.K_RIGHT]:
        stickman_body.apply_force_at_local_point((5000, 0), (0, 0))

    space.step(1 / 60)
    space.debug_draw(draw_options)

    # Dessiner les points d'ancrage
    for anchor in anchor_points:
        pygame.draw.circle(screen, RED, anchor, 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
