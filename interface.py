import pygame
from constants import *
from cmath import exp, pi, phase as atan2, sqrt, cos, sin
import numpy as np
from elements import Button


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
        self.drawing = False
    
    def update(self, window, events, mode, loop, reset, sort, update, mode_update, playing):
        mx, my = pygame.mouse.get_pos()
        speed = int(np.interp(self.speed, (1, 100), (30, 1)))
        self.i += 1
        self.i %= speed
        if self.cycles and self.i % speed == 0:
            self.time += 2 * pi / len(self.cycles) if playing else 0
        if update:
            if isinstance(sort, str):
                pass
            else:
                self.dft(sort.text, sort.dir)
        if mode_update:
            self.time = 0
            self.fourier_conns.clear()
            if loop:
                self.points = self.points + list(reversed(self.points))
            if mode == "VISUALIZE":
                text = pygame.font.SysFont("comicsans", 80).render("Calculating...", 1, WHITE)
                window.blit(text, (900 - text.get_width()/2, 500 - text.get_height()/2))
                pygame.display.update()
                if isinstance(sort, str):
                    self.dft("radius", True)
                else:
                    self.dft(sort.text, sort.dir)
            if mode == "CREATE":
                self.points.clear()

        if self.time > 2 * pi:
            self.time = 0
            if reset:
                self.fourier_conns.clear()

        self.draw(window, mode, loop)
        in_draw_area = self.x < mx < self.x + self.width and self.y < my < self.y + self.height
        if mode == "CREATE":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and in_draw_area:
                    self.drawing = True if not pygame.Rect(self.clear.x, self.clear.y, self.clear.width, self.clear.height).collidepoint(event.pos) else False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.drawing = False

            clear = self.clear.update(window, events)
            if in_draw_area and self.drawing:
                self.points.append((mx - self.x - self.width/2, my - self.y - self.height/2))
            if clear:
                self.points.clear()

    
    def draw(self, window, mode, loop):
        if mode == "VISUALIZE":
            self.fourier_conns.append(self.draw_fourier(window))
            for i in range(len(self.fourier_conns) - 1):
                pygame.draw.line(window, RED, self.fourier_conns[i], self.fourier_conns[i+1], self.line_thick)
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
