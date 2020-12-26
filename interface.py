import pygame
from constants import *
from cmath import exp, pi, phase as atan2, sqrt, cos, sin
import numpy as np


class Interface:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.cycles = []
        self.time = 0
        self.points = []
        self.fourier_conns = []
    
    def update(self, window, events, mode, loop, reset, sort, update, playing):
        mx, my = pygame.mouse.get_pos()
        if self.cycles: self.time += 2 * pi / len(self.cycles) if playing else 0
        if update:
            self.time = 0
            if isinstance(sort, str):
                self.dft("radius", True)
            else:
                self.dft(sort.text, sort.dir)
        self.draw(window, mode)
        if mode == "CREATE":
            if self.x < mx < self.x + self.width and self.y < my < self.y + self.height:
                if pygame.mouse.get_pressed()[0]:
                    self.points.append((mx - self.x - self.width/2, my - self.y - self.height/2))

    
    def draw(self, window, mode):
        if mode == "VISUALIZE":
            self.fourier_conns.append(self.draw_fourier(window))
            for i in range(len(self.fourier_conns) - 1):
                pygame.draw.line(window, RED, self.fourier_conns[i] + np.array((self.x + self.width/2, self.y + self.height/2)), self.fourier_conns[i+1] + np.array((self.x + self.width/2, self.y + self.height/2)), 3)
            if len(self.fourier_conns) > 1: pygame.draw.line(window, RED, self.fourier_conns[-1] + np.array((self.x + self.width/2, self.y + self.height/2)), self.fourier_conns[0] + np.array((self.x + self.width/2, self.y + self.height/2)), 3)
        else:
            if len(self.points) > 1:
                for i in range(len(self.points) - 1):
                    pygame.draw.line(window, WHITE, self.points[i] + np.array((self.x + self.width/2, self.y + self.height/2)), self.points[i+1] + np.array((self.x + self.width/2, self.y + self.height/2)), 3)
                pygame.draw.line(window, WHITE, self.points[-1] + np.array((self.x + self.width/2, self.y + self.height/2)), self.points[0] + np.array((self.x + self.width/2, self.y + self.height/2)), 3)

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
            pygame.draw.line(window, RED if len(cycle) == 4 else WHITE, (prev_x.real, prev_y.real), (x.real, y.real), 3)

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
