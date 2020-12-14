import pygame
from constants import *


pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fourier Transform Visualizer")


def main(window):
    clock = pygame.time.Clock()
    points = []
    drawing = False

    while True:
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                with open("points.txt", "w") as f:
                    for i in range(len(points)):
                        points[i] = " ".join(map(str, (points[i][0] - WIDTH/2, points[i][1] - HEIGHT/2))) + "\n"
                    f.writelines(points)
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False

        if drawing:
            points.append(pygame.mouse.get_pos())

        for i in range(len(points)-1):
            pygame.draw.line(window, WHITE, points[i], points[i+1], 2)

        pygame.display.update()


main(WINDOW)