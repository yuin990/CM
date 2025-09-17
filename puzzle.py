import pygame as pg
import sys
import random


class AtomPuzzle:
    def __init__(self, screen, atom_data, sprites_group, map_offset_x, map_offset_y, map_width, map_height):
        self.screen = screen
        self.atom_data = atom_data
        self.sprites_group = sprites_group
        self.W, self.H = self.screen.get_size()

        self.map_offset_x = map_offset_x
        self.map_offset_y = map_offset_y
        self.map_width = map_width
        self.map_height = map_height

        self.font = self.get_font(26)
        self.label_font = self.get_font(30)
        self.result_font = self.get_font(40)
        self.n_pos, self.n_r, self.s_r = (self.W // 2, self.H // 2), 50, 200
        self.goal_e = self.atom_data["valence_e"]
        self.held_e, self.game_over, self.win = None, False, False

        self.electrons = [
            self.E(
                random.randint(self.map_offset_x + 10, self.map_offset_x + self.map_width - 10),
                random.randint(self.map_offset_y + 10, self.map_offset_y + self.map_height - 10)
            ) for _ in range(self.atom_data["protons"])
        ]

    def get_font(self, size):
        try:
            return pg.font.Font(
                pg.font.match_font('malgungothic') or pg.font.match_font('AppleGothic') or pg.font.match_font(
                    'NanumGothic'), size)
        except:
            return pg.font.Font(None, size)

    class E:
        def __init__(self, x, y):
            self.pos, self.r, self.color = [x, y], 15, (0, 100, 255)

        def draw(self, screen, label_font):
            pg.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.r)
            txt = label_font.render("-", 1, (0, 0, 0))
            screen.blit(txt, txt.get_rect(center=self.pos))

        def get_rect(self):
            return pg.Rect(self.pos[0] - self.r, self.pos[1] - self.r, self.r * 2, self.r * 2)

    def run_puzzle(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN and not self.game_over:
                    if pg.Rect(self.W - 150, self.H // 2, 120, 50).collidepoint(event.pos):
                        count = sum(1 for e in self.electrons if
                                    self.s_r - 20 < ((e.pos[0] - self.n_pos[0]) ** 2 + (
                                                e.pos[1] - self.n_pos[1]) ** 2) ** 0.5 < self.s_r + 20)
                        self.game_over, self.win = True, (count == self.atom_data["valence_e"])
                    else:
                        for e in self.electrons:
                            if e.get_rect().collidepoint(event.pos):
                                self.held_e = e
                                break
                elif event.type == pg.MOUSEBUTTONUP:
                    self.held_e = None

                if event.type == pg.MOUSEBUTTONDOWN and self.game_over:
                    if self.win and pg.Rect(self.W - 150, self.H // 2 + 70, 120, 50).collidepoint(event.pos):
                        return "win"
                    if not self.win and pg.Rect(self.W - 150, self.H // 2 + 70, 120, 50).collidepoint(event.pos):
                        return "lose"

            if self.held_e:
                mouse_x, mouse_y = pg.mouse.get_pos()
                new_x = max(self.held_e.r, min(mouse_x, self.W - self.held_e.r))
                new_y = max(self.held_e.r, min(mouse_y, self.H - self.held_e.r))
                self.held_e.pos = [new_x, new_y]

            if not self.game_over:
                for e in self.electrons:
                    dist = ((e.pos[0] - self.n_pos[0]) ** 2 + (e.pos[1] - self.n_pos[1]) ** 2) ** 0.5
                    e.color = (255, 255, 0) if self.s_r - 20 < dist < self.s_r + 20 else (0, 100, 255)

            self.sprites_group.draw(self.screen)

            pg.draw.circle(self.screen, (255, 0, 0), self.n_pos, self.n_r)
            plus_txt = self.label_font.render(str(self.atom_data["protons"]) + "+", 1, (255, 255, 255))
            self.screen.blit(plus_txt, plus_txt.get_rect(center=self.n_pos))
            pg.draw.circle(self.screen, (0, 0, 0), self.n_pos, self.s_r, 2)
            for e in self.electrons:
                e.draw(self.screen, self.label_font)

            inst_txt = self.font.render(
                f"원소 {self.atom_data['name']}({self.atom_data['valence_e']})과 같은 원자가전자배치를 가진 원자를 만드시오.", 1, (0, 0, 0))

            self.screen.blit(inst_txt, inst_txt.get_rect(center=(self.W // 2, 40)))

            if not self.game_over:
                pg.draw.rect(self.screen, (150, 150, 150), pg.Rect(self.W - 150, self.H // 2, 120, 50),
                             border_radius=10)
                btn_txt = self.font.render("끝내기", 1, (0, 0, 0))
                self.screen.blit(btn_txt, btn_txt.get_rect(center=(self.W - 90, self.H // 2 + 25)))
            else:
                text_y = self.H // 2 - 80
                result_msg = "정답입니다." if self.win else "오답입니다."
                result_color = (0, 255, 0) if self.win else (255, 0, 0)
                result_txt = self.result_font.render(result_msg, 1, result_color)
                self.screen.blit(result_txt, result_txt.get_rect(center=(self.W // 2, text_y)))

                info_txt = self.font.render(f"{self.atom_data['name']}은 원자가전자가 {self.atom_data['valence_e']}개인 원소입니다.",
                                            1, (0, 0, 0))
                self.screen.blit(info_txt, info_txt.get_rect(center=(self.W // 2, self.H // 2 + 30)))

                btn_rect = pg.Rect(self.W - 150, self.H // 2 + 70, 120, 50)
                btn_color = (0, 100, 255) if self.win else (150, 150, 150)
                btn_text = "그만두기" if self.win else "다시 하기"
                btn_text_color = (255, 255, 255) if self.win else (0, 0, 0)

                pg.draw.rect(self.screen, btn_color, btn_rect, border_radius=10)
                btn_txt = self.font.render(btn_text, 1, btn_text_color)
                self.screen.blit(btn_txt, btn_txt.get_rect(center=btn_rect.center))

            pg.display.flip()