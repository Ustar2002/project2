# star.py

import pygame
import settings

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 스타 이미지 로드 시도
        try:
            original_image = pygame.image.load('assets/images/star.png').convert_alpha()
        except FileNotFoundError:
            # 이미지가 없을 경우 대체 이미지 생성
            original_image = pygame.Surface((30, 30))
            original_image.fill(settings.YELLOW)
        # 이미지 크기 조정
        self.image = pygame.transform.scale(original_image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = settings.STAR_SPEED  # settings.py에 STAR_SPEED 추가 필요


    def update(self, keys):
        # 스타 이동 처리
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # 맵 경계 내에서만 이동
        self.rect.x = max(0, min(self.rect.x, settings.MAP_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, settings.MAP_HEIGHT - self.rect.height))
