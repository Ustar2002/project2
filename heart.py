#heart.py

import pygame
import settings

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 하트 이미지 로드
        try:
            original_image = pygame.image.load('assets/images/heart.png').convert_alpha()
        except FileNotFoundError:
            original_image = pygame.Surface((30, 30))
            original_image.fill(settings.RED)
        self.image = pygame.transform.scale(original_image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))
