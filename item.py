#item.py

import pygame
import settings

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 아이템 이미지 로드
        try:
            original_image = pygame.image.load('assets/images/item.png').convert_alpha()
        except FileNotFoundError:
            original_image = pygame.Surface((30, 30))
            original_image.fill(settings.BLUE)
        self.image = pygame.transform.scale(original_image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))
