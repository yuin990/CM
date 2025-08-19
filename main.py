import pygame
from player import Player
from level import Level

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("코드마스터")

clock = pygame.time.Clock()

all_sprites = pygame.sprite.LayeredUpdates()

level = Level(all_sprites)
player_start_pos_x = level.map_offset_x + level.tile_size * 1.5
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

    all_sprites.update(dt, level.wall_sprites)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()