#gravity.py

import pygame
import settings

class GravityManager:
    def __init__(self):
        # 중력 벡터 및 방향 초기화
        self.gravity = pygame.math.Vector2(0, 1)
        self.current_gravity = 'down'

        # 중력 제어 관련 설정
        self.gravity_duration = settings.GRAVITY_DURATION
        self.max_gravity_control = settings.MAX_GRAVITY_CONTROL
        self.current_gravity_control = self.max_gravity_control
        self.recharge_delay = settings.GRAVITY_RECHARGE_DELAY
        self.recharge_rate = settings.GRAVITY_RECHARGE_RATE

        # 타이머 초기화
        self.gravity_timer = 0
        self.last_used_time = pygame.time.get_ticks()

    def set_gravity(self, direction):
        if self.current_gravity_control <= 0:
            return

        # 중력 방향 설정
        directions = {
            'down': pygame.math.Vector2(0, 1),
            'up': pygame.math.Vector2(0, -1),
            'left': pygame.math.Vector2(-1, 0),
            'right': pygame.math.Vector2(1, 0)
        }
        self.gravity = directions.get(direction, pygame.math.Vector2(0, 1))
        self.current_gravity = direction

        # 중력 제어량 감소 및 타이머 재설정
        self.current_gravity_control -= 1
        self.gravity_timer = pygame.time.get_ticks()
        self.last_used_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()

        # 중력 지속 시간 체크
        if self.gravity_timer and (current_time - self.gravity_timer) / 1000 >= self.gravity_duration:
            self.reset_gravity()

        # 중력 제어량 회복
        if (current_time - self.last_used_time) / 1000 >= self.recharge_delay:
            self.current_gravity_control = min(
                self.current_gravity_control + self.recharge_rate * (1 / settings.FPS),
                self.max_gravity_control
            )

    def reset_gravity(self):
        self.gravity = pygame.math.Vector2(0, 1)
        self.current_gravity = 'down'
        self.gravity_timer = 0

    def gravity_vector(self):
        return self.gravity

    def jump_vector(self, strength):
        # 중력 방향에 따른 점프 벡터 설정
        jumps = {
            'down': pygame.math.Vector2(0, -strength),
            'up': pygame.math.Vector2(0, strength),
            'left': pygame.math.Vector2(strength, 0),
            'right': pygame.math.Vector2(-strength, 0)
        }
        return jumps.get(self.current_gravity, pygame.math.Vector2(0, -strength))
