# boss.py

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
        self.original_image = self.image  # 기본 이미지 저장

        # 보스의 경직 이미지 로드
        try:
            stun_image = pygame.image.load('assets/images/boss_stun.png').convert_alpha()
            self.stun_image = pygame.transform.scale(stun_image, (100, 100))
        except FileNotFoundError:
            # 경직 이미지가 없을 경우 기본 이미지 사용
            self.stun_image = self.image.copy()

        # 보스의 종료 이미지 로드
        try:
            finished_image = pygame.image.load('assets/images/boss_finished.png').convert_alpha()
            self.finished_image = pygame.transform.scale(finished_image, (100, 100))
        except FileNotFoundError:
            # 종료 이미지가 없을 경우 기본 이미지 사용
            self.finished_image = self.image.copy()

        self.rect = self.image.get_rect(center=(x, y))

        # 보스 속성 초기화
        self.gravity_manager = gravity_manager
        self.health = settings.BOSS_HEALTH
        self.max_health = settings.BOSS_HEALTH  # 최대 체력 추가
        self.attack_timer = pygame.time.get_ticks()
        self.projectiles = pygame.sprite.Group()
        self.speed = settings.BOSS_SPEED

        self.is_stunned = False  # 보스의 경직 상태
        self.stun_timer = 0      # 경직 시작 시간
        self.stun_duration = settings.BOSS_STUN_DURATION  # 경직 지속 시간 (밀리초 단위)

        self.is_finished = False  # 보스의 종료 상태
        self.finish_timer = 0     # 종료 애니메이션 시작 시간
        self.finish_duration = settings.BOSS_FINISH_DURATION  # 종료 애니메이션 지속 시간 (밀리초 단위)

        self.invincible = False   # 보스의 무적 상태 플래그

    def set_invincible(self, invincible):
        self.invincible = invincible
        if invincible:
            # 무적 상태일 때 시각적 효과 (예: 반투명)
            self.image.set_alpha(128)
        else:
            # 무적 상태 해제 시 시각적 효과 복원
            self.image.set_alpha(255)

    def take_damage(self, amount):
        if not self.invincible and not self.is_finished:
            self.health -= amount
            print(f"Boss took {amount} damage! Health: {self.health}")
            if self.health <= 0:
                self.finish_boss()

    def update(self, player):
        current_time = pygame.time.get_ticks()

        if self.is_finished:
            # 종료 애니메이션 실행 중
            if current_time - self.finish_timer >= self.finish_duration:
                # 종료 애니메이션 완료
                self.kill()  # 보스 제거
            else:
                # 종료 애니메이션 진행 (예: 이미지 깜박임 또는 기타 효과 추가 가능)
                # 현재는 단순히 종료 이미지를 유지
                self.image = self.finished_image
            return  # 종료 상태일 때 나머지 업데이트 건너뜀

        if self.is_stunned:
            # 경직 상태일 때는 이동과 공격을 하지 않습니다.
            if current_time - self.stun_timer >= self.stun_duration:
                self.is_stunned = False  # 경직 해제
                self.set_invincible(False)  # 무적 해제
                self.image = self.original_image  # 기본 이미지로 복구
            else:
                self.image = self.stun_image  # 경직 이미지로 변경
                self.set_invincible(True)  # 무적 설정
            return  # 경직 상태일 때 나머지 업데이트 건너뜀

        # 보스가 활성화된 상태에서만 움직임과 공격
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
            speed = 3
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance != 0:
                vel_x = dx / distance * speed
                vel_y = dy / distance * speed
                projectile = Projectile(self.rect.centerx, self.rect.centery, vel_x, vel_y)
                self.projectiles.add(projectile)

    def finish_boss(self):
        """보스가 종료 상태로 전환될 때 호출"""
        self.is_finished = True
        self.finish_timer = pygame.time.get_ticks()
        self.image = self.finished_image
        # 보스의 모든 투사체 제거
        for projectile in self.projectiles:
            projectile.kill()
        self.projectiles.empty()
