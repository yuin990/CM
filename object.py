# object.py
import pygame


class Object(pygame.sprite.Sprite):
    # image_path 대신 image 객체를 인자로 받습니다.
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_held = False

    def update(self, player_rect):
        if self.is_held:
            self.rect.centerx = player_rect.centerx
            self.rect.bottom = player_rect.top - 6