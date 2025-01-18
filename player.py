import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        self.current_speed = 0

        # the direction the player moves in, 0 for standstill, 1 for forward, -1 for backward
        self.direction = 0
    
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def accelerate(self):
        if self.current_speed != PLAYER_SPEED:
            self.current_speed = pygame.math.lerp(self.current_speed, PLAYER_SPEED * self.direction, PLAYER_ACCELERATION_RATE)

    def decelerate(self):
        if self.current_speed != 0:
            self.current_speed = pygame.math.lerp(self.current_speed, 0, PLAYER_DECELERATION_RATE)

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # check if the player should move forward or backward. else decelerate
        if self.direction != 0:
            self.accelerate()
        else:
            self.decelerate()

        self.position += forward * self.current_speed * dt
        

    def shoot(self):
        if self.cooldown > 0:
            return
        
        self.cooldown = PLAYER_SHOOT_COOLDOWN
        new_shot = Shot(self.position.x, self.position.y)
        new_shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.cooldown -= dt

        if not keys[pygame.K_w] or keys[pygame.K_s]:
            self.direction = 0
        
        if keys[pygame.K_a]:
            self.rotate(dt * -1)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.direction = 1

        if keys[pygame.K_s]:
            self.direction = -1
        
        if keys[pygame.K_SPACE]:
            self.shoot()

        self.move(dt)