import pygame
from constants import *
from elements import *


# Window Management
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fourier Visualizer")


def main(window):
    pygame.init()
    clock = pygame.time.Clock()
    drop = Dropdown((10, 10), (200, 50), (200, 300), border_col=WHITE, bg_col=BLACK, color=WHITE, hightlight_col=(80, 80, 80))
    button = Button(220, 10, 200, 50, "HOOLOOBABA", bg_col_hover=(80, 80, 80))

    while True:
        clock.tick(FPS)
        window.fill(BLACK)
        events = pygame.event.get()
        drop.draw(window, events)
        button.update(window, events)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.display.update()


main(WINDOW)