# camera.py

import pygame
import settings

class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.scroll_speed = settings.CAMERA_SCROLL_SPEED
        self.fixed_position = None
        self.target = None  # 카메라가 따라갈 대상

    def apply(self, entity):
        # 카메라 이동에 따른 엔티티 위치 조정
        return entity.rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def update(self):
        if self.fixed_position:
            # 고정된 위치로 카메라 설정 (보스방 등)
            self.camera_rect.center = self.fixed_position
            # 화면 경계 체크
            self.camera_rect.x = max(0, min(self.camera_rect.x, self.width - settings.SCREEN_WIDTH))
            self.camera_rect.y = max(0, min(self.camera_rect.y, self.height - settings.SCREEN_HEIGHT))
        elif self.target:
            # 부드러운 카메라 이동을 위한 보간
            target_x = self.target.rect.centerx - settings.SCREEN_WIDTH // 2
            target_y = self.target.rect.centery - settings.SCREEN_HEIGHT // 2
            self.camera_rect.x += (target_x - self.camera_rect.x) * 0.1
            self.camera_rect.y += (target_y - self.camera_rect.y) * 0.1

            # 맵 경계 안으로 제한
            self.camera_rect.x = max(0, min(self.camera_rect.x, self.width - settings.SCREEN_WIDTH))
            self.camera_rect.y = max(0, min(self.camera_rect.y, self.height - settings.SCREEN_HEIGHT))

        else:
            # 카메라 자동 스크롤
            self.camera_rect.x += self.scroll_speed
            self.camera_rect.x = max(0, min(self.camera_rect.x, self.width - settings.SCREEN_WIDTH))

    def update_target(self, target):
        # 카메라가 따라갈 대상을 설정
        self.target = target
