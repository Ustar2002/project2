#boss.py

import pygame
import settings
from projectile import Projectile

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, gravity_manager):
        super().__init__()
        # 보스 이미지 로드
        try:
            original_image = pygame.image.load('assets/images/boss.png').convert_alpha()
        except FileNotFoundError:
            # 이미지가 없을 경우 대체 이미지 생성
            original_image = pygame.Surface((100, 100))
            original_image.fill(settings.PURPLE)
        self.image = pygame.transform.scale(original_image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))

        # 보스 속성 초기화
        self.gravity_manager = gravity_manager
        self.health = settings.BOSS_HEALTH
        self.attack_timer = pygame.time.get_ticks()
        self.projectiles = pygame.sprite.Group()
        self.speed = settings.BOSS_SPEED

        self.is_stunned = False  # 보스의 경직 상태
        self.stun_timer = 0      # 경직 시작 시간
        self.stun_duration = 2000  # 경직 지속 시간 (밀리초 단위)

    def update(self, player):
        current_time = pygame.time.get_ticks()

        if self.is_stunned:
            # 경직 상태일 때는 이동과 공격을 하지 않습니다.
            if current_time - self.stun_timer >= self.stun_duration:
                self.is_stunned = False  # 경직 해제
        else:
            self.move_towards_player(player)
            self.attack_pattern(player, current_time)
            
        self.projectiles.update()

    def move_towards_player(self, player):
        # 플레이어를 향해 이동
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance != 0:
            self.rect.x += int(dx / distance * self.speed)
            self.rect.y += int(dy / distance * self.speed)

    def attack_pattern(self, player, current_time):
        # 보스 체력에 따라 공격 패턴 변화
        if self.health > settings.BOSS_HEALTH * 0.5:
            attack_interval = 1000  # 1초마다 공격
        else:
            attack_interval = 700   # 0.7초마다 공격

        if current_time - self.attack_timer > attack_interval:
            self.attack_timer = current_time
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            speed = 7
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance != 0:
                vel_x = dx / distance * speed
                vel_y = dy / distance * speed
                projectile = Projectile(self.rect.centerx, self.rect.centery, vel_x, vel_y)
                self.projectiles.add(projectile)