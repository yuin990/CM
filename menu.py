import pygame
import math


class Menu:
    def __init__(self, screen, font, title_font, screen_width, screen_height, click_sound):
        self.screen = screen
        self.font = font
        self.title_font = title_font
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.click_sound = click_sound

        self.start_button_rect = pygame.Rect(0, 0, 200, 50)
        self.start_button_rect.center = (self.screen_width // 2, self.screen_height * 0.55)

        self.title_label = self.title_font.render("GAME START", True, (61, 218, 215))
        self.title_label_rect = self.title_label.get_rect(center=(self.screen_width // 2, self.screen_height * 0.35))

        self.alpha = 255.0
        self.alpha_speed = -2.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button_rect.collidepoint(event.pos):
                if self.click_sound:
                    self.click_sound.play()
                return "playing"
        return "menu"

    def draw(self):
        self.screen.fill((255, 255, 255))

        self.alpha += self.alpha_speed
        if self.alpha <= 128 or self.alpha >= 255:
            self.alpha_speed *= -1
            self.alpha = max(128, min(self.alpha, 255))

        self.title_label.set_alpha(int(self.alpha))
        self.screen.blit(self.title_label, self.title_label_rect)

        pygame.draw.rect(self.screen, (61, 218, 215), self.start_button_rect, border_radius=10)
        start_text = self.font.render("시작하기", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(start_text, start_text_rect)