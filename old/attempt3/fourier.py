from constants import *
from cmath import pi, phase as atan2, sqrt, exp


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
        cycles.append({"freq": freq, "phase": phase, "amp": amp})

    cycles.sort(key=lambda x: x["amp"], reverse=True)
    cycles[-1]["last"] = True

    return cycles
