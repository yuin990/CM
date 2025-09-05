import pygame
import math
from player import Player
from level import Level
from menu import Menu

pygame.init()
pygame.mixer.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("코드마스터")

clock = pygame.time.Clock()

try:
    font = pygame.font.Font('assets/fonts/Galmuri9.ttf', 24)
    title_font = pygame.font.Font('assets/fonts/Galmuri9.ttf', 48)
    puzzle_font = pygame.font.Font('assets/fonts/Galmuri9.ttf', 48)
except pygame.error:
    font = pygame.font.SysFont('Arial', 24)
    title_font = pygame.font.SysFont('Arial', 48)
    puzzle_font = pygame.font.SysFont('Arial', 48)
    print("Galmuri9.ttf 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")

game_state = "menu"

messages = [
    "안녕하세요! 방에 오신 것을 환영합니다.",
    "퍼즐을 풀며 나아가보세요.",
    "옆에 있는 문을 열면 시작됩니다."
]
current_message_index = -1
message_timer = 0
message_duration = 3.0
tutorial_text = ""
tutorial_text_surface = None
tutorial_text_rect = None
puzzle_text = "산소를 만들자!"
puzzle_text_surface = None
puzzle_text_rect = None

all_sprites = pygame.sprite.LayeredUpdates()
level = None
player = None
click_sound = None

try:
    click_sound = pygame.mixer.Sound('assets/audio/click.wav')
    pygame.mixer.music.load('assets/audio/back.mp3')
except pygame.error:
    print("사운드 파일을 찾을 수 없습니다. 소리 재생을 건너뜁니다.")

menu_screen = Menu(screen, font, title_font, screen_width, screen_height, click_sound)
held_object = None


def start_game():
    global game_state, level, player, all_sprites, tutorial_text_surface, tutorial_text_rect, puzzle_text_surface, puzzle_text_rect, held_object

    game_state = "playing"
    all_sprites.empty()

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.music.play(-1)

    level = Level(all_sprites)

    player_start_pos_x = level.map_offset_x + level.tile_size * 2.5
    player_start_pos_y = level.map_offset_y + level.tile_size * 1.5
    player = Player((player_start_pos_x, player_start_pos_y), 'assets/images/Character.png',
                    'assets/data/Character.json', 1, all_sprites)

    tutorial_text = "wasd/화살표 키로 조작"
    tutorial_text_surface = font.render(tutorial_text, True, (255, 255, 255))
    tutorial_text_rect = tutorial_text_surface.get_rect(center=(screen_width // 2, screen_height - 30))

    puzzle_text_surface = puzzle_font.render(puzzle_text, True, (0, 0, 0))
    # 게임 시작 시 held_object 초기화
    held_object = None


def end_game():
    global game_state, level, player, all_sprites, tutorial_text_surface, tutorial_text_rect, held_object
    game_state = "menu"
    level = None
    player = None
    all_sprites.empty()
    tutorial_text_surface = None
    tutorial_text_rect = None
    held_object = None

    pygame.mixer.music.stop()


running = True
last_time = pygame.time.get_ticks()

while running:
    dt = (pygame.time.get_ticks() - last_time) / 1000.0
    last_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            new_state = menu_screen.handle_event(event)
            if new_state == "playing":
                start_game()

        elif game_state == "playing":
            exit_button_rect = pygame.Rect(screen_width - 100, 20, 80, 30)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    end_game()
                    if click_sound:
                        click_sound.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if click_sound:
                        click_sound.play()
                    if level.lightbulb is not None and player.rect.colliderect(level.lightbulb.rect.inflate(32, 32)):
                        current_message_index = (current_message_index + 1)
                        if current_message_index >= len(messages):
                            current_message_index = 0

                        if current_message_index == len(messages) - 1:
                            message_timer = 2.0
                        else:
                            message_timer = message_duration

                    elif level.door_sprite is not None and player.rect.colliderect(
                            level.door_sprite.rect.inflate(40, 40)):
                        level.current_room_index = (level.current_room_index + 1) % len(level.room_names)
                        next_room_name = level.room_names[level.current_room_index]

                        all_sprites.empty()
                        level.load_room(next_room_name, all_sprites, player)
                        all_sprites.add(player, layer=1)
                        # 방이동 시 held_object 초기화
                        held_object = None

                        if next_room_name == "room_2":
                            player.pos = pygame.math.Vector2(level.map_offset_x + level.tile_size * 1.5,
                                                             level.map_offset_y + (
                                                                     len(level.room_map) // 2) * level.tile_size + level.tile_size * 0.5)
                        else:
                            player.pos = pygame.math.Vector2(level.map_offset_x + level.tile_size * 2.5,
                                                             level.map_offset_y + level.tile_size * 1.5)

                    elif level.nucleus is not None and player.rect.colliderect(level.nucleus.rect.inflate(32, 32)):
                        print("원자 퍼즐과 상호작용합니다.")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if held_object:
                        held_object.is_held = False
                        held_object = None
                    elif level.objects_list:
                        for obj in level.objects_list:
                            if player.rect.colliderect(obj.rect.inflate(32, 32)):
                                obj.is_held = True
                                held_object = obj
                                all_sprites.remove(obj)
                                all_sprites.add(obj, layer=2)
                                break

    if game_state == "menu":
        menu_screen.draw()

    elif game_state == "playing":
        if level.door_sprite is not None and level.e_button is not None and player.rect.colliderect(
                level.door_sprite.rect.inflate(40, 40)):
            level.e_button.rect.center = (level.door_sprite.rect.centerx, level.door_sprite.rect.top - 20)
        elif level.lightbulb is not None and level.e_button is not None and player.rect.colliderect(
                level.lightbulb.rect.inflate(40, 40)):
            level.e_button.rect.center = (level.lightbulb.rect.centerx, level.lightbulb.rect.top - 20)
        elif level.nucleus is not None and level.e_button is not None and player.rect.colliderect(
                level.nucleus.rect.inflate(32, 32)):
            level.e_button.rect.center = (level.nucleus.rect.centerx, level.nucleus.rect.top - 20)
        elif level.e_button is not None:
            level.e_button.rect.center = (-100, -100)

        player.update(dt, level.wall_sprites)
        if held_object:
            held_object.update(player.rect)

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        if level.room_names[level.current_room_index] == "room_1":
            if tutorial_text_surface is not None:
                tutorial_text_surface.set_alpha(int(128 + 127 * math.sin(pygame.time.get_ticks() / 500)))
                screen.blit(tutorial_text_surface, tutorial_text_rect)

        if level.lightbulb is not None and current_message_index != -1 and message_timer > 0:
            message_timer -= dt
            text_surface = font.render(messages[current_message_index], True, (0, 0, 0))
            text_rect = text_surface.get_rect(
                midbottom=(level.lightbulb.rect.midtop[0], level.lightbulb.rect.midtop[1] - 50))
            screen.blit(text_surface, text_rect)

        if level.room_names[level.current_room_index] == "room_2" and puzzle_text_surface is not None:
            puzzle_text_rect = puzzle_text_surface.get_rect(
                center=(screen_width // 2, screen_height // 2 - 200))
            screen.blit(puzzle_text_surface, puzzle_text_rect)

        exit_button_rect = pygame.Rect(screen_width - 100, 20, 80, 30)
        pygame.draw.rect(screen, (200, 50, 50), exit_button_rect, border_radius=5)
        exit_text = font.render("나가기", True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_text, exit_text_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()