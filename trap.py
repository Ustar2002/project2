#trap.py

import pygame
import settings

class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # 함정 이미지 생성
        self.image = pygame.Surface((width, height))
        self.image.fill(settings.RED)
        self.rect = self.image.get_rect(topleft=(x, y))
