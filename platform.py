#platform.py

import pygame
import settings
import random

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # 플랫폼의 색상을 랜덤으로 선택
        color = random.choice([settings.RED, settings.GREEN, settings.BLUE, settings.YELLOW])
        # 플랫폼 이미지 생성
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
