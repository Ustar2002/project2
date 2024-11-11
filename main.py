# main.py

import pygame
import sys
import random
from player import Player
from gravity import GravityManager
from level import Level
from camera import Camera
from enemy import Enemy, EnemyType2
from item import Item
from flag import Flag
from heart import Heart
from platform import Platform
from star import Star
from blood_effect import BloodEffect
from boss import Boss  

import settings
import time
import traceback  # 예외 스택 추적을 위한 모듈


# 초기화
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Project2_2022105744_정유성")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)
jump_sound = pygame.mixer.Sound('assets/sounds/jump.wav')
stomp_sound = pygame.mixer.Sound('assets/sounds/stomp.wav')  

# 보스방에서 사용할 변수 초기화
star_spawn_timer = pygame.time.get_ticks()
STAR_SPAWN_INTERVAL = 5000  # 5초마다 스타 생성

# 중력 매니저 생성
gravity_manager = GravityManager()

# 레벨 데이터 리스트
level_data_list = [
    {
        # 첫 번째 레벨 데이터
        'platforms': [
            settings.INITIAL_PLATFORM_POSITION,
            (500, 400, 200, 20),
            (700, 300, 200, 20),
            (900, 200, 20, 200),
            (1100, 400, 150, 20),
            (1300, 500, 200, 30),
            (1500, 300, 100, 200),
            (1700, 500, 200, 20),
            (1900, 600, 100, 20),
            (2100, 200, 30, 250),
            (2300, 400, 200, 50),
            (2500, 300, 150, 20),
            (2700, 500, 300, 20),
            (2900, 250, 200, 20),
            (3100, 300, 20, 300),
            (3300, 400, 250, 20),
            (3500, 500, 200, 20),
            (3700, 600, 100, 20),
            (3900, 400, 20, 300),
            (4100, 600, 300, 30),
            (4300, 300, 200, 20),
            (4500, 200, 20, 250),
        ],
        # 적 데이터
        'enemies': [
            (550, 350),
            (1350, 450),
            (1950, 350),
            (2750, 250),
            (3550, 250),
            (4150, 450),
        ],
        # 적 타입 2 데이터
        'enemies_type2': [
            (1200, 400),
            (2000, 600),
            (2800, 500),
            (3600, 400),
            (4400, 300),
        ],
        # 아이템 데이터
        'items': [
            (600, 450),
            (1600, 350),
            (2600, 250),
            (3600, 450),
            (4600, 350),
        ],
        # 퍼즐 데이터
        'puzzles': [
            (350, 450),
            (1250, 350),
            (2250, 250),
            (3250, 450),
            (4250, 350),
        ],
        # 트랩 데이터
        'traps': [
            (800, 580, 100, 20),
            (1800, 580, 100, 20),
            (2800, 580, 100, 20),
            (3800, 580, 100, 20),
            (4800, 580, 100, 20),
        ],
        'is_boss_level': False,
        'boss_position': None,
        'flag_position': (4800, 150)  # 맵 끝에 맞춘 플래그 위치
    },
    {
        # 보스방 레벨 데이터
        'platforms': [
            (4000, 200, 20, 600),    # 왼쪽 벽
            (4780, 200, 20, 600),    # 오른쪽 벽
            (4000, 200, 800, 20),    # 상단 벽
            (4000, 780, 800, 20),    # 하단 벽
            # 내부 플랫폼
        ],
        'enemies': [],
        'enemies_type2': [],
        'items': [],
        'puzzles': [],
        'traps': [],
        'stars': [  # 스타 스프라이트의 초기 위치 
            (4200, 550),
            (4300, 550),
        ],
        'is_boss_level': True,
        'boss_position': (4400, 500),           # 보스 위치
        'boss_room_center': (4400, 500),        # 보스방 중앙 좌표
        'player_start_position': (4400, 700),   # 플레이어 시작 위치
        'gravity_condition': 'down',
    }
]

# 게임 상태 변수
current_level_index = 0
current_level_data = level_data_list[current_level_index]
current_level = Level(current_level_data, gravity_manager)
is_boss_level_active = False  # 보스방 활성화 여부
game_over = False
victory = False  # 보스 클리어 여부
running = True

# 플레이어 생성
player = Player(gravity_manager)
camera = Camera(settings.MAP_WIDTH, settings.MAP_HEIGHT)
all_sprites = pygame.sprite.Group()
all_sprites.add(current_level.platforms, current_level.enemies, current_level.enemies_type2,
                current_level.items, current_level.puzzles, current_level.traps, player)

# 클리어 시간 측정을 위한 변수
level_start_time = pygame.time.get_ticks()
level_end_time = None

def reset_game(start_from_boss=False):
    # 게임 초기화 함수
    global current_level, player, camera, all_sprites, game_over, is_boss_level_active
    global current_level_index, current_level_data, star_spawn_timer

    current_level_index = 1 if start_from_boss else 0
    current_level_data = level_data_list[current_level_index]
    current_level = Level(current_level_data, gravity_manager)

    player = Player(gravity_manager)
    player.health = settings.PLAYER_HEALTH  # 체력 초기화
    if not start_from_boss:
        player.rect.centerx, player.rect.bottom = settings.INITIAL_PLATFORM_POSITION[:2]
    else:
        player.rect.centerx = current_level_data['player_start_position'][0]
        player.rect.bottom = current_level_data['player_start_position'][1]

    camera = Camera(settings.MAP_WIDTH, settings.MAP_HEIGHT)
    camera.fixed_position = None  # 카메라 고정 해제

    # all_sprites를 새로 생성
    all_sprites = pygame.sprite.Group()
    
    all_sprites.add(current_level.platforms.sprites())
    all_sprites.add(current_level.enemies.sprites())
    all_sprites.add(current_level.enemies_type2.sprites())
    all_sprites.add(current_level.items.sprites())
    all_sprites.add(current_level.puzzles.sprites())
    all_sprites.add(current_level.traps.sprites())
    all_sprites.add(player)
    
    if current_level.boss:
        all_sprites.add(current_level.boss)
        print("Boss has been added to all_sprites during reset_game.")
        # 보스의 투사체는 여기서 추가하지 않습니다.

    if current_level.flag:
        all_sprites.add(current_level.flag)  # all_sprites가 정의된 후에 호출

    if start_from_boss and current_level.stars:
        for star in current_level.stars:
            all_sprites.add(star)
            print(f"Star at ({star.rect.centerx}, {star.rect.centery}) has been added to all_sprites during reset_game.")
    
    game_over = False
    victory = False

    if start_from_boss:
        is_boss_level_active = True

        # 카메라 타겟 설정
        camera.update_target(player)

        # 스타 스폰 타이머 초기화
        star_spawn_timer = pygame.time.get_ticks()

    else:
        is_boss_level_active = False

# 초기 게임 상태 설정
reset_game()
checkpoint_position = (900, 200)
enemy_spawn_timer = pygame.time.get_ticks()
heart_spawn_timer = pygame.time.get_ticks()
heart_group = pygame.sprite.Group()
ENEMY_SPAWN_INTERVAL = 5000
ENEMY_SPAWN_RADIUS = 300

def show_countdown():
    # 카운트다운 표시 함수
    font_large = pygame.font.SysFont('Arial', 72)
    for i in range(3, 0, -1):
        screen.fill(settings.BLACK)
        countdown_text = font_large.render(str(i), True, settings.WHITE)
        screen.blit(countdown_text, (settings.SCREEN_WIDTH // 2 - countdown_text.get_width() // 2,
                                     settings.SCREEN_HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(1000)

def show_game_over_screen():
    # 게임 오버 화면 표시 함수
    screen.fill(settings.BLACK)
    font_large = pygame.font.SysFont('Arial', 48)
    game_over_text = font_large.render('Game Over', True, settings.WHITE)
    prompt_text = font.render('Do you want to play again? Y/N', True, settings.WHITE)

    screen.blit(game_over_text, (settings.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                 settings.SCREEN_HEIGHT // 2 - 100))
    screen.blit(prompt_text, (settings.SCREEN_WIDTH // 2 - prompt_text.get_width() // 2,
                              settings.SCREEN_HEIGHT // 2))

    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(settings.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting = False
                    return True
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()

def show_victory_screen():
    # 보스 클리어 화면 표시 함수
    screen.fill(settings.BLACK)
    font_large = pygame.font.SysFont('Arial', 48)
    victory_text = font_large.render('Congratulations! You Defeated the Boss!', True, settings.WHITE)
    clear_time = (level_end_time - level_start_time) / 1000  # 초 단위로 변환
    time_text = font.render(f'Clear Time: {clear_time:.2f} seconds', True, settings.WHITE)
    prompt_text = font.render('Do you want to play again? Y/N', True, settings.WHITE)

    screen.blit(victory_text, (settings.SCREEN_WIDTH // 2 - victory_text.get_width() // 2,
                               settings.SCREEN_HEIGHT // 2 - 100))
    screen.blit(time_text, (settings.SCREEN_WIDTH // 2 - time_text.get_width() // 2,
                            settings.SCREEN_HEIGHT // 2 - 50))
    screen.blit(prompt_text, (settings.SCREEN_WIDTH // 2 - prompt_text.get_width() // 2,
                              settings.SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(settings.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting = False
                    reset_game(start_from_boss=False)
                    show_countdown()
                    return True
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()

def draw_boss_health_bar(screen, boss, font):
    if boss is None or not boss.alive():
        return

    # 보스 체력 정보 가져오기
    boss_health = boss.health
    boss_max_health = boss.max_health  # 수정: settings.BOSS_HEALTH 대신 boss.max_health

    # 체력 바의 크기와 위치 설정
    bar_width = settings.BOSS_HEALTH_BAR_WIDTH
    bar_height = settings.BOSS_HEALTH_BAR_HEIGHT
    margin = settings.BOSS_HEALTH_BAR_MARGIN
    x = settings.SCREEN_WIDTH - bar_width - margin
    y = margin

    # 배경 바 그리기 (빨간색)
    pygame.draw.rect(screen, settings.BOSS_HEALTH_BAR_BG_COLOR, (x, y, bar_width, bar_height))

    # 현재 체력에 따른 채워진 바의 너비 계산
    current_bar_width = int(bar_width * (boss_health / boss_max_health))

    # 체력 비율에 따른 색상 변화
    if boss_health > boss_max_health * 0.6:
        bar_color = settings.BOSS_HEALTH_BAR_FG_COLOR  # 녹색
    elif boss_health > boss_max_health * 0.3:
        bar_color = (255, 255, 0)  # 노란색
    else:
        bar_color = (255, 0, 0)  # 빨간색

    # 채워진 바 그리기 (녹색/노란색/빨간색)
    pygame.draw.rect(screen, bar_color, (x, y, current_bar_width, bar_height))

    # 보스 체력 텍스트 표시
    health_text = font.render(f'Boss Health: {boss_health}/{boss_max_health}', True, settings.BOSS_HEALTH_TEXT_COLOR)
    text_rect = health_text.get_rect(center=(x + bar_width // 2, y + bar_height + 10))
    screen.blit(health_text, text_rect)

def transition_to_boss_level():
    global current_level_index, current_level_data, current_level
    global player, all_sprites, camera, is_boss_level_active
    global star_spawn_timer  # 전역 변수로 선언

    print("Transitioning to boss level.")
    # 보스 레벨로 업데이트
    current_level_index = 1
    current_level_data = level_data_list[current_level_index]
    current_level = Level(current_level_data, gravity_manager)

    # 플레이어 위치 및 체력 초기화
    player.health = settings.PLAYER_HEALTH
    player.rect.centerx = current_level_data['player_start_position'][0]
    player.rect.bottom = current_level_data['player_start_position'][1]
    is_boss_level_active = True

    # 스프라이트 그룹 재설정
    all_sprites.empty()
    all_sprites.add(current_level.platforms.sprites())
    all_sprites.add(current_level.enemies.sprites())
    all_sprites.add(current_level.enemies_type2.sprites())
    all_sprites.add(current_level.items.sprites())
    all_sprites.add(current_level.puzzles.sprites())
    all_sprites.add(current_level.traps.sprites())
    all_sprites.add(current_level.stars.sprites()) 
    all_sprites.add(player)
    if current_level.boss:
        all_sprites.add(current_level.boss)
        print("Boss has been added to all_sprites.")
    else:
        print("Boss is not available or already dead.")

    # 카메라 고정 위치 설정
    camera.fixed_position = None  # 이 줄을 수정하여 카메라 고정 해제
    camera.target = player        # 카메라가 플레이어를 따라가도록 설정

    # 보스방 관련 변수 초기화
    star_spawn_timer = pygame.time.get_ticks()  # 스타 스폰 타이머 초기화

def activate_stars(direction):
    """
    모든 스타를 활성화하여 주어진 방향으로 이동하게 합니다.
    """
    for star in current_level.stars:
        if not star.active:
            star.set_direction(direction)
            print(f"Star at ({star.rect.centerx}, {star.rect.centery}) activated to move {direction}.")

# 메인 루프
show_countdown()

try:
    while running:
        if game_over:
            play_again = show_game_over_screen()
            if play_again:
                # 보스방에서 죽었다면 보스방에서 리트라이
                reset_game(start_from_boss=False)  # 보스방에서 죽었을 때 시작 위치로 리스폰
                show_countdown()
                continue
            else:
                running = False
                break

        current_time = pygame.time.get_ticks()
        clock.tick(settings.FPS)

        if not is_boss_level_active:
            # 적 스폰 로직은 보스방이 아닐 때만 실행
            if current_time - enemy_spawn_timer > ENEMY_SPAWN_INTERVAL:
                enemy_spawn_timer = current_time
                while True:
                    spawn_x = random.randint(int(camera.camera_rect.x), int(camera.camera_rect.x + settings.SCREEN_WIDTH))
                    spawn_y = random.randint(0, settings.MAP_HEIGHT - 100)
                    distance_to_player = ((spawn_x - player.rect.centerx) ** 2 + (spawn_y - player.rect.centery) ** 2) ** 0.5
                    if distance_to_player > ENEMY_SPAWN_RADIUS:
                        break

                if random.choice([True, False]):
                    new_enemy = Enemy(spawn_x, spawn_y, gravity_manager)
                    current_level.enemies.add(new_enemy)
                    print(f"Spawned EnemyType1 at ({spawn_x}, {spawn_y}).")
                else:
                    new_enemy = EnemyType2(spawn_x, spawn_y, gravity_manager)
                    current_level.enemies_type2.add(new_enemy)
                    print(f"Spawned EnemyType2 at ({spawn_x}, {spawn_y}).")
                all_sprites.add(new_enemy)

        if is_boss_level_active:
            # 스타 스프라이트 주기적으로 생성 (최대 3개)
            if current_time - star_spawn_timer > STAR_SPAWN_INTERVAL:
                if len(current_level.stars) < 3:
                    star_spawn_timer = current_time
                    # 스타를 보스방 내부 플랫폼에 랜덤하게 생성
                    star_x = random.randint(4020 + 30, 4780 - 30)  # 벽 두께와 스타 크기를 고려
                    star_y = random.randint(220, 780 - 30)
                    new_star = Star(star_x, star_y)
                    current_level.stars.add(new_star)
                    all_sprites.add(new_star)
                    print(f"Spawned Star at ({star_x}, {star_y}).")

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # 중력 방향 변경
                if event.key == pygame.K_UP:
                    gravity_manager.set_gravity('up')
                    activate_stars('up')
                elif event.key == pygame.K_DOWN:
                    gravity_manager.set_gravity('down')
                    activate_stars('down')
                elif event.key == pygame.K_LEFT:
                    gravity_manager.set_gravity('left')
                    activate_stars('left')
                elif event.key == pygame.K_RIGHT:
                    gravity_manager.set_gravity('right')
                    activate_stars('right')

        # 키보드 입력 상태 가져오기
        keys = pygame.key.get_pressed()

        # 업데이트 로직
        gravity_manager.update()
        player.update(current_level.platforms, current_level.enemies, jump_sound)
        current_level.puzzles.update(gravity_manager.gravity_vector(), current_level.platforms, player)
        current_level.enemies.update(current_level.platforms, current_level.puzzles)
        current_level.enemies_type2.update(current_level.platforms, current_level.puzzles)

        # 아이템 및 하트 처리
        item_hits = pygame.sprite.spritecollide(player, current_level.items, True)
        if item_hits:
            player.health = min(player.health + 1, settings.PLAYER_HEALTH)
            print(f"Player picked up an item. Health: {player.health}")

        current_time = pygame.time.get_ticks()
        if current_time - heart_spawn_timer > settings.HEART_SPAWN_INTERVAL:
            heart_spawn_timer = current_time
            heart_x = random.randint(100, settings.MAP_WIDTH - 100)
            heart_y = random.randint(100, settings.MAP_HEIGHT - 100)
            new_heart = Heart(heart_x, heart_y)
            heart_group.add(new_heart)
            all_sprites.add(new_heart)
            print(f"Spawned Heart at ({heart_x}, {heart_y}).")

        heart_hits = pygame.sprite.spritecollide(player, heart_group, True)
        if heart_hits:
            player.health = min(player.health + 1, settings.PLAYER_HEALTH)
            print(f"Player picked up a heart. Health: {player.health}")

        # 충돌 처리
        if current_level.flag and pygame.sprite.collide_rect(player, current_level.flag):
            print("Congratulations! You reached the flag!")
            transition_to_boss_level()
            continue

        if current_level.boss and current_level.boss.alive():
            current_level.boss.update(player)
            current_level.boss.projectiles.update()

            # 보스의 투사체와 플레이어의 충돌 처리
            boss_projectile_hits = pygame.sprite.spritecollide(player, current_level.boss.projectiles, True)
            if boss_projectile_hits:
                player.take_damage(1)
                print(f"Player hit by boss's projectile. Health: {player.health}")
                if player.health <= 0:
                    game_over = True

            # 보스의 투사체와 스타의 충돌 처리
            # 스타가 보스의 투사체와 충돌 시 스타 제거
            for projectile in current_level.boss.projectiles:
                star_hits = pygame.sprite.spritecollide(projectile, current_level.stars, True)
                if star_hits:
                    projectile.kill()
                    print(f"Projectile at ({projectile.rect.centerx}, {projectile.rect.centery}) hit a star and was removed.")

            # 보스와 스타의 충돌 처리
            boss_star_hits = pygame.sprite.spritecollide(
                current_level.boss,
                current_level.stars,
                True  # 스타는 제거
            )
            if boss_star_hits:
                current_level.boss.take_damage(30)
                current_level.boss.is_stunned = True
                current_level.boss.stun_timer = pygame.time.get_ticks()
                print(f"Boss hit by a star. Health: {current_level.boss.health}")

            # 보스와 플레이어의 충돌 처리
            if pygame.sprite.collide_rect(player, current_level.boss):
                # 플레이어가 보스를 밟았는지 확인
                if (player.vel.y > 0) and (player.prev_rect.bottom <= current_level.boss.rect.top):
                    # 플레이어가 보스를 밟음
                    current_level.boss.take_damage(settings.BOSS_STOMP_DAMAGE)  # 설정 파일에서 정의한 값 사용
                    current_level.boss.is_stunned = True
                    current_level.boss.stun_timer = pygame.time.get_ticks()

                    # 피 효과 추가
                    blood = BloodEffect(current_level.boss.rect.centerx, current_level.boss.rect.top)
                    all_sprites.add(blood)
                    print("Boss stomped by player.")

                    # 플레이어 점프 (보스 밟은 후 반동 효과)
                    player.vel.y = -player.jump_strength / 2  # 반동 높이 조절

                    # 소리 효과 추가
                    stomp_sound.play()

                    # 보스 체력이 0 이하이면 보스 종료 애니메이션 실행
                    if current_level.boss.health <= 0:
                        current_level.boss.finish_boss()
                        level_end_time = pygame.time.get_ticks()  # 클리어 시간 기록
                        victory = True  # 승리 상태 설정
                        print("Boss defeated!")
                else:
                    # 보스와의 일반적인 충돌 (플레이어 체력 감소)
                    player.take_damage(1)
                    print(f"Player collided with boss. Health: {player.health}")
                    if player.health <= 0:
                        game_over = True

        # 적과의 충돌 처리
        enemy_hits = pygame.sprite.spritecollide(player, current_level.enemies, False)
        enemy_type2_hits = pygame.sprite.spritecollide(player, current_level.enemies_type2, False)
        if enemy_hits or enemy_type2_hits:
            player.take_damage(1)
            print(f"Player collided with enemy. Health: {player.health}")
            if player.health <= 0:
                game_over = True

        trap_hits = pygame.sprite.spritecollide(player, current_level.traps, False)
        if trap_hits:
            player.take_damage(1)
            print(f"Player hit by trap. Health: {player.health}")
            if player.health > 0:
                player.respawn()
                print("Player respawned.")
            else:
                game_over = True

        # 카메라 업데이트
        camera.update()

        if not camera.camera_rect.colliderect(player.rect):
            player.take_damage(10)
            print(f"Player went out of camera view. Health: {player.health}")
            if player.health > 0:
                player.respawn()
                print("Player respawned after going out of view.")
            else:
                game_over = True

        # 스타 스프라이트 업데이트 (중력 방향에 따라 이동)
        current_level.stars.update()

        # 스타와 플랫폼 충돌 처리
        for star in current_level.stars:
            # 스타가 플랫폼과 충돌하면 제거
            if pygame.sprite.spritecollideany(star, current_level.platforms):
                star.kill()
                print(f"Star at ({star.rect.centerx}, {star.rect.centery}) collided with a platform and was removed.")
            # 스타가 보스와 충돌하면 데미지를 주고 제거
            if is_boss_level_active and current_level.boss and pygame.sprite.collide_rect(star, current_level.boss):
                current_level.boss.take_damage(10)  # 원하는 데미지 설정
                star.kill()
                print(f"Star at ({star.rect.centerx}, {star.rect.centery}) collided with boss and was removed.")

        if is_boss_level_active and victory:
            show_victory_screen()
            reset_game(start_from_boss=False)
            show_countdown()
            continue

        # 화면 그리기
        screen.fill(settings.BLACK)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        # 보스의 투사체 그리기
        if current_level.boss and current_level.boss.alive():
            for projectile in current_level.boss.projectiles:
                screen.blit(projectile.image, camera.apply(projectile))

        # 스타 스프라이트 그리기
        for star in current_level.stars:
            screen.blit(star.image, camera.apply(star))
        
        # 보스 체력 바 그리기
        if is_boss_level_active and current_level.boss and current_level.boss.alive():
            draw_boss_health_bar(screen, current_level.boss, font)

        # UI 요소 그리기
        health_text = font.render(f'Health: {player.health}', True, settings.WHITE)
        screen.blit(health_text, (10, 10))

        gravity_control_text = font.render(
            f'Gravity Control: {int(gravity_manager.current_gravity_control)}/{gravity_manager.max_gravity_control}',
            True,
            settings.WHITE
        )
        screen.blit(gravity_control_text, (10, 40))

        pygame.display.flip()
except Exception as e:
    print(f'An error occurred: {e}')
    traceback.print_exc()  # 예외 스택 트레이스 출력
finally:
    pygame.quit()
    sys.exit()
