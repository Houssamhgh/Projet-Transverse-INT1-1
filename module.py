import pygame
import random
import math


# Constantes internes
GRAVITATIONAL_CONST = 9.81
MASS = 0.05
GRAVITY = MASS * GRAVITATIONAL_CONST
ON_GROUND = False
SPACE_BETWEEN_ROPES = 300

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Spider:
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.speed_x = random.choice([-1, 1]) * random.randint(1, 3)
        self.speed_y = random.choice([-1, 1]) * random.randint(1, 3)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def bounce(self, width, height):
        if self.x < 0 or self.x > width:
            self.speed_x = -self.speed_x
        if self.y < 0 or self.y > height:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 10)

class Rope(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.anchor = pygame.Vector2(x, y)
        self.length = None

    def attach(self, ball):
        self.length = (ball.pos - self.anchor).length()
        ball.is_attached = True
        ball.attached_rope = self
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
            pygame.draw.circle(screen, GREEN, (self.anchor.x - camera_x, self.anchor.y), 6)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=10):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.velocity = pygame.Vector2(8, 5)
        self.is_attached = False
        self.attached_rope = None
        self.mass = 1.0
        self.is_alive = True
        self.state = ON_GROUND

    def update(self, keys, platforms, slopes, ropes, height):
        if not self.is_alive:
            return

        if keys[pygame.K_SPACE]:
            if not self.is_attached and ropes:
                closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
                closest_rope.attach(self)
        else:
            self.is_attached = False
            self.attached_rope = None

        if self.is_attached:
            direction = self.pos - self.attached_rope.anchor
            if direction.length() > 0:
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

        if self.pos.y >= height - self.radius:
            self.pos.y = height - self.radius
            self.velocity.y = 0
            self.state = ON_GROUND
            self.is_alive = False
            self.kill()

        for platform in platforms:
            if platform.rect.colliderect(pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius,
                                                     self.radius * 2, self.radius * 2)):
                if platform.bouncy:
                    # Calcul de la direction de la collision
                    if self.velocity.y > 0:  # Collision par le haut
                        self.velocity.y = -self.velocity.y * 1.5
                    else:  # Collision par le bas
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
        pygame.draw.circle(screen, BLUE, (self.pos.x - camera_x, self.pos.y), self.radius)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, bouncy=False):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.bouncy = bouncy

    def draw(self, screen, camera_x):
        color = GREEN if self.bouncy else RED
        pygame.draw.rect(screen, color, self.rect.move(-camera_x, 0))

class SlopedPlatform(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, bouncy=True):
        super().__init__()
        self.start = pygame.Vector2(x1, y1)
        self.end = pygame.Vector2(x2, y2)
        self.bouncy = bouncy
        self.thickness = 8
        self.color = GREEN if bouncy else RED
        # Ajout d'une boîte englobante pour la détection de collision
        self.rect = pygame.Rect(
            min(x1, x2) - self.thickness,
            min(y1, y2) - self.thickness,
            abs(x2 - x1) + self.thickness * 2,
            abs(y2 - y1) + self.thickness * 2
        )

    def draw(self, screen, camera_x):
        start = self.start - pygame.Vector2(camera_x, 0)
        end = self.end - pygame.Vector2(camera_x, 0)
        pygame.draw.line(screen, self.color, start, end, self.thickness)

    def check_collision_and_bounce(self, ball):
        # Vérification rapide avec la boîte englobante
        if not self.rect.colliderect(pygame.Rect(
            ball.pos.x - ball.radius,
            ball.pos.y - ball.radius,
            ball.radius * 2,
            ball.radius * 2
        )):
            return

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
            # Pour les plateformes verticales (x1 == x2)
            if self.start.x == self.end.x:
                # Si la balle vient de gauche
                if ball.pos.x < self.start.x:
                    ball.pos.x = self.start.x - ball.radius
                    ball.velocity.x = -ball.velocity.x * 1.5
                # Si la balle vient de droite
                else:
                    ball.pos.x = self.start.x + ball.radius
                    ball.velocity.x = -ball.velocity.x * 1.5
            else:
                penetration_depth = ball.radius - distance
                correction_vector = delta.normalize() * penetration_depth if distance != 0 else normal * penetration_depth
                ball.pos += correction_vector

                if self.bouncy:
                    ball.velocity = ball.velocity.reflect(normal) * 1.5
                else:
                    ball.is_alive = False
                    ball.kill()

# Fonctions de génération
def generate_rope_chain():
    return [
        Rope(600, 50),
        Rope(1000, 150),
        Rope(1300, 200),
        Rope(2000, 100),
        Rope(2700, 70),
        Rope(3200, 100),
        Rope(3700, 80),
        Rope(4000, 50),
        Rope(5000, 100),
    ]

def generate_platforms():
    return [
        Platform(615, 400, 150, 10, bouncy=True),
        Platform(1050, 400, 150, 20, bouncy=False),
        Platform(1800, 400, 150, 20, bouncy=True),
        Platform(2700, 400, 150, 20, bouncy=False),
        Platform(3600, 400, 150, 20, bouncy=True),
    ]

def generate_slopes():
    return [
        SlopedPlatform(350, 300, 600, 400),
        SlopedPlatform(350, 100, 350, 300),
        SlopedPlatform(4000, 400, 4000, 300),
    ]
