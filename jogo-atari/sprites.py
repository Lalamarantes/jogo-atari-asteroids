import pygame
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.speedx = PLAYER_SPEED
            
        self.rect.x += self.speedx
        
        # Impede que o jogador saia da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        return bullet

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = BULLET_SPEED

    def update(self):
        self.rect.y += self.speedy
        # Destrói o tiro se passar do topo da tela
        if self.rect.bottom < 0:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        self.image = pygame.Surface((size, size))
        self.image.fill(ASTEROID_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        # Começa fora da tela, logo acima
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)

    def update(self):
        self.rect.y += self.speedy
