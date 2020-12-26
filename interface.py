import pygame
from constants import *
from cmath import exp, pi, phase as atan2, sqrt, cos, sin


class Interface:
    def __init__(self, x, y, width, height, mode):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.mode = mode
        self.cycles = []
        self.time = 0
    
    def update(self, window, events):
        self.draw(window)
    
    def draw(self, window):
        pass

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

    def dft(self, _points, sort, reverse):
        points = []
        for x, y in _points:
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

        self.cycles[-1]["last"] = True

        return self.cycles
