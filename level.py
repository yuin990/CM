# level.py
import pygame
import json
import os
from puzzle import AtomPuzzle
from object import Object


class Level:
    def __init__(self, all_sprites):
        self.tile_size = 64
        self.screen_width = 800
        self.screen_height = 600

        with open('assets/data/rooms.json', 'r', encoding='utf-8') as f:
            self.rooms = json.load(f)

        self.room_names = list(self.rooms.keys())
        self.current_room_index = 0
        self.is_puzzle_solved = False

        self.map_width = len(self.rooms[self.room_names[0]][0]) * self.tile_size
        self.map_height = len(self.rooms[self.room_names[0]]) * self.tile_size
        self.map_offset_x = (self.screen_width - self.map_width) // 2
        self.map_offset_y = (self.screen_height - self.map_height) // 2

        self.door_sprite = None
        self.e_button = None
        self.lightbulb = None
        self.nucleus = None
        self.electrons = pygame.sprite.Group()
        self.wall_sprites = pygame.sprite.Group()
        self.puzzle = AtomPuzzle()
        self.all_sprites = all_sprites
        self.objects_list = pygame.sprite.Group()
        self.held_object = None
        self.load_room(self.room_names[self.current_room_index], all_sprites, None)

    def load_room(self, room_name, all_sprites, player):
        for sprite in list(all_sprites):
            if sprite != player:
                sprite.kill()

        self.wall_sprites.empty()
        self.door_sprite = None
        self.e_button = None
        self.lightbulb = None
        self.nucleus = None
        self.electrons.empty()
        self.objects_list.empty()

        self.room_map = self.rooms[room_name]
        self.create_map_tiles(all_sprites)
        self.create_e_button(all_sprites)

        if room_name == "room_1":
            self.create_door(all_sprites)
            self.create_lightbulb(all_sprites)

        elif room_name == "room_2":
            self.create_single_electron(all_sprites)
            if self.is_puzzle_solved:
                self.create_door(all_sprites)

    def create_single_electron(self, all_sprites):
        try:
            electron_image = pygame.image.load('assets/images/puzzle2.png').convert_alpha()
            # 이미지를 300x300으로 키웁니다.
            electron_image = pygame.transform.scale(electron_image, (200, 200))
        except pygame.error:
            electron_image = pygame.Surface((64, 64))
            electron_image.fill((0, 0, 255))
            print("puzzle2.png 파일을 찾을 수 없습니다. 임시 스프라이트를 사용합니다.")

        center_x = self.map_offset_x + self.map_width // 2
        center_y = self.map_offset_y + self.map_height // 2

        # 키운 이미지 자체를 전달합니다.
        electron = self.create_object_with_image(center_x, center_y, electron_image)
        self.electrons.add(electron)
        self.objects_list.add(electron)

    def create_object_with_image(self, x, y, image):
        new_object = Object(x, y, image)
        self.all_sprites.add(new_object, layer=1)
        return new_object

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

    def create_e_button(self, all_sprites):
        try:
            e_button_image = pygame.image.load('assets/images/e_button.png').convert_alpha()
        except pygame.error:
            e_button_image = pygame.Surface((64, 64))
            e_button_image.fill((255, 255, 0))
            print("e_button.png 파일을 찾을 수 없습니다. 임시 스프라이트를 사용합니다.")

        self.e_button = pygame.sprite.Sprite()
        self.e_button.image = e_button_image
        self.e_button.rect = e_button_image.get_rect(center=(-100, -100))
        all_sprites.add(self.e_button, layer=2)

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

    def create_atom_puzzle(self, all_sprites):
        try:
            orbital_image = pygame.image.load('assets/images/puzzle1.png').convert_alpha()
            orbital_image = pygame.transform.scale(orbital_image, (200, 200))
        except pygame.error:
            orbital_image = pygame.Surface((300, 300))
            orbital_image.fill((255, 255, 0))
            print("puzzle1.png 파일을 찾을 수 없습니다. 임시 스프라이트를 사용합니다.")

        self.nucleus = pygame.sprite.Sprite()
        self.nucleus.image = orbital_image

        center_x = self.map_offset_x + self.map_width // 2
        center_y = self.map_offset_y + self.map_height // 2

        self.nucleus.rect = self.nucleus.image.get_rect(center=(center_x, center_y))

        all_sprites.add(self.nucleus, layer=1)

        try:
            electron_image = pygame.image.load('assets/images/puzzle2.png').convert_alpha()
            electron_image = pygame.transform.scale(electron_image, (170, 170))
        except pygame.error:
            electron_image = pygame.Surface((64, 64))
            electron_image.fill((0, 0, 255))
            print("puzzle2.png 파일을 찾을 수 없습니다. 임시 스프라이트를 사용합니다.")

        electron_positions = [
            (center_x - 200, center_y - 200), (center_x + 200, center_y - 200),
            (center_x - 200, center_y), (center_x + 200, center_y),
            (center_x - 200, center_y + 200), (center_x + 200, center_y + 200),
            (center_x, center_y - 200), (center_x, center_y + 200)
        ]

        for pos in electron_positions:
            electron = pygame.sprite.Sprite()
            electron.image = electron_image
            electron.rect = electron.image.get_rect(center=pos)
            self.electrons.add(electron)
            all_sprites.add(electron, layer=1)