import pygame
import math
import random
from Constants import GRAVITY, WIDTH, HEIGHT, WHITE, BLUE, GREEN, RED, ON_GROUND
from Settings import screen
from Levels import ropes
from Main import ball



class Spider:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed_x = random.choice([-1, 1]) * random.randint(1, 3)
        self.speed_y = random.choice([-1, 1]) * random.randint(1, 3)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < 0 or self.x > WIDTH:
            self.speed_x = -self.speed_x
        if self.y < 0 or self.y > HEIGHT:
            self.speed_y = -self.speed_y

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 10)


class Rope(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.anchor = pygame.Vector2(x, y)
        self.length = None

    def attach(self, ball):
        self.length = (ball.pos - self.anchor).length()
        ball.is_attached, ball.attached_rope = True, self
        ball.initial_velocity = ball.velocity.length()

    def update(self, ball):
        if ball.is_attached and ball.attached_rope == self:
            keys= pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.length = max(10,self.length-2)
            direction = ball.pos - self.anchor
            distance = direction.length()
            if distance > self.length:
                ball.pos = self.anchor + direction.normalize() * self.length


    def draw(self, screen, ball, camera_x):
        if ball.is_attached and ball.attached_rope == self:
            pygame.draw.line(screen, WHITE,
                             (self.anchor.x - camera_x, self.anchor.y),
                             (ball.pos.x - camera_x, ball.pos.y), 3)
        if ball.pos.x<4100:
            pygame.draw.circle(screen, (0, 255, 0), (self.anchor.x - camera_x, self.anchor.y), 6)

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
        self.is_alive=True

    def update(self, keys, platforms,slopes):
        if not self.is_alive:
            return
        if keys[pygame.K_SPACE]:
            if not self.is_attached:
                closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
                closest_rope.attach(self)
        else:
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
            slope.check_collision_and_bounce(ball)

    def draw(self, screen, camera_x):
        pygame.draw.circle(screen, BLUE, (self.pos.x - camera_x, self.pos.y), self.radius)


class SlopedPlatform (pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, bouncy=True):
        super().__init__()
        self.start = pygame.Vector2(x1, y1)
        self.end = pygame.Vector2(x2, y2)
        self.bouncy = bouncy
        self.thickness = 8
        self.color = (0, 255, 0) if bouncy else (255, 0, 0)

    def draw(self, screen, camera_x):
        start = self.start - pygame.Vector2(camera_x, 0)
        end = self.end - pygame.Vector2(camera_x, 0)
        pygame.draw.line(screen, self.color, start, end, self.thickness)

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
            # Inverse la normale si la balle vient de l'autre côté
            if ball.velocity.dot(normal) > 0:
                normal = -normal

            penetration_depth = ball.radius - distance
            correction_vector = delta.normalize() * penetration_depth if distance != 0 else normal * penetration_depth
            ball.pos += correction_vector

            if self.bouncy:
                ball.velocity = ball.velocity.reflect(normal) * 1.2
                return True
            else:
                ball.is_alive = False
                ball.kill()
                return False
        return False


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, bouncy=False):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.bouncy= bouncy

    def draw(self, screen, camera_x):
        if self.bouncy:
            pygame.draw.rect(screen, GREEN, self.rect.move(-camera_x, 0))
        else:
            pygame.draw.rect(screen, RED, self.rect.move(-camera_x, 0))