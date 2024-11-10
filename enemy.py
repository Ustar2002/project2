#enemy.py

import pygame
import settings

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, gravity_manager):
        super().__init__()
        # 적 이미지 로드
        try:
            original_image = pygame.image.load('assets/images/enemy.png').convert_alpha()
        except FileNotFoundError:
            original_image = pygame.Surface((40, 40))
            original_image.fill(settings.GREEN)
        self.image = pygame.transform.scale(original_image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))

        # 적 속성 초기화
        self.gravity_manager = gravity_manager
        self.vel = pygame.math.Vector2(0, 0)
        self.speed = settings.ENEMY_SPEED
        self.health = settings.ENEMY_HEALTH

    def update(self, platforms, puzzles):
        # 중력 방향에 따라 이동
        gravity_direction = self.gravity_manager.current_gravity
        self.vel.x, self.vel.y = 0, 0

        if gravity_direction == 'down':
            self.vel.y = self.speed
        elif gravity_direction == 'up':
            self.vel.y = -self.speed
        elif gravity_direction == 'left':
            self.vel.x = -self.speed
        elif gravity_direction == 'right':
            self.vel.x = self.speed

        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        # 맵 경계 체크 및 반전
        if self.rect.left < 0 or self.rect.right > settings.MAP_WIDTH:
            self.vel.x *= -1
        if self.rect.top < 0 or self.rect.bottom > settings.MAP_HEIGHT:
            self.vel.y *= -1

        # 퍼즐 블록과의 충돌 처리
        hits = pygame.sprite.spritecollide(self, puzzles, False)
        if hits:
            self.health -= 1
            if self.health <= 0:
                self.kill()

class EnemyType2(pygame.sprite.Sprite):
    def __init__(self, x, y, gravity_manager):
        super().__init__()
        # 적 타입 2 이미지 로드
        try:
            original_image = pygame.image.load('assets/images/enemy2.png').convert_alpha()
        except FileNotFoundError:
            original_image = pygame.Surface((40, 40))
            original_image.fill(settings.YELLOW)
        self.image = pygame.transform.scale(original_image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))

        # 적 타입 2 속성 초기화
        self.gravity_manager = gravity_manager
        self.speed = settings.ENEMY_SPEED
        self.health = settings.ENEMY_HEALTH

    def update(self, platforms, puzzles):
        # 좌우로만 이동
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > settings.MAP_WIDTH:
            self.speed *= -1
