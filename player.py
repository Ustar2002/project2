# player.py

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

    def update(self, platforms, enemies, jump_sound):
        keys = pygame.key.get_pressed()
        self.vel.x = 0
        self.vel.y = 0 
        gravity_direction = self.gravity_manager.current_gravity

        # 중력 방향에 따른 방향키 설정
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

        # Star 발사 처리 (예: F 키)
        if keys[pygame.K_f]:
            self.launch_star()

        # 점프 입력 처리
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.vel += self.gravity_manager.jump_vector(self.jump_strength)
            self.on_ground = False
            jump_sound.play()

        # 중력 적용
        self.vel += self.gravity_manager.gravity_vector()

        # 나머지 이동 및 충돌 처리
        self.rect.x += self.vel.x
        self.collide(platforms, 'x')
        self.rect.y += self.vel.y
        self.collide(platforms, 'y')

        # 적과의 충돌 처리
        hits = pygame.sprite.spritecollide(self, enemies, False)
        if hits:
            self.health -= 1
            if self.health > 0:
                self.respawn()
            else:
                self.kill()

        # 화면 범위를 벗어난 경우 처리
        if self.rect.top > settings.MAP_HEIGHT:
            self.health -= 1
            if self.health > 0:
                self.respawn()
            else:
                self.kill()

        if self.rect.bottom < settings.UPPER_LIMIT:
            self.health -= 1
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

