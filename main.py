import pygame
from player import Player
from level import Level

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("코드마스터")

# 색상 정의
BLACK = (0, 0, 0)

# 게임 클럭 설정
clock = pygame.time.Clock()

# 레이어드 업데이트 그룹 생성
all_sprites = pygame.sprite.LayeredUpdates()

# 플레이어와 레벨 객체 생성
player = Player((400, 300), 'assets/images/Character.png', 'assets/data/Character.json', 1, all_sprites)
level = Level(all_sprites)

# 게임 루프
running = True
last_time = pygame.time.get_ticks()

while running:
    # dt (델타 타임) 계산
    dt = (pygame.time.get_ticks() - last_time) / 1000.0
    last_time = pygame.time.get_ticks()

    # 1. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. 모든 스프라이트 업데이트
    all_sprites.update(dt)

    # 3. 화면 그리기
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # 4. 화면 업데이트
    pygame.display.flip()

    # 초당 프레임 수 (FPS) 설정
    clock.tick(60)

# Pygame 종료
pygame.quit()