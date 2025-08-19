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
        self.tile_size = 32
        self.wall_color = (100, 100, 100)
        self.wall_sprites = pygame.sprite.Group()
        self.create_map_tiles(all_sprites)

    def create_map_tiles(self, all_sprites):
        for row_index, row in enumerate(self.room_map):
            for col_index, tile in enumerate(row):
                if tile == 1:
                    wall_tile = pygame.sprite.Sprite()
                    wall_tile.image = pygame.Surface((self.tile_size, self.tile_size))
                    wall_tile.image.fill(self.wall_color)
                    wall_tile.rect = wall_tile.image.get_rect(
                        topleft=(col_index * self.tile_size, row_index * self.tile_size))

                    all_sprites.add(wall_tile, layer=0)
                    self.wall_sprites.add(wall_tile)