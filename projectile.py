#projectile.py

import pygame
import settings

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, vel_x, vel_y):
        super().__init__()
        # 투사체 이미지 생성
        self.image = pygame.Surface((10, 10))
        self.image.fill(settings.RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = pygame.math.Vector2(vel_x, vel_y)

    def update(self):
        # 투사체 위치 업데이트
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        # 화면 밖으로 나가면 삭제
        if (self.rect.right < 0 or self.rect.left > settings.MAP_WIDTH or
            self.rect.bottom < 0 or self.rect.top > settings.MAP_HEIGHT):
            self.kill()
