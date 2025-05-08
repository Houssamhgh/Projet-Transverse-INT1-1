import pygame
import random
import math
from settings import *
#Fonctions utilitaires et classes
class Rope(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.anchor = pygame.Vector2(x, y)
        self.length = None
        self.image = pygame.image.load("boutons/torch1.png").convert_alpha()  # Load your image
        self.image = pygame.transform.scale(self.image, (35, 90) )
    def attach(self, ball):
        self.length = (ball.pos - self.anchor).length()
        ball.is_attached, ball.attached_rope = True, self
        ball.initial_velocity = ball.velocity.length()

    def update(self, ball):
        if ball.is_attached and ball.attached_rope == self:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.length = max(10, self.length - 2)
            direction = ball.pos - self.anchor
            distance = direction.length()
            if distance > self.length:
                ball.pos = self.anchor + direction.normalize() * self.length

    def draw(self, screen, ball, camera_x):
        if ball.is_attached and ball.attached_rope == self:
            pygame.draw.line(screen, WHITE,
                             (self.anchor.x - camera_x, self.anchor.y),
                             (ball.pos.x - camera_x, ball.pos.y), 3)
        if ball.pos.x < 4100:
            # Instead of the circle, we blit the image
            rect = self.image.get_rect(center=(self.anchor.x - camera_x, self.anchor.y))
            screen.blit(self.image, rect)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=10):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.velocity = pygame.Vector2(8, 5)
        self.is_attached = False
        self.attached_rope = None
        self.state = ON_GROUND
        self.mass = 1.0
        self.is_alive = True

    def update(self, keys, platforms, slopes, ropes):
        if not self.is_alive:
            return
        if keys[pygame.K_SPACE] and not self.is_attached:
            closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
            closest_rope.attach(self)
        elif not keys[pygame.K_SPACE]:
            self.is_attached = False
            self.attached_rope = None

        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
            self.velocity.y = 0

        if self.is_attached:
            direction = self.pos - self.attached_rope.anchor
            distance = direction.length()
            if distance > 0:
                direction.normalize_ip()
                theta = math.atan2(direction.x, direction.y)
                force_tangential = self.mass * GRAVITY * math.sin(theta)
                tangent = pygame.Vector2(-direction.y, direction.x)
                self.velocity += tangent * force_tangential
                self.pos += self.velocity
                current_distance = (self.pos - self.attached_rope.anchor).length()
                if abs(current_distance - self.attached_rope.length) > 1:
                    correction = direction * (self.attached_rope.length - current_distance)
                    self.pos += correction
                    self.velocity -= direction * direction.dot(self.velocity)
        else:
            self.velocity.y += GRAVITY
            self.pos += self.velocity

        if self.pos.y >= HEIGHT - self.radius:
            self.pos.y = HEIGHT - self.radius
            self.velocity.y = 0
            self.state = ON_GROUND

        for platform in platforms:
            if platform.rect.colliderect(pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius,
                                                     self.radius * 2, self.radius * 2)):
                if platform.bouncy:
                    self.velocity.y = -self.velocity.y * 1.5
                    self.state = ON_GROUND
                    self.is_attached = False
                else:
                    self.state = ON_GROUND
                    self.is_attached = False
                    self.is_alive = False
                    self.kill()
                    break

        for slope in slopes:
            slope.check_collision_and_bounce(self)

    def draw(self, screen, camera_x):
        self.image = pygame.image.load("boutons/spider.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.radius * 3.7, self.radius * 3.7))
        screen.blit(self.image, (self.pos.x - camera_x - self.radius-10, self.pos.y - self.radius))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, bouncy=False):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.bouncy = bouncy

        # Choose texture based on bouncy state
        texture_path = "boutons/wood.png" if self.bouncy else "boutons/SPIKES.png"
        self.image = pygame.image.load(texture_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))
class SlopedPlatform(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, bouncy=True):
        super().__init__()
        self.start = pygame.Vector2(x1, y1)
        self.end = pygame.Vector2(x2, y2)
        self.bouncy = bouncy
        self.thickness = 25

        self.length = int((self.end - self.start).length())
        self.angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

        # Choose texture based on bouncy state
        texture_path = "boutons/wood.png" if self.bouncy else "boutons/SPIKES.png"
        self.base_image = pygame.image.load(texture_path).convert_alpha()
        self.base_image = pygame.transform.scale(self.base_image, (self.length, self.thickness))
        self.image = pygame.transform.rotate(self.base_image, -self.angle)

    def draw(self, screen, camera_x):
        start = self.start - pygame.Vector2(camera_x, 0)
        end = self.end - pygame.Vector2(camera_x, 0)
        midpoint = (start + end) / 2

        rotated_rect = self.image.get_rect(center=midpoint)
        screen.blit(self.image, rotated_rect.topleft)

    def check_collision_and_bounce(self, ball):
        line_vec = self.end - self.start
        line_unit = line_vec.normalize()
        normal = pygame.Vector2(-line_unit.y, line_unit.x)
        ball_to_start = ball.pos - self.start
        proj_length = ball_to_start.dot(line_unit)
        proj_length_clamped = max(0, min(proj_length, line_vec.length()))
        closest_point = self.start + proj_length_clamped * line_unit
        delta = ball.pos - closest_point
        distance = delta.length()
        if distance < ball.radius:
            if ball.velocity.dot(normal) > 0:
                normal = -normal
            penetration = ball.radius - distance
            correction = delta.normalize() * penetration if distance != 0 else normal * penetration
            ball.pos += correction
            if self.bouncy:
                ball.velocity = ball.velocity.reflect(normal) * 1.2
            else:
                ball.is_alive = False
                ball.kill()
            return True
        return False

def generate_rope_chain(index):
    return [[Rope(1000, 150), Rope(1300, 100), Rope(2300, 100), Rope(3000, 100), Rope(3500, 80), Rope(5000, 100)],
            [Rope(600, 50), Rope(1000, 150), Rope(1300, 200), Rope(2000, 100), Rope(2700, 70), Rope(3200, 100), Rope(3700, 80), Rope(4000, 50), Rope(5000, 100)],
            [Rope(600, 50), Rope(950, 200), Rope(1300, 100), Rope(2075, 225), Rope(2075, 570), Rope(2575, 75), Rope(2575, 475), Rope(3000, 100), Rope(3700, 80), Rope(5000, 100)],
            [Rope(600, 50), Rope(1000, 150), Rope(1300, 200), Rope(2000, 100), Rope(2700, 70), Rope(3200, 100), Rope(3500, 80), Rope(4000, 50), Rope(5000, 100)]
            ][index]

def generate_platforms(index):
    levels = [
        [Platform(400, 400, 150, 10, True),
         Platform(1000, 400, 150, 20, False),
         Platform(1500, 300, 150, 20, True),
         Platform(2000, 500, 150, 20, False),
         Platform(2700, 400, 150, 20, True),
         Platform(3200, 500, 150, 20, False),
         Platform(3700, 500, 150, 20, True)],

        [Platform(615, 400, 150, 10, True),
         Platform(1050, 400, 150, 20, False),
         Platform(1800, 400, 150, 20, True),
         Platform(2700, 400, 150, 20, False),
         Platform(3600, 400, 150, 20, True)],

        [Platform(1500, 300, 150, 20, True),
         Platform(2000, 150, 150, 20, True),
         Platform(2000, 300, 150, 20, True),
         Platform(2000, 500, 150, 20, False),
         Platform(2500, 150, 150, 20, True),
         Platform(2500, 400, 150, 20, True),
         Platform(2500, 550, 150, 20, False)],

        [Platform(700, 400, 150, 10, True),
         Platform(1050, 400, 150, 20, False),
         Platform(1500, 400, 150, 20, True),
         Platform(2000, 500, 150, 20, True)]
    ]
    return levels[index]
def generate_slopes(index):
    return [
        [],

        [SlopedPlatform(350, 300, 600, 400),
        SlopedPlatform(350, 100, 350,300 ),
        SlopedPlatform(4000,400, 4000, 300 ),],

        [SlopedPlatform(350, 300, 600, 400,True),
        SlopedPlatform(1000,0,1000,250,True),
        SlopedPlatform(1000,350,1000,600,True),
        SlopedPlatform(2000,150,2000,300,True),
         SlopedPlatform(2000,500,2000,600,False),
         SlopedPlatform(2150,150,2150,300,True),
         SlopedPlatform(2150,500,2150,600,False),
         SlopedPlatform(2500,150,2500,0,True),
         SlopedPlatform(2500,400,2500,550,False),
         SlopedPlatform(2650,400,2650,550,False),
         SlopedPlatform(2650,150,2650,0,True),
         SlopedPlatform(3000,300,3150,325,True),
         SlopedPlatform(3150,325,3300,300,False),
         SlopedPlatform(3300,300,3450,325,True),
        SlopedPlatform(4000,250, 4000, 350,True ),
         SlopedPlatform(4000,0, 4000, 100,False),
         SlopedPlatform(4000,500, 4000, 600,False),
         ],

        [SlopedPlatform(350, 300, 600, 400),
        SlopedPlatform(4000,400, 4000, 300 ),
        SlopedPlatform(5000,400, 4000, 300 ),
        ]
    ][index]

