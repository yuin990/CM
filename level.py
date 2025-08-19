import pygame


class Level:
    def __init__(self, all_sprites):
        self.room_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.tile_size = 64
        self.map_width = len(self.room_map[0]) * self.tile_size
        self.map_height = len(self.room_map) * self.tile_size
        self.screen_width = 800
        self.screen_height = 600

        self.map_offset_x = (self.screen_width - self.map_width) // 2
        self.map_offset_y = (self.screen_height - self.map_height) // 2

        self.wall_sprites = pygame.sprite.Group()
        self.create_map_tiles(all_sprites)

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