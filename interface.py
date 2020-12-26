import pygame
from constants import *
from cmath import exp, pi, phase as atan2, sqrt


class Interface:
    def __init__(self, x, y, width, height, mode):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.mode = mode
    
    def update(self, window, events):
        self.draw(window)
    
    def draw(self, window):
        pass

    def dft(self, _points, sort, reverse):
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
            cycles.append({"freq": freq, "phase": phase, "amp": amp})

        if sort.lower() == "radius":
            cycles.sort(key=lambda x: x["amp"], reverse=reverse)
        elif sort.lower() == "phase":
            cycles.sort(key=lambda x: x["phase"], reverse=reverse)
        elif sort.lower() == "speed":
            cycles.sort(key=lambda x: x["freq"], reverse=reverse)

        cycles[-1]["last"] = True

        return cycles
