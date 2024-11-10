#puzzle.py

import pygame
import settings

class MovableBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 이동 가능한 블록 이미지 생성
        self.image = pygame.Surface((50, 50))
        self.image.fill(settings.YELLOW)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel = pygame.math.Vector2(0, 0)

    def update(self, gravity_vector, platforms, player):
        # 중력 적용
        self.vel += gravity_vector
        # 위치 업데이트 및 충돌 처리
        self.rect.x += self.vel.x
        self.collide(platforms, 'x')
        self.rect.y += self.vel.y
        self.collide(platforms, 'y')

    def collide(self, platforms, direction):
        # 플랫폼과의 충돌 처리
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            for platform in hits:
                if direction == 'x':
                    if self.vel.x > 0:
                        self.rect.right = platform.rect.left
                    elif self.vel.x < 0:
                        self.rect.left = platform.rect.right
                    self.vel.x = 0
                elif direction == 'y':
                    if self.vel.y > 0:
                        self.rect.bottom = platform.rect.top
                    elif self.vel.y < 0:
                        self.rect.top = platform.rect.bottom
                    self.vel.y = 0
