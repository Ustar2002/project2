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

    def update(self):
        # 스타는 기본적으로 움직이지 않으므로 업데이트 로직이 필요 없습니다.
        pass
