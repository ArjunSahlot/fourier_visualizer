import pygame
from constants import *
from math import *


class _Complex:
    def __init__(self, re, im):
        self.re, self.im = re, im

    def multiply(self, complex):
        return _Complex(self.re * complex.re - self.im * complex.im, self.re * complex.im + self.im * complex.re)

    def add(self, complex):
        self.re += complex.re
        self.im += complex.im

    def divide(self, num):
        self.re /= num
        self.im /= num

    def __repr__(self):
        return f"Real: {self.re}, Imaginary: {self.im}"


class Fourier:
    def __init__(self, x, y, cycles, speed=10):
        self.x, self.y = x, y
        self.cycles = cycles
        self.cycles[-1].make_last()
        self.speed = speed / 10
        self.prev = None
        self.surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 0))

    def draw(self, window):
        x, y = self.x, self.y
        for cycle in self.cycles:
            x, y = cycle.draw(window, x, y, self.speed)

        if self.prev is not None:
            pygame.draw.line(self.surf, RED, self.prev, (x, y), 3)
        self.prev = (x, y)

        window.blit(self.surf, (0, 0))


class Cycle:
    def __init__(self, amp, phase, hertz):
        self.amp, self.rotation, self.freq = amp, phase, hertz*2*pi/FPS
        self.last = False

    def make_last(self):
        self.last = True

    def draw(self, window, x, y, speed):
        pos = (cos(self.rotation)*self.amp + x, sin(self.rotation)*self.amp + y)
        pygame.draw.circle(window, WHITE if not self.last else RED, (x, y), self.amp, 1)
        pygame.draw.line(window, WHITE if not self.last else RED, (x, y), pos, 3)
        self.rotation += self.freq * speed
        return pos

    def __repr__(self):
        return f"Radius: {self.amp}, Rotation: {self.rotation}, Freq: {self.freq}"


def discrete_fourier_transform(_points):
    points = []
    for x, y in _points:
        points.append(_Complex(x, y))

    cycles = []
    N = len(points)
    for k in range(N):
        summation = _Complex(0, 0)
        for n in range(N):
            phi = (2 * pi * k * n) / N
            num = _Complex(cos(phi), -sin(phi))
            summation.add(points[n].multiply(num))

        summation.divide(N)

        freq = k
        phase = atan2(summation.im, summation.re)
        amp = sqrt(summation.re**2 + summation.im**2)
        cycles.append(Cycle(amp, phase, freq))

    return cycles