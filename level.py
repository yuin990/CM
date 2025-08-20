import pygame
import json
import os


class Level:
    def __init__(self, all_sprites):
        self.tile_size = 64
        self.screen_width = 800
        self.screen_height = 600

        with open('assets/data/rooms.json', 'r', encoding='utf-8') as f:
            self.rooms = json.load(f)

        self.room_names = list(self.rooms.keys())
        self.current_room_index = 0

        self.map_width = len(self.rooms[self.room_names[0]][0]) * self.tile_size
        self.map_height = len(self.rooms[self.room_names[0]]) * self.tile_size
        self.map_offset_x = (self.screen_width - self.map_width) // 2
        self.map_offset_y = (self.screen_height - self.map_height) // 2

        self.door_sprite = None
        self.e_button = None
        self.lightbulb = None
        self.wall_sprites = pygame.sprite.Group()
        self.load_room(self.room_names[self.current_room_index], all_sprites, None)

    def load_room(self, room_name, all_sprites, player):
        # 기존 맵 요소만 제거 (플레이어는 유지)
        for sprite in list(all_sprites):
            if sprite != player:
                sprite.kill()

        self.wall_sprites.empty()
        self.door_sprite = None
        self.e_button = None
        self.lightbulb = None

        self.room_map = self.rooms[room_name]
        self.create_map_tiles(all_sprites)

        if room_name == "room_1":
            self.create_door(all_sprites)
            self.create_lightbulb(all_sprites)

    def create_map_tiles(self, all_sprites):
        for row_index, row in enumerate(self.room_map):
            for col_index, tile in enumerate(row):
                if tile == 1:
                    wall_tile = pygame.sprite.Sprite()
                    wall_tile.image = pygame.Surface((self.tile_size, self.tile_size))
                    wall_tile.image.fill((200, 200, 250))
                    wall_tile.rect = wall_tile.image.get_rect(topleft=(col_index * self.tile_size + self.map_offset_x,
                                                                       row_index * self.tile_size + self.map_offset_y))

                    all_sprites.add(wall_tile, layer=0)
                    self.wall_sprites.add(wall_tile)
                else:
                    floor_tile = pygame.sprite.Sprite()
                    floor_tile.image = pygame.Surface((self.tile_size, self.tile_size))
                    floor_tile.image.fill((230, 230, 255))
                    floor_tile.rect = floor_tile.image.get_rect(topleft=(col_index * self.tile_size + self.map_offset_x,
                                                                         row_index * self.tile_size + self.map_offset_y))

                    all_sprites.add(floor_tile, layer=0)

    def create_door(self, all_sprites):
        self.door_sprite = pygame.sprite.Sprite()
        door_width = 16
        self.door_sprite.image = pygame.Surface((door_width, self.tile_size))
        self.door_sprite.image.fill((139, 69, 19))

        center_row = len(self.room_map) // 2
        door_x = (len(self.room_map[0]) - 1) * self.tile_size + self.map_offset_x
        door_y = center_row * self.tile_size + self.map_offset_y

        self.door_sprite.rect = self.door_sprite.image.get_rect(topleft=(door_x - door_width, door_y))

        all_sprites.add(self.door_sprite, layer=1)
        self.wall_sprites.add(self.door_sprite)

        try:
            e_button_image = pygame.image.load('assets/images/e_button.png').convert_alpha()
        except pygame.error:
            e_button_image = pygame.Surface((64, 64))
            e_button_image.fill((255, 255, 0))
            print("e_button.png 파일을 찾을 수 없습니다. 임시 스프라이트를 사용합니다.")

        self.e_button = pygame.sprite.Sprite()
        self.e_button.image = e_button_image
        self.e_button.rect = self.e_button.image.get_rect(center=(-100, -100))
        all_sprites.add(self.e_button, layer=2)

    def create_lightbulb(self, all_sprites):
        try:
            lightbulb_image = pygame.image.load('assets/images/lightbulb.png').convert_alpha()
            lightbulb_image = pygame.transform.scale(lightbulb_image, (64, 64))
        except pygame.error:
            lightbulb_image = pygame.Surface((64, 64))
            lightbulb_image.fill((255, 255, 0))
            print("lightbulb.png 파일을 찾을 수 없습니다. 임시 스프라이트를 사용합니다.")

        self.lightbulb = pygame.sprite.Sprite()
        self.lightbulb.image = lightbulb_image

        center_x = self.map_offset_x + self.map_width // 2
        center_y = self.map_offset_y + self.map_height // 2

        self.lightbulb.rect = self.lightbulb.image.get_rect(center=(center_x, center_y))

        all_sprites.add(self.lightbulb, layer=1)
        self.wall_sprites.add(self.lightbulb)