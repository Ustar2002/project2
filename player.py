#player.py

import pygame
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self, gravity_manager):
        super().__init__()
        # 플레이어 이미지 로드 시도
        try:
            original_image = pygame.image.load('assets/images/player.png').convert_alpha()
        except FileNotFoundError:
            # 이미지가 없을 경우 대체 이미지 생성
            original_image = pygame.Surface((50, 50))
            original_image.fill(settings.WHITE)
        # 이미지 크기 조정
        self.image = pygame.transform.scale(original_image, (50, 50))
        self.rect = self.image.get_rect()
        # 초기 위치 설정
        initial_platform = settings.INITIAL_PLATFORM_POSITION
        self.rect.centerx = initial_platform[0] + initial_platform[2] // 2
        self.rect.bottom = initial_platform[1]

        # 플레이어 속성 초기화
        self.gravity_manager = gravity_manager
        self.vel = pygame.math.Vector2(0, 0)
        self.speed = settings.PLAYER_SPEED
        self.jump_strength = settings.PLAYER_JUMP_STRENGTH
        self.on_ground = False
        self.health = settings.PLAYER_HEALTH
        self.checkpoint = None
        self.invincible = False  # 무적 상태 플래그
        self.invincibility_timer = 0  # 무적 타이머

        # 이전 위치 추적
        self.prev_rect = self.rect.copy()
        
    def set_invincible(self, invincible):
        self.invincible = invincible
        if invincible:
            # 무적 상태일 때 시각적 효과 (예: 반투명)
            self.image.set_alpha(128)
            self.invincibility_timer = pygame.time.get_ticks()
        else:
            # 무적 상태 해제 시 시각적 효과 복원
            self.image.set_alpha(255)

    def take_damage(self, amount):
        if not self.invincible:
            self.health -= amount
            print(f"Player took {amount} damage! Health: {self.health}")
            self.set_invincible(True)  # 무적 상태로 설정

    def update(self, platforms, enemies, jump_sound):
        # 이전 위치 저장 (이동하기 전에 저장)
        self.prev_rect = self.rect.copy()

        current_time = pygame.time.get_ticks()

        # 무적 시간 체크
        if self.invincible and (current_time - self.invincibility_timer >= settings.PLAYER_INVINCIBILITY_DURATION):
            self.set_invincible(False)

        keys = pygame.key.get_pressed()
        self.vel.x = 0
        gravity_direction = self.gravity_manager.current_gravity

        # 중력 방향에 따른 이동 처리
        if gravity_direction == 'down':
            if keys[pygame.K_a]:
                self.vel.x = -self.speed
            if keys[pygame.K_d]:
                self.vel.x = self.speed
        elif gravity_direction == 'up':
            if keys[pygame.K_a]:
                self.vel.x = self.speed
            if keys[pygame.K_d]:
                self.vel.x = -self.speed
        elif gravity_direction == 'left':
            if keys[pygame.K_a]:
                self.vel.y = self.speed
            if keys[pygame.K_d]:
                self.vel.y = -self.speed
        elif gravity_direction == 'right':
            if keys[pygame.K_a]:
                self.vel.y = -self.speed
            if keys[pygame.K_d]:
                self.vel.y = self.speed

        # 점프 처리
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.vel += self.gravity_manager.jump_vector(self.jump_strength)
            self.on_ground = False
            jump_sound.play()

        # 중력 적용
        self.vel += self.gravity_manager.gravity_vector()

        # 위치 업데이트 및 충돌 처리
        self.rect.x += self.vel.x
        self.collide(platforms, 'x')
        self.rect.y += self.vel.y
        self.collide(platforms, 'y')

        # 적과의 충돌 처리
        hits = pygame.sprite.spritecollide(self, enemies, False)
        if hits:
            self.take_damage(1)
            if self.health <= 0:
                self.kill()

        # 화면 밖으로 나갔을 때 처리
        if self.rect.top > settings.MAP_HEIGHT or self.rect.bottom < settings.UPPER_LIMIT:
            self.take_damage(10)
            if self.health > 0:
                self.respawn()
            else:
                self.kill()

    def collide(self, platforms, direction):
        # 플랫폼과의 충돌 처리
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            for platform in hits:
                if direction == 'x':
                    if self.vel.x > 0:
                        self.rect.right = platform.rect.left
                    elif self.vel.x < 0:
                        self.rect.left = platform.rect.right
                    self.vel.x = 0
                elif direction == 'y':
                    if self.vel.y > 0:
                        self.rect.bottom = platform.rect.top
                        self.on_ground = True
                    elif self.vel.y < 0:
                        self.rect.top = platform.rect.bottom
                    self.vel.y = 0
        else:
            if direction == 'y':
                self.on_ground = False

    def respawn(self):
        # 플레이어를 체크포인트나 초기 위치로 리스폰
        if self.checkpoint:
            self.rect.center = self.checkpoint
        else:
            initial_platform = settings.INITIAL_PLATFORM_POSITION
            self.rect.centerx = initial_platform[0] + initial_platform[2] // 2
            self.rect.bottom = initial_platform[1]
        self.vel = pygame.math.Vector2(0, 0)

    def set_checkpoint(self, position):
        # 체크포인트 설정
        self.checkpoint = position
