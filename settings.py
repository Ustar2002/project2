#settings.py

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 맵 크기 설정
MAP_WIDTH = 5000
MAP_HEIGHT = 1200

# 초기 플랫폼 위치
INITIAL_PLATFORM_POSITION = (300, 500, 200, 20)

# 색상 정의
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# 게임 설정
FPS = 60
GRAVITY_DURATION = 5
GRAVITY_RECHARGE_TIME = 3

# 플레이어 설정
PLAYER_SPEED = 4
PLAYER_JUMP_STRENGTH = 15
PLAYER_HEALTH = 10
PLAYER_INVINCIBILITY_DURATION = 2000  # 플레이어 무적 지속 시간 (밀리초)

# 적 설정
ENEMY_SPEED = 2
ENEMY_HEALTH = 3

# 보스 설정
BOSS_HEALTH = 150
BOSS_SPEED = 3

# 중력 컨트롤량 설정
MAX_GRAVITY_CONTROL = 5
GRAVITY_RECHARGE_DELAY = 3
GRAVITY_RECHARGE_RATE = 1

# 하트 생성 간격 (밀리초)
HEART_SPAWN_INTERVAL = 10000

# 화면 위쪽 상한선
UPPER_LIMIT = -200

# 카메라 설정
CAMERA_SCROLL_SPEED = 1

# 보스 스텀프 관련 설정
BOSS_STUN_DURATION = 2000        # 보스가 경직 상태로 있는 시간 (밀리초)
BOSS_STOMP_DAMAGE = 10            # 보스를 밟았을 때 감소하는 체력
BLOOD_EFFECT_DURATION = 500       # 피 효과 지속 시간 (밀리초)

# 보스 체력 바 설정
BOSS_HEALTH_BAR_WIDTH = 200
BOSS_HEALTH_BAR_HEIGHT = 20
BOSS_HEALTH_BAR_BG_COLOR = (255, 0, 0)      # 배경 바 색상 (빨간색)
BOSS_HEALTH_BAR_FG_COLOR = (0, 255, 0)      # 채워진 바 색상 (녹색)
BOSS_HEALTH_TEXT_COLOR = (255, 255, 255)    # 텍스트 색상 (흰색)
BOSS_HEALTH_BAR_MARGIN = 10                 # 화면 가장자리와의 거리

# 보스 종료 애니메이션 관련 설정
BOSS_FINISH_DURATION = 2000    # 보스 종료 애니메이션 지속 시간 (밀리초)

# 게임 일시정지 플래그
PAUSED = False                    # 모든 스프라이트의 움직임을 정지시키는 플래그

# 스타 설정
STAR_SPEED = 5  # 스타의 이동 속도 추가
