import pygame
from constants import *
from fourier import *
from cmath import sin, cos, pi


pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fourier Transform Visualizer")


def draw_fourier(window, x, y, time, fourier):
    for cycle in fourier:
        prev_x = x
        prev_y = y
        freq = cycle["freq"]
        radius = cycle["amp"]
        phase = cycle["phase"]
        x += radius * cos(freq * time + phase)
        y += radius * sin(freq * time + phase)

        pygame.draw.circle(window, RED if len(cycle) == 4 else WHITE, (prev_x.real, prev_y.real), radius, 1)
        pygame.draw.line(window, RED if len(cycle) == 4 else WHITE, (prev_x.real, prev_y.real), (x.real, y.real), 3)

    return (x.real, y.real)


def main(window):
    clock = pygame.time.Clock()
    with open("points.txt", "r") as f:
        points = []
        lines = f.read().strip().split("\n")
        for line in lines:
            points.append(tuple(map(float, line.split())))

    fourier = discrete_fourier_transform(points)
    conns = []
    speed = 10
    time = 0

    while True:
        clock.tick(FPS)
        window.fill(BLACK)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        conns.append(draw_fourier(window, WIDTH/2, HEIGHT/2, time, fourier))
        for i in range(len(conns)-1):
            pygame.draw.line(window, RED, conns[i], conns[i+1], 4)
        time += 2 * pi * speed / len(fourier) / 10
        pygame.display.update()


main(WINDOW)