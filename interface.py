import pygame
from constants import *
from cmath import exp, pi, phase as atan2, sqrt, cos, sin
import numpy as np
from elements import *
import pickle


class Interface:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.cycles = []
        self.time = 0
        self.i = 0
        self.speed = 90
        self.line_thick = 4
        self.points = []
        self.fourier_conns = []
        self.clear = Button(850, 0, 100, 50, "Clear", bg_col_hover=(80, 80, 80))
        self.name = TextInput(
            (950, 960),
            (300, 40),
            (0, 0, 1),
            border_col=WHITE,
            text_col=WHITE,
            cursor_col=(255, 255, 254),
            font=pygame.font.SysFont("comicsans", 30),
            max_len=20
        )
        self.draws = Dropdown(
            (1090, 0),
            (300, 50),
            (300, 150),
            bg_col=(0, 0, 0),
            border_col=WHITE,
            color=WHITE,
            hightlight_col=(80, 80, 80),
            sensitivity=10,
            type="draw"
        )
        self.save_draw = Button(1240, 65, 150, 40, "Save Creations", bg_col_hover=(80, 80, 80), font_size=25)
        self.save = Button(1265, 960, 135, 40, "Save", bg_col_hover=(80, 80, 80))
        self.loop = Check(415, 15, "Loop")
        self.play = PlayButton(415, 905)
        self.drawing = False
        self.data = pickle.load(open(os.path.join(PARDIR, "creations.fourier"), "rb")) if os.path.isfile(os.path.join(PARDIR, "creations.fourier")) else {}
        self.draws.choices = list(self.data.keys())
    
    def update(self, window, events, mode, reset, sort, update, mode_update, reverse):
        mx, my = pygame.mouse.get_pos()
        speed = int(np.interp(self.speed, (1, 100), (30, 1)))
        self.i += 1
        self.i %= speed
        if self.cycles and self.i % speed == 0:
            num = -2 if reverse else 2
            self.time += num * pi / len(self.cycles) if self.play.status else 0
        if update:
            if isinstance(sort, str):
                pass
            else:
                self.dft(sort.text, sort.dir)
        if mode_update:
            self.time = 0
            self.fourier_conns.clear()
            if self.loop.checked:
                self.points = self.points + list(reversed(self.points))
            if mode == "VISUALIZE":
                text = pygame.font.SysFont("comicsans", 80).render("Calculating...", 1, WHITE)
                window.blit(text, (900 - text.get_width()/2, 500 - text.get_height()/2))
                pygame.display.update()
                if isinstance(sort, str):
                    self.dft("radius", True)
                else:
                    self.dft(sort.text, sort.dir)
            else:
                if self.draws.selected == "Untitled":
                    self.points.clear()
                else:
                    self.points = self.data[self.draws.selected]

        if self.time > 2 * pi or self.time < -2 * pi:
            self.time = 0
            if reset:
                self.fourier_conns.clear()

        self.draw(window, mode, self.loop.checked)
        in_draw_area = self.x < mx < self.x + self.width and self.y < my < self.y + self.height
        if mode == "CREATE":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and in_draw_area:
                    if not (
                        self.clear.clicked(events) or
                        self.save.clicked(events) or
                        self.name.clicked(events) or
                        self.draws.clicked(events) or
                        self.loop.clicked(events) or
                        self.play.clicked(events) or
                        self.save_draw.clicked(events)
                    ):
                        self.drawing = True
                        if self.draws.selected in self.data:
                            self.draws.selected = "Untitled"
                if event.type == pygame.MOUSEBUTTONUP:
                    self.drawing = False

            if in_draw_area and self.drawing:
                self.points.append((mx - self.x - self.width/2, my - self.y - self.height/2))

            clear = self.clear.update(window, events)
            if clear:
                self.draws.selected = "Untitled"
                self.points.clear()

            if self.save.update(window, events) or self.name.draw(window, events):
                if self.name.text:
                    if self.name.text not in self.draws.choices:
                        self.draws.choices.append(self.name.text)
                    self.draws.selected = self.name.text
                    self.data[self.name.text] = self.points[:]
                    self.name.clear_text()

            draw_update = self.draws.draw(window, events)
            if draw_update:
                if self.draws.selected in self.data:
                    self.points = self.data[self.draws.selected]
                if isinstance(draw_update, str):
                    del self.data[draw_update]
            self.loop.update(window, events)
            self.save_draw.y = 65 + self.draws.pop_size[1] if self.draws.popped else 65
            self.save_draw.rect[1] = 65 + self.draws.pop_size[1] if self.draws.popped else 65
            if self.save_draw.update(window, events):
                pickle.dump(self.data, open(os.path.join(PARDIR, "creations.fourier"), "wb"))
            
        else:
            self.play.update(window, events)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_DOWN]:
                if self.cycles and self.i % speed == 0:
                    self.time -= 2 * pi / len(self.cycles)
            if keys[pygame.K_RIGHT] or keys[pygame.K_UP]:
                if self.cycles and self.i % speed == 0:
                    self.time += 2 * pi / len(self.cycles)

    
    def draw(self, window, mode, loop):
        if mode == "VISUALIZE":
            self.fourier_conns.append(self.draw_fourier(window))
            for i in range(len(self.fourier_conns) - 1):
                pygame.draw.line(window, RED, self.fourier_conns[i], self.fourier_conns[i+1], self.line_thick)
            text_surf = pygame.font.SysFont("comicsans", 40).render(self.draws.selected, 1, WHITE)
            window.blit(text_surf, (WIDTH - 10 - text_surf.get_width(), 10))
        else:
            if len(self.points) > 1:
                offset = np.array((self.x + self.width/2, self.y + self.height/2))
                for i in range(len(self.points) - 1):
                    pygame.draw.line(window, WHITE, self.points[i] + offset, self.points[i+1] + offset, self.line_thick)
                if not loop:
                    pygame.draw.line(window, WHITE, self.points[-1] + offset, self.points[0] + offset, self.line_thick)

    def draw_fourier(self, window):
        x, y = self.x + self.width/2, self.y + self.height/2

        for cycle in self.cycles:
            prev_x = x
            prev_y = y
            freq = cycle["freq"]
            radius = cycle["amp"]
            phase = cycle["phase"]
            x += radius * cos(freq * self.time + phase)
            y += radius * sin(freq * self.time + phase)

            pygame.draw.circle(window, RED if len(cycle) == 4 else WHITE, (prev_x.real, prev_y.real), radius, 1)
            pygame.draw.line(window, RED if len(cycle) == 4 else WHITE, (prev_x.real, prev_y.real), (x.real, y.real), self.line_thick)

        return (x.real, y.real)

    def dft(self, sort, reverse):
        points = []
        for x, y in self.points:
            points.append(complex(x, y))

        self.cycles = []
        N = len(points)
        for k in range(N):
            summation = complex(0, 0)
            for n in range(N):
                num = exp(-2j * pi * k * n / N)
                summation += points[n] * num

            summation /= N

            freq = k
            phase = atan2(summation)
            amp = sqrt(summation.real**2 + summation.imag**2).real
            self.cycles.append({"freq": freq, "phase": phase, "amp": amp})

        if sort.lower() == "radius":
            self.cycles.sort(key=lambda x: x["amp"], reverse=reverse)
        elif sort.lower() == "phase":
            self.cycles.sort(key=lambda x: x["phase"], reverse=reverse)
        elif sort.lower() == "speed":
            self.cycles.sort(key=lambda x: x["freq"], reverse=reverse)

        if self.cycles: self.cycles[-1]["last"] = True

        return self.cycles
