import pygame
from player import Player
from level import Level

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("코드마스터")

clock = pygame.time.Clock()

try:
    font = pygame.font.Font('assets/fonts/Galmuri9.ttf', 24)
except pygame.error:
    font = pygame.font.SysFont('Arial', 24)
    print("Galmuri9.ttf 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")

messages = [
    "안녕하세요! 방에 오신 것을 환영합니다.",
    "퍼즐을 풀며 나아가보세요.",
    "옆에 있는 문을 열면 시작됩니다."
]
current_message_index = -1
message_timer = 0
message_duration = 3.0

all_sprites = pygame.sprite.LayeredUpdates()

level = Level(all_sprites)
player_start_pos_x = level.map_offset_x + level.tile_size * 2.5
player_start_pos_y = level.map_offset_y + level.tile_size * 1.5
player = Player((player_start_pos_x, player_start_pos_y), 'assets/images/Character.png', 'assets/data/Character.json',
                1, all_sprites)

running = True
last_time = pygame.time.get_ticks()

while running:
    dt = (pygame.time.get_ticks() - last_time) / 1000.0
    last_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if level.lightbulb is not None and player.rect.colliderect(level.lightbulb.rect.inflate(32, 32)):
                    current_message_index = (current_message_index + 1)
                    if current_message_index >= len(messages):
                        current_message_index = 0

                    if current_message_index == len(messages) - 1:
                        message_timer = 2.0
                    else:
                        message_timer = message_duration

                elif level.door_sprite is not None and player.rect.colliderect(level.door_sprite.rect.inflate(40, 40)):
                    level.current_room_index = (level.current_room_index + 1) % len(level.room_names)
                    next_room_name = level.room_names[level.current_room_index]
                    level.load_room(next_room_name, all_sprites, player)

                    player.pos = pygame.math.Vector2(level.map_offset_x + level.tile_size * 1.5,
                                                     level.map_offset_y + level.tile_size * 1.5)

    e_button_visible = False

    if level.door_sprite is not None and player.rect.colliderect(level.door_sprite.rect.inflate(40, 40)):
        e_button_visible = True
        level.e_button.rect.center = (level.door_sprite.rect.centerx, level.door_sprite.rect.top - 20)

    if level.lightbulb is not None and player.rect.colliderect(level.lightbulb.rect.inflate(40, 40)):
        e_button_visible = True
        level.e_button.rect.center = (level.lightbulb.rect.centerx, level.lightbulb.rect.top - 20)

    if not e_button_visible and level.e_button is not None:
        level.e_button.rect.center = (-100, -100)

    all_sprites.update(dt, level.wall_sprites)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    if level.lightbulb is not None and current_message_index != -1 and message_timer > 0:
        message_timer -= dt
        text_surface = font.render(messages[current_message_index], True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            midbottom=(level.lightbulb.rect.midtop[0], level.lightbulb.rect.midtop[1] - 50))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()