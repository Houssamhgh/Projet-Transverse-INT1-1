import pygame
import random
import math
from settings import *
#this file contains all the classes and other functions used in the game



class SoundManager:
    #class to manage sounds and music
    def __init__(self):

        pygame.mixer.init()

        self.sounds = {
            'starting_sound': pygame.mixer.Sound('Sound/start_game_sound.wav'),
            'gameover_sound': pygame.mixer.Sound('Sound/game_over_sound.wav'),
            'hanging_sound': pygame.mixer.Sound('Sound/rope_sound.wav'),
            'levelup_sound': pygame.mixer.Sound('Sound/level_up_sound.wav'),
            'win_sound': pygame.mixer.Sound('Sound/end_game_sound.wav'),
        }


        self.music_tracks = {
            'track1': 'Music/epic_track.wav',
            'track2': 'Music/haunted_track.wav',
            'track3': 'Music/spooky_track.wav',
        }

    def play_sound(self, name):
        #function used to play a sound
        if name in self.sounds:
            self.sounds[name].play()

    def play_music(self, track_name, loop=True):
        #function used to play a music track
        if track_name in self.music_tracks:
            pygame.mixer.music.load(self.music_tracks[track_name])
            pygame.mixer.music.set_volume(0.5)  #volume of the music
            pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        #function used to stop the music
        pygame.mixer.music.stop()

    def pause_music(self):
        #function used to pause the music
        pygame.mixer.music.pause()

    def resume_music(self):
        #function used to resume the music
        pygame.mixer.music.unpause()

class Rope(pygame.sprite.Sprite):
    #class of the ropes
    def __init__(self, x, y):
        #initialization of the rope
        super().__init__()
        self.anchor = pygame.Vector2(x, y)
        self.length = None
        self.image = pygame.image.load("boutons/torch1.png").convert_alpha()  #loads rope image ( here a torch)
        self.image = pygame.transform.scale(self.image, (45, 75) )
    def attach(self, ball):
        #function used to attach the rope to the ball
        self.length = (ball.pos - self.anchor).length()
        ball.is_attached, ball.attached_rope = True, self
        ball.initial_velocity = ball.velocity.length()

    def update(self, ball):
        #function used to update the rope's length
        if ball.is_attached and ball.attached_rope == self:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.length = max(10, self.length - 2)
            direction = ball.pos - self.anchor
            distance = direction.length()
            if distance > self.length:
                ball.pos = self.anchor + direction.normalize() * self.length

    def draw(self, screen, ball, camera_x):
        #function used to draw the rope ( a simple white line using pygame.draw.line)
        if ball.is_attached and ball.attached_rope == self:
            pygame.draw.line(screen, WHITE,
                             (self.anchor.x - camera_x, self.anchor.y),
                             (ball.pos.x - camera_x, ball.pos.y), 3)
        if ball.pos.x < 4100:
            #display of the image
            rect = self.image.get_rect(center=(self.anchor.x - camera_x, self.anchor.y))
            screen.blit(self.image, rect)

class Ball(pygame.sprite.Sprite):
    #class of the ball (here a spider) 
    def __init__(self, x, y, radius=10):
        #initialization of the ball
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
        #function used to update the ball's position and velocity
        if not self.is_alive:
            #if user lost, no ball
            return
        if keys[pygame.K_SPACE] and not self.is_attached:
            #check if user tries to attach the ball to a rope and does it
            closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
            closest_rope.attach(self)
        elif not keys[pygame.K_SPACE]:
            #if user is not pressing space, the ball is not attached to any rope
            self.is_attached = False
            self.attached_rope = None

        if self.pos.y - self.radius < 0:
            #if the ball collides with the ceiling, it stops her
            self.pos.y = self.radius
            self.velocity.y = 0

        if self.is_attached:
            #maintains the ball at the distance of the rope from the slope
            direction = self.pos - self.attached_rope.anchor
            distance = direction.length()
            if distance > 0:
                #yhe ball is attached to the rope
                direction.normalize_ip()
                theta = math.atan2(direction.x, direction.y)
                force_tangential = self.mass * GRAVITY * math.sin(theta)
                tangent = pygame.Vector2(-direction.y, direction.x)
                self.velocity += tangent * force_tangential
                self.pos += self.velocity #update velocity of the ball
                current_distance = (self.pos - self.attached_rope.anchor).length()
                if abs(current_distance - self.attached_rope.length) > 1:
                    #if the ball is too far from the rope, it is corrected
                    correction = direction * (self.attached_rope.length - current_distance)
                    self.pos += correction
                    self.velocity -= direction * direction.dot(self.velocity)
        else:
            #if not attached, ball is submitted to gravity, simulating free fall
            self.velocity.y += GRAVITY
            self.pos += self.velocity

        if self.pos.y >= HEIGHT - self.radius:
            #if the ball collides with the ground, it stops her and the level is over
            self.pos.y = HEIGHT - self.radius
            self.velocity.y = 0
            self.state = ON_GROUND

        for platform in platforms:
            #checks for a colliion between a platform and the ball
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
        #function used to draw the ball (here a spider)
        self.image = pygame.image.load("boutons/spider.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.radius * 3.7, self.radius * 3.7))
        screen.blit(self.image, (self.pos.x - camera_x - self.radius-10, self.pos.y - self.radius))

class Platform(pygame.sprite.Sprite):
    #class for the patforms
    def __init__(self, x, y, width, height, bouncy=False):
        #gives the platform its position and size
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.bouncy = bouncy

        #loads image for platform
        self.image = pygame.image.load("boutons/wood.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen, camera_x):
        #draws the platforms at their position
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))


class SlopedPlatform(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, bouncy=True):
        #gives the slope its position and size
        super().__init__()
        self.start = pygame.Vector2(x1, y1)
        self.end = pygame.Vector2(x2, y2)
        self.bouncy = bouncy
        self.thickness = 10
        self.color = GREEN if bouncy else RED

        #give the slope some properties
        self.length = int((self.end - self.start).length())
        self.angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

        #load ans displays image to the slope length and thickness
        self.base_image = pygame.image.load("boutons/wood.png").convert_alpha()
        self.base_image = pygame.transform.scale(self.base_image, (self.length, self.thickness))
        self.image = pygame.transform.rotate(self.base_image, -self.angle)

    def draw(self, screen, camera_x):
        #draws the slope at its position
        start = self.start - pygame.Vector2(camera_x, 0)
        end = self.end - pygame.Vector2(camera_x, 0)
        midpoint = (start + end) / 2

        rotated_rect = self.image.get_rect(center=midpoint)
        screen.blit(self.image, rotated_rect.topleft)

    def check_collision_and_bounce(self, ball):
        #complex function that makes the ball bounce of inclined platforms
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
                #if it's a bouncy slope, the ball bounces
                ball.velocity = ball.velocity.reflect(normal) * 1.2
            else:
                #otherwise, it dies
                ball.is_alive = False
                ball.kill()
            return True
        return False

def generate_rope_chain(index):
    #this contains arrays of ropes that are used for each level
    return [[Rope(1000, 150), Rope(1300, 100), Rope(2300, 100), Rope(3000, 100), Rope(3500, 80), Rope(5000, 100)],
            [Rope(600, 50), Rope(1000, 150), Rope(1300, 200), Rope(2000, 100), Rope(2700, 70), Rope(3200, 100), Rope(3700, 80), Rope(4000, 50), Rope(5000, 100)],
            [Rope(600, 50), Rope(950, 200), Rope(1300, 100), Rope(2075, 225), Rope(2075, 570), Rope(2575, 75), Rope(2575, 475), Rope(3000, 100), Rope(3700, 80), Rope(5000, 100)],
            [Rope(600, 50), Rope(1000, 150), Rope(1300, 200), Rope(2000, 100), Rope(2700, 70), Rope(3200, 100), Rope(3500, 80), Rope(4000, 50), Rope(5000, 100)]
            ][index]

def generate_platforms(index):
    #this contains arrays of platforms that are used for each level
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
    #this contains arrays of slopes that are used for each level
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
