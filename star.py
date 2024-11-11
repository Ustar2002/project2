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
        self.active = False  # 스타의 활성화 상태
        self.vel = pygame.math.Vector2(0, 0)  # 스타의 속도

    def set_direction(self, direction):
        """
        스타의 이동 방향을 설정하고 활성화합니다.
        """
        directions = {
            'down': pygame.math.Vector2(0, self.speed),
            'up': pygame.math.Vector2(0, -self.speed),
            'left': pygame.math.Vector2(-self.speed, 0),
            'right': pygame.math.Vector2(self.speed, 0)
        }
        self.vel = directions.get(direction, pygame.math.Vector2(0, self.speed))
        self.active = True

    def update(self):
        if self.active:
            # 스타 이동
            self.rect.x += self.vel.x
            self.rect.y += self.vel.y

            # 맵 경계 내에서만 이동
            self.rect.x = max(0, min(self.rect.x, settings.MAP_WIDTH - self.rect.width))
            self.rect.y = max(0, min(self.rect.y, settings.MAP_HEIGHT - self.rect.height))
