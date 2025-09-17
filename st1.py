import pygame as pg, sys, random

pg.init()
W, H = 800, 600
screen = pg.display.set_mode((W, H))
pg.display.set_caption("네온(Ne) 원자 게임")

C = lambda r, g, b: (r, g, b)
WHITE, BLACK, GRAY, BLUE, YELLOW, GREEN, RED = C(255, 255, 255), C(0, 0, 0), C(150, 150, 150), C(0, 100, 255), C(255,
                                                                                                                 255,
                                                                                                                 0), C(
    0, 255, 0), C(255, 0, 0)


def get_font(size):
    try:
        return pg.font.Font(
            pg.font.match_font('malgungothic') or pg.font.match_font('AppleGothic') or pg.font.match_font(
                'NanumGothic'), size)
    except:
        return pg.font.Font(None, size)


font, label_font, result_font = get_font(26), get_font(30), get_font(40)
n_pos, n_r, s_r = (W // 2, H // 2), 50, 200
goal_e = 8
held_e, game_over, win = None, False, False


class E:
    def __init__(self, x, y):
        self.pos, self.r, self.color = [x, y], 15, BLUE

    def draw(self):
        pg.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.r)
        txt = label_font.render("-", 1, BLACK)
        screen.blit(txt, txt.get_rect(center=self.pos))

    def get_rect(self):
        return pg.Rect(self.pos[0] - self.r, self.pos[1] - self.r, self.r * 2, self.r * 2)


def reset():
    global electrons, held_e, game_over, win
    electrons = [E(random.randint(10, W - 10), random.randint(10, H - 10)) for _ in range(14)]
    held_e, game_over, win = None, False, False


reset()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit();
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN and not game_over:
            if pg.Rect(W - 150, H // 2, 120, 50).collidepoint(event.pos):
                count = sum(1 for e in electrons if
                            s_r - 20 < ((e.pos[0] - n_pos[0]) ** 2 + (e.pos[1] - n_pos[1]) ** 2) ** 0.5 < s_r + 20)
                game_over, win = True, (count == goal_e)
            else:
                for e in electrons:
                    if e.get_rect().collidepoint(event.pos): held_e = e; break
        elif event.type == pg.MOUSEBUTTONUP:
            held_e = None

        if event.type == pg.MOUSEBUTTONDOWN and game_over:
            if win and pg.Rect(W - 150, H // 2 + 70, 120, 50).collidepoint(event.pos): pg.quit(); sys.exit()
            if not win and pg.Rect(W - 150, H // 2 + 70, 120, 50).collidepoint(event.pos): reset()

    if held_e: held_e.pos = pg.mouse.get_pos()
    if not game_over:
        for e in electrons:
            dist = ((e.pos[0] - n_pos[0]) ** 2 + (e.pos[1] - n_pos[1]) ** 2) ** 0.5
            e.color = YELLOW if s_r - 20 < dist < s_r + 20 else BLUE

    screen.fill(WHITE)

    pg.draw.circle(screen, RED, n_pos, n_r)
    plus_txt = label_font.render("+", 1, WHITE)
    screen.blit(plus_txt, plus_txt.get_rect(center=n_pos))
    pg.draw.circle(screen, BLACK, n_pos, s_r, 2)

    for e in electrons: e.draw()

    inst_txt = font.render("원소 Ne과 같은 원자가전자배치를 가진 원자를 만드시오.", 1, BLACK)
    screen.blit(inst_txt, inst_txt.get_rect(center=(W // 2, 40)))

    if not game_over:
        pg.draw.rect(screen, GRAY, pg.Rect(W - 150, H // 2, 120, 50), border_radius=10)
        btn_txt = font.render("끝내기", 1, BLACK)
        screen.blit(btn_txt, btn_txt.get_rect(center=(W - 90, H // 2 + 25)))
    else:
        text_y = H // 2 - 80
        result_msg = "정답입니다." if win else "오답입니다."
        result_color = GREEN if win else RED
        result_txt = result_font.render(result_msg, 1, result_color)
        screen.blit(result_txt, result_txt.get_rect(center=(W // 2, text_y)))

        info_txt = font.render("Ne은 원자가전자가 8개인 원소입니다.", 1, BLACK)
        screen.blit(info_txt, info_txt.get_rect(center=(W // 2, H // 2 + 30)))

        btn_rect = pg.Rect(W - 150, H // 2 + 70, 120, 50)
        btn_color = BLUE if win else GRAY
        btn_text = "그만두기" if win else "다시 하기"
        btn_text_color = WHITE if win else BLACK

        pg.draw.rect(screen, btn_color, btn_rect, border_radius=10)
        btn_txt = font.render(btn_text, 1, btn_text_color)
        screen.blit(btn_txt, btn_txt.get_rect(center=btn_rect.center))

    pg.display.flip()