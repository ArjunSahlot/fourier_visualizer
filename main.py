import pygame
from constants import *
from elements import *
from sort import SortUI
from interface import Interface


# Window Management
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fourier Visualizer")


def main(window):
    pygame.init()
    clock = pygame.time.Clock()
    button = Button(100, 15, 200, 50, "Visualize", bg_col_hover=(80, 80, 80))
    choices = (SortUI("Radius", False), SortUI("Speed", False), SortUI("Phase", False))
    drop = Dropdown((100, 80),
                    (200, 50),
                    (200, 150),
                    choices=choices,
                    border_col=WHITE,
                    bg_col=BLACK,
                    color=WHITE,
                    hightlight_col=(80, 80, 80),
                    sensitivity=10,
                    initial_text="Sort")
    loop = Check(137, 147, "Loop")
    reset = Check(26.5, 210, "Clear every iteration")
    speed = Slider([80, 275], (240, 30), 18, pygame.font.SysFont("comicsans", 25), "Speed", 90, (1, 100))
    mode = "CREATE"
    interface = Interface(400, 0, 1000, 1000)
    playing = True

    while True:
        clock.tick(FPS)
        window.fill(BLACK)
        pygame.draw.line(window, WHITE, (400, 0), (400, 1000), 5)
        events = pygame.event.get()
        update = drop.draw(window, events)
        mode_update = False
        if button.update(window, events):
            mode = "CREATE" if mode == "VISUALIZE" else "VISUALIZE"
            button.text = "CREATE" if mode == "VISUALIZE" else "VISUALIZE"
            mode_update = True
        loop.y = 145 + drop.pop_size[1] if drop.popped else 147
        loop.update(window, events)
        reset.y = 210 + drop.pop_size[1] if drop.popped else 210
        reset.update(window, events)
        speed.loc[1] = 275 + drop.pop_size[1] if drop.popped else 275
        speed.update(window, events)
        interface.speed = speed.value
        interface.update(window, events, mode, loop.checked, reset.checked, drop.selected, update, mode_update, playing)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
        pygame.display.update()


main(WINDOW)