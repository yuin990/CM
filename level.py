import pygame as pg
import json
import os
from puzzle import AtomPuzzle

ATOMS = {
    "He": {"name": "헬륨", "valence_e": 2, "protons": 2},
    "Ne": {"name": "네온", "valence_e": 8, "protons": 10},
    "O": {"name": "산소", "valence_e": 6, "protons": 8}
}

class Level:
    def __init__(self, all_sprites, screen):
        self.screen = screen
        self.all_sprites = all_sprites
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
        self.electrons = pg.sprite.Group()
        self.wall_sprites = pg.sprite.Group()
        self.puzzle = None

        self.objects_list = []

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
        self.objects_list = []

        self.room_map = self.rooms[room_name]
        self.create_map_tiles(all_sprites)

        if room_name == "room_1":
            self.create_lightbulb(all_sprites)
            self.create_door(all_sprites)

        elif room_name == "room_2":
            self.run_atom_puzzle()
            if self.is_puzzle_solved:
                self.create_door(all_sprites)

    def run_atom_puzzle(self):
        atom_puzzle = AtomPuzzle(
            pg.display.get_surface(),
            ATOMS["Ne"],
            self.all_sprites,
            self.map_offset_x,
            self.map_offset_y,
            self.map_width,
            self.map_height
        )
        result = atom_puzzle.run_puzzle()

        if result == "win":
            self.is_puzzle_solved = True
        elif result == "lose":
            self.is_puzzle_solved = False
            self.run_atom_puzzle()

    def create_map_tiles(self, all_sprites):
        for row_index, row in enumerate(self.room_map):
            for col_index, tile in enumerate(row):
                x = col_index * self.tile_size + self.map_offset_x
                y = row_index * self.tile_size + self.map_offset_y

                if tile == 1:
                    wall_tile = pg.sprite.Sprite()
                    wall_tile.image = pg.Surface((self.tile_size, self.tile_size))
                    wall_tile.image.fill((200, 200, 250))
                    wall_tile.rect = wall_tile.image.get_rect(topleft=(x, y))

                    all_sprites.add(wall_tile, layer=0)
                    self.wall_sprites.add(wall_tile)
                else:
                    floor_tile = pg.sprite.Sprite()
                    floor_tile.image = pg.Surface((self.tile_size, self.tile_size))
                    floor_tile.image.fill((230, 230, 255))
                    floor_tile.rect = floor_tile.image.get_rect(topleft=(x, y))

                    all_sprites.add(floor_tile, layer=0)

    def create_door(self, all_sprites):
        self.door_sprite = pg.sprite.Sprite()
        door_width = 16
        self.door_sprite.image = pg.Surface((door_width, self.tile_size))
        self.door_sprite.image.fill((139, 69, 19))

        center_row = len(self.room_map) // 2
        door_x = (len(self.room_map[0]) - 1) * self.tile_size + self.map_offset_x
        door_y = center_row * self.tile_size + self.map_offset_y
        self.door_sprite.rect = self.door_sprite.image.get_rect(topleft=(door_x - door_width, door_y))

        all_sprites.add(self.door_sprite, layer=1)
        self.wall_sprites.add(self.door_sprite)

        try:
            e_button_image = pg.image.load('assets/images/e_button.png').convert_alpha()
        except pg.error:
            e_button_image = pg.Surface((64, 64))
            e_button_image.fill((255, 255, 0))
            print("e_button.png 파일을 찾을 수 없습니다. 임시 스프라이트를 사용합니다.")

        self.e_button = pg.sprite.Sprite()
        self.e_button.image = e_button_image
        self.e_button.rect = e_button_image.get_rect(center=(-100, -100))
        all_sprites.add(self.e_button, layer=2)

    def create_lightbulb(self, all_sprites):
        try:
            lightbulb_image = pg.image.load('assets/images/lightbulb.png').convert_alpha()
            lightbulb_image = pg.transform.scale(lightbulb_image, (64, 64))
        except pg.error:
            lightbulb_image = pg.Surface((64, 64))
            lightbulb_image.fill((255, 255, 0))
            print("lightbulb.png 파일을 찾을 수 없습니다. 임시 스프라이트를 사용합니다.")

        self.lightbulb = pg.sprite.Sprite()
        self.lightbulb.image = lightbulb_image

        center_x = self.map_offset_x + self.map_width // 2
        center_y = self.map_offset_y + self.map_height // 2

        self.lightbulb.rect = self.lightbulb.image.get_rect(center=(center_x, center_y))

        all_sprites.add(self.lightbulb, layer=1)
        self.wall_sprites.add(self.lightbulb)

    def create_atom_puzzle(self, all_sprites):
        try:
            orbital_image = pg.image.load('assets/images/puzzle1.png').convert_alpha()
            orbital_image = pg.transform.scale(orbital_image, (300, 300))
        except pg.error:
            orbital_image = pg.Surface((300, 300))
            orbital_image.fill((255, 255, 0))
            print("puzzle1.png 파일을 찾을 수 없습니다. 임시 스프라이트를 사용합니다.")

        self.nucleus = pg.sprite.Sprite()
        self.nucleus.image = orbital_image

        center_x = self.map_offset_x + self.map_width // 2
        center_y = self.map_offset_y + self.map_height // 2

        self.nucleus.rect = self.nucleus.image.get_rect(center=(center_x, center_y))

        all_sprites.add(self.nucleus, layer=1)

        try:
            electron_image = pg.image.load('assets/images/puzzle2.png').convert_alpha()
            electron_image = pg.transform.scale(electron_image, (64, 64))
        except pg.error:
            electron_image = pg.Surface((64, 64))
            electron_image.fill((0, 0, 255))
            print("puzzle2.png 파일을 찾을 수 없습니다. 임시 스프라이트를 사용합니다.")

        electron_positions = [
            (center_x - 100, center_y - 100), (center_x + 100, center_y - 100),
            (center_x - 100, center_y), (center_x + 100, center_y),
            (center_x - 100, center_y + 100), (center_x + 100, center_y + 100),
            (center_x, center_y - 100), (center_x, center_y + 100)
        ]

        for pos in electron_positions:
            electron = pg.sprite.Sprite()
            electron.image = electron_image
            electron.rect = electron.image.get_rect(center=pos)
            self.electrons.add(electron)
            all_sprites.add(electron, layer=1)