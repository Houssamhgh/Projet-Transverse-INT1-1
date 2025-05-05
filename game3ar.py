import pygame
import random
import math

# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Game Configuration
GRAVITY = 9.81  # Gravité réelle (m/s²)
DAMPING = 0.999  # Amortissement léger pour garder du réalisme
MOVE_FORCE = 0.01  # Influence du joueur sur l'oscillation

# Game States
game_over = False
score = 0

# Charger l'image de l'araignée
try:
    spider_image = pygame.image.load("9109569.jpg")  # Chargez l'image de l'araignée
    spider_image = pygame.transform.scale(spider_image, (50, 50))  # Redimensionner l'image de l'araignée
    print("Image de l'araignée chargée avec succès!")
except Exception as e:
    print(f"Erreur lors du chargement de l'image: {e}")
    spider_image = None  # Si l'image n'est pas chargée, utiliser un cercle par défaut

class Rope:
    def __init__(self, x, y):
        self.anchor = pygame.Vector2(x, y)
        self.length = 150  # Longueur de la corde fixe pour simplifier

    def attach(self, ball):
        ball.is_attached = True
        ball.attached_rope = self
        ball.angle = math.atan2(ball.pos.y - self.anchor.y, ball.pos.x - self.anchor.x)
        ball.angular_velocity = 0  # Réinitialiser la vitesse angulaire

    def update(self, ball):
        if ball.is_attached and ball.attached_rope == self:
            acceleration = - (GRAVITY / self.length) * math.sin(ball.angle)  # Formule du pendule
            ball.angular_velocity += acceleration
            ball.angular_velocity *= DAMPING  # Appliquer un léger amortissement
            ball.angle += ball.angular_velocity

            # Mettre à jour la position
            ball.pos.x = self.anchor.x + self.length * math.sin(ball.angle)
            ball.pos.y = self.anchor.y + self.length * math.cos(ball.angle)

    def draw(self, screen, ball, camera_x):
        if ball.is_attached:
            pygame.draw.line(screen, (255, 255, 255),
                             (self.anchor.x - camera_x, self.anchor.y),
                             (ball.pos.x - camera_x, ball.pos.y), 3)
        pygame.draw.circle(screen, (0, 255, 0), (self.anchor.x - camera_x, self.anchor.y), 6)


class Spider:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.is_attached = False
        self.attached_rope = None
        self.angle = 0
        self.angular_velocity = 0

    def update(self, keys):
        if self.is_attached and self.attached_rope:
            if keys[pygame.K_LEFT]:
                self.angular_velocity -= MOVE_FORCE  # Pousser vers la gauche
            if keys[pygame.K_RIGHT]:
                self.angular_velocity += MOVE_FORCE  # Pousser vers la droite

        else:
            self.velocity.y += GRAVITY * 0.1  # Appliquer la gravité
            self.pos += self.velocity
            self.velocity *= 0.99  # Appliquer un léger amortissement

            # Collision avec le sol
            if self.pos.y >= HEIGHT - 50:  # Assurez-vous que l'image ne dépasse pas
                self.pos.y = HEIGHT - 50
                self.velocity.y = 0

    def toggle_attachment(self, ropes):
        if self.is_attached:
            self.is_attached = False
            self.attached_rope = None
        else:
            closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
            closest_rope.attach(self)

    def draw(self, screen, camera_x):
        # Affichage de l'image de l'araignée
        if spider_image:
            screen.blit(spider_image, (self.pos.x - camera_x - spider_image.get_width() // 2, self.pos.y - spider_image.get_height() // 2))
        else:
            pygame.draw.circle(screen, (0, 0, 255), (self.pos.x - camera_x, self.pos.y), 20)


def generate_rope_chain():
    return [Rope(WIDTH // 2 + i * 300, HEIGHT // 4 + random.randint(-50, 50)) for i in range(5)]


# Initialisation
spider = Spider(WIDTH // 2, HEIGHT // 2)
ropes = generate_rope_chain()
camera_x = 0

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            spider.toggle_attachment(ropes)

    # Mise à jour du jeu
    spider.update(keys)
    for rope in ropes:
        rope.update(spider)

    # Affichage des objets
    for rope in ropes:
        rope.draw(screen, spider, camera_x)
    spider.draw(screen, camera_x)

    # Affichage du score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
