#flag.py

import pygame
import settings

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 깃발 이미지 로드
        try:
            original_image = pygame.image.load('assets/images/flag.png').convert_alpha()
        except FileNotFoundError:
            original_image = pygame.Surface((40, 80))
            original_image.fill(settings.YELLOW)
        self.image = pygame.transform.scale(original_image, (40, 80))
        self.rect = self.image.get_rect(center=(x, y))
