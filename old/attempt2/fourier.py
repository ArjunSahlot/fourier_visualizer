import pygame
from constants import *
from cmath import sin, cos, pi, phase as atan2, sqrt, exp


class Fourier:
    def __init__(self, x, y, cycles, speed=10):
        self.x, self.y = x, y
        self.cycles = cycles
        self.cycles[-1].make_last()
        self.speed = speed / 10
        self.prev = None
        self.time = 0
        self.time_inc = 2 * pi / len(cycles)
        self.surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 0))

    def draw(self, window):
        x, y = self.x, self.y
        for cycle in self.cycles:
            x, y = cycle.draw(window, x, y, self.time, self.speed)

        if self.prev is not None:
            pygame.draw.line(self.surf, RED, self.prev, (x, y), 3)
        self.prev = (x, y)

        window.blit(self.surf, (0, 0))
        self.time += self.time_inc


class Cycle:
    def __init__(self, amp, phase, freq):
        self.amp, self.phase, self.freq = amp, phase, freq
        self.last = False

    def make_last(self):
        self.last = True

    def draw(self, window, x, y, time, speed):
        x_pos = cos((self.freq * time + self.phase)*10/speed).real*self.amp + x
        y_pos = sin((self.freq * time + self.phase)*10/speed).real*self.amp + y
        pos = (x_pos, y_pos)
        pygame.draw.circle(window, WHITE if not self.last else RED, (x, y), self.amp, 1)
        pygame.draw.line(window, WHITE if not self.last else RED, (x, y), pos, 3)
        return pos

    def __repr__(self):
        return f"Radius: {self.amp}, Rotation: {self.rotation}, Freq: {self.freq}"


def discrete_fourier_transform(_points):
    points = []
    for x, y in _points:
        points.append(complex(x, y))

    cycles = []
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
        cycles.append(Cycle(amp, phase, freq))

    return cycles
