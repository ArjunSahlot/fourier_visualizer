import pygame
from constants import *
from fourier import *


pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fourier Transform Visualizer")


def main(window):
    clock = pygame.time.Clock()
    with open("points.txt", "r") as f:
        points = []
        lines = f.read().strip().split("\n")
        for line in lines:
            points.append(tuple(map(float, line.split())))

    cycles = discrete_fourier_transform(points)
    fourier = Fourier(WIDTH/2, HEIGHT/2, cycles, 1)

    while True:
        clock.tick(FPS)
        window.fill(BLACK)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        fourier.draw(window)
        pygame.display.update()


main(WINDOW)