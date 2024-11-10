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

        # 스타의 초기 속도
        self.vel = pygame.math.Vector2(0, 0)
        
        # 중력 매니저 참조
        self.gravity_manager = gravity_manager

    def update(self):
        # 중력 적용
        if self.apply_gravity:
            self.vel += self.gravity_manager.gravity_vector()
        # 위치 업데이트
        self.rect.x += int(self.vel.x)
        self.rect.y += int(self.vel.y)
        # 화면 밖으로 나가면 제거
        if (self.rect.right < 0 or self.rect.left > settings.MAP_WIDTH or
            self.rect.bottom < 0 or self.rect.top > settings.MAP_HEIGHT):
            self.kill()