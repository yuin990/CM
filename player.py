import pygame
import json
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, spritesheet_path, json_path, layer, *groups):
        super().__init__(*groups)
        self._layer = layer

        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        with open(json_path, 'r', encoding='utf-8') as f:
            self.anim_data = json.load(f)

        self.animations = {}
        self.load_animations()
        self.scale_factor = 2.0
        self.scaled_animations = {}
        self._create_scaled_animations()

        self.state = 'idle_front'
        self.current_frame = 0
        self.animation_timer = 0
        self.facing_right = True

        self.image = self.scaled_animations[self.state][self.current_frame][0]
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 200

    def _create_scaled_animations(self):
        for state, frames in self.animations.items():
            self.scaled_animations[state] = []
            for base_image, duration in frames:
                original_size = base_image.get_size()
                scaled_size = (int(original_size[0] * self.scale_factor), int(original_size[1] * self.scale_factor))
                scaled_image = pygame.transform.scale(base_image, scaled_size)
                self.scaled_animations[state].append((scaled_image, duration))

    def load_animations(self):
        self.animations = {
            'idle_front': [],
            'walk_front': [],
            'walk_right': [],
            'walk_left': []
        }

        frame_data = self.anim_data['frames']
        for i in range(len(frame_data)):
            frame_name = f"Character {i}.png"
            if frame_name in frame_data:
                frame = frame_data[frame_name]
                x, y, w, h = frame['frame']['x'], frame['frame']['y'], frame['frame']['w'], frame['frame']['h']
                duration = 500
                sub_image = self.spritesheet.subsurface(pygame.Rect(x, y, w, h))

                if i in [0, 1]:
                    self.animations['idle_front'].append((sub_image, duration))
                elif i in [4, 5]:
                    self.animations['walk_front'].append((sub_image, duration))
                elif i in [6, 7]:
                    self.animations['walk_left'].append((sub_image, duration))

        for image, duration in self.animations['walk_left']:
            flipped_image = pygame.transform.flip(image, True, False)
            self.animations['walk_right'].append((flipped_image, duration))

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.current_frame = 0
            self.animation_timer = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        self.velocity.y = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity.x = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity.y = 1

        if self.velocity.length() > 0:
            self.velocity.normalize_ip()

    def update_state(self):
        if self.velocity.length() > 0:
            if self.velocity.y > 0:
                self.set_state('walk_front')
            elif self.velocity.y < 0:
                self.set_state('walk_front')
            elif self.velocity.x > 0:
                self.set_state('walk_right')
            elif self.velocity.x < 0:
                self.set_state('walk_left')
        else:
            self.set_state('idle_front')

    def animate(self, dt):
        current_animation = self.scaled_animations[self.state]
        self.animation_timer += dt * 1000

        if len(current_animation) > 0 and self.animation_timer >= current_animation[self.current_frame][1]:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(current_animation)

        if len(current_animation) > 0:
            self.image = current_animation[self.current_frame][0]

        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

    def update(self, dt, walls):
        self.handle_input()
        self.update_state()
        self.animate(dt)

        self.pos.x += self.velocity.x * self.speed * dt
        self.rect.centerx = round(self.pos.x)
        self.collide_walls(walls, 'x')
        self.pos.x = self.rect.centerx

        self.pos.y += self.velocity.y * self.speed * dt
        self.rect.centery = round(self.pos.y)
        self.collide_walls(walls, 'y')
        self.pos.y = self.rect.centery

    def collide_walls(self, walls, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, walls, False)
            for wall in hits:
                if self.velocity.x > 0:
                    self.rect.right = wall.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = wall.rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, walls, False)
            for wall in hits:
                if self.velocity.y > 0:
                    self.rect.bottom = wall.rect.top
                elif self.velocity.y < 0:
                    self.rect.top = wall.rect.bottom