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

import settings

# 초기화
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Project2_2022105744_정유성")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)
jump_sound = pygame.mixer.Sound('assets/sounds/jump.wav')
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
running = True

# 플레이어 생성
player = Player(gravity_manager)
camera = Camera(settings.MAP_WIDTH, settings.MAP_HEIGHT)
all_sprites = pygame.sprite.Group()
all_sprites.add(current_level.platforms, current_level.enemies, current_level.enemies_type2,
                current_level.items, current_level.puzzles, current_level.traps, player)


def reset_game(start_from_boss=False):
    # 게임 초기화 함수
    global current_level, player, camera, all_sprites, game_over, is_boss_level_active
    current_level_index = 1 if start_from_boss else 0
    current_level_data = level_data_list[current_level_index]
    current_level = Level(current_level_data, gravity_manager)

    player = Player(gravity_manager)
    player.health = settings.PLAYER_HEALTH  # 체력 초기화
    player.rect.centerx, player.rect.bottom = settings.INITIAL_PLATFORM_POSITION[:2]

    camera = Camera(settings.MAP_WIDTH, settings.MAP_HEIGHT)
    camera.fixed_position = None  # 카메라 고정 해제
    
    # 여기에서 all_sprites를 생성합니다.
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
        # 보스의 투사체는 여기서 추가하지 않습니다.

    if current_level.flag:
        all_sprites.add(current_level.flag)  # all_sprites가 정의된 후에 호출

    game_over = False

    if start_from_boss:
        player.rect.centerx = 4400  # 보스방의 중앙 x 좌표 (예시)
        player.rect.bottom = 700    # 보스방의 바닥에서 약간 위쪽 (예시)
        is_boss_level_active = True

        # 플레이어 아래에 플랫폼 생성 및 추가
        platform_width = 200
        platform_height = 20
        platform_x = player.rect.centerx - platform_width // 2
        platform_y = player.rect.bottom
        new_platform = Platform(platform_x, platform_y, platform_width, platform_height)
        current_level.platforms.add(new_platform)
        all_sprites.add(new_platform)

        # 카메라 고정 위치 해제 및 타겟 설정
        camera.fixed_position = None
        camera.update_target(player)
    
    else:
        # 보스 레벨이 아닌 경우 카메라의 고정 위치를 해제합니다.
        camera.fixed_position = None
        is_boss_level_active = False



# 초기 게임 상태 설정
reset_game()
checkpoint_position = (900, 200)
enemy_spawn_timer = pygame.time.get_ticks()
heart_spawn_timer = pygame.time.get_ticks()
heart_group = pygame.sprite.Group()
ENEMY_SPAWN_INTERVAL = 5000
ENEMY_SPAWN_RADIUS = 300
running = True
game_over = False





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


def transition_to_boss_level():
    global current_level_index, current_level_data, current_level
    global player, all_sprites, camera, is_boss_level_active
    global star_spawn_timer  # 전역 변수로 선언

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

    # 카메라 고정 위치 설정
    camera.fixed_position = None  # 이 줄을 수정하여 카메라 고정 해제
    camera.target = player        # 카메라가 플레이어를 따라가도록 설정

    # 보스방 관련 변수 초기화
    star_spawn_timer = pygame.time.get_ticks()  # 스타 스폰 타이머 초기화




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
                else:
                    new_enemy = EnemyType2(spawn_x, spawn_y, gravity_manager)
                    current_level.enemies_type2.add(new_enemy)
                all_sprites.add(new_enemy)


        if is_boss_level_active:
            # 스타 스프라이트 주기적으로 생성
            if current_time - star_spawn_timer > STAR_SPAWN_INTERVAL:
                star_spawn_timer = current_time
                # 스타를 보스방 내부 플랫폼에 랜덤하게 생성
                star_x = random.randint(4020 + 30, 4780 - 30)  # 벽 두께와 스타 크기를 고려
                star_y = random.randint(220, 780 - 30)
                new_star = Star(star_x, star_y)
                current_level.stars.add(new_star)
                all_sprites.add(new_star)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # 중력 방향 변경
                if event.key == pygame.K_UP:
                    gravity_manager.set_gravity('up')
                elif event.key == pygame.K_DOWN:
                    gravity_manager.set_gravity('down')
                elif event.key == pygame.K_LEFT:
                    gravity_manager.set_gravity('left')
                elif event.key == pygame.K_RIGHT:
                    gravity_manager.set_gravity('right')

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

        current_time = pygame.time.get_ticks()
        if current_time - heart_spawn_timer > settings.HEART_SPAWN_INTERVAL:
            heart_spawn_timer = current_time
            heart_x = random.randint(100, settings.MAP_WIDTH - 100)
            heart_y = random.randint(100, settings.MAP_HEIGHT - 100)
            new_heart = Heart(heart_x, heart_y)
            heart_group.add(new_heart)
            all_sprites.add(new_heart)

        heart_hits = pygame.sprite.spritecollide(player, heart_group, True)
        if heart_hits:
            player.health = min(player.health + 1, settings.PLAYER_HEALTH)




        # 충돌 처리
        if current_level.flag and pygame.sprite.collide_rect(player, current_level.flag):
            print("Congratulations! You reached the flag!")
            transition_to_boss_level()
            continue

        if current_level.boss:
            current_level.boss.update(player)
            current_level.boss.projectiles.update()

            # 보스의 투사체와 스타의 충돌 처리
            projectile_star_hits = pygame.sprite.groupcollide(
                current_level.boss.projectiles,
                current_level.stars,
                True,  # 투사체는 제거
                False  # 스타는 제거하지 않음
            )

            # 보스와 스타의 충돌 처리
            boss_star_hits = pygame.sprite.spritecollide(
                current_level.boss,
                current_level.stars,
                True  # 스타는 제거
            )
            if boss_star_hits:
                current_level.boss.health -= 30
                current_level.boss.is_stunned = True
                current_level.boss.stun_timer = pygame.time.get_ticks()

            hits = pygame.sprite.spritecollide(
                player,
                current_level.boss.projectiles,
                True
            )
            if hits:
                player.health -= 1
                if player.health <= 0:
                    game_over = True
            if pygame.sprite.collide_rect(player, current_level.boss):
                player.health -= 1
                if player.health <= 0:
                    game_over = True

        enemy_hits = pygame.sprite.spritecollide(player, current_level.enemies, False)
        enemy_type2_hits = pygame.sprite.spritecollide(player, current_level.enemies_type2, False)
        if enemy_hits or enemy_type2_hits:
            player.health -= 1
            if player.health <= 0:
                game_over = True

        trap_hits = pygame.sprite.spritecollide(player, current_level.traps, False)
        if trap_hits:
            player.health -= 1
            if player.health > 0:
                player.respawn()
            else:
                game_over = True

        if player.health <= 0:
            game_over = True

        if player.rect.colliderect(pygame.Rect(checkpoint_position[0], checkpoint_position[1], 50, 50)):
            player.set_checkpoint(checkpoint_position)



        # 카메라 업데이트
        camera.update()

        if not camera.camera_rect.colliderect(player.rect):
            player.health -= 1
            if player.health > 0:
                player.respawn()
            else:
                game_over = True

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
            else:
                new_enemy = EnemyType2(spawn_x, spawn_y, gravity_manager)
                current_level.enemies_type2.add(new_enemy)
            all_sprites.add(new_enemy)


        
        # all_sprites 그리기 전에 스타 스프라이트 업데이트
        current_level.stars.update()

        # 화면 그리기
        screen.fill(settings.BLACK)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        # 보스의 투사체 그리기
        if current_level.boss:
            for projectile in current_level.boss.projectiles:
                screen.blit(projectile.image, camera.apply(projectile))

         # 스타 스프라이트 그리기
        for star in current_level.stars:
            screen.blit(star.image, camera.apply(star))

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
finally:
    pygame.quit()
    sys.exit()
