# blood_effect.py

import pygame
import settings

class BloodEffect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 피 이미지 로드 시도
        try:
            original_image = pygame.image.load('assets/images/blood.png').convert_alpha()
            self.image = pygame.transform.scale(original_image, (30, 30))
        except FileNotFoundError:
            # 이미지가 없을 경우 빨간색 원으로 대체
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0, 128), (15, 15), 15)
        self.rect = self.image.get_rect(center=(x, y))
        self.spawn_time = pygame.time.get_ticks()
        self.duration = settings.BLOOD_EFFECT_DURATION  # 설정 파일에서 정의한 값 사용

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.duration:
            self.kill()
