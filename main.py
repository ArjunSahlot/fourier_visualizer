#
#  Fourier visualizer
#  Visualize the fourier transform in pygame.
#  Copyright Arjun Sahlot 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import pygame
from constants import *
from elements import *
from dropui import *
from interface import Interface


# Window Management
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fourier Visualizer")


def main(window):
    pygame.init()
    clock = pygame.time.Clock()
    button = Button(100, 15, 200, 50, "Visualize", bg_col_hover=(80, 80, 80))
    choices = (SortUI("Radius", False), SortUI("Speed", False), SortUI("Phase", False))
    sort_drop = Dropdown(
        (100, 80),
        (200, 50),
        (200, 150),
        choices=choices,
        border_col=WHITE,
        bg_col=BLACK,
        color=WHITE,
        hightlight_col=(80, 80, 80),
        sensitivity=10,
        initial_text="Sort"
    )
    reset = Check(26.5, 147, "Clear every iteration")
    reverse = Check(114.5, 210, "Reverse")
    speed = Slider([80, 280], (240, 30), 18, pygame.font.SysFont("comicsans", 25), "Speed", 90, (1, 100))
    draw = ColorPicker((70, 400), 100, (280, 400), (40, 200), False, False, 5, (0, 0), (0, 0), start="white")
    fourier = ColorPicker((70, 650), 100, (280, 650), (40, 200), False, False, 5, (0, 0), (0, 0), start="red")
    color_label_font = pygame.font.SysFont("comicsans", 25)
    mode = "CREATE"
    tab_start = None
    interface = Interface(400, 0, 1000, 1000)

    while True:
        clock.tick(FPS)
        window.fill(BLACK)
        pygame.draw.line(window, WHITE, (400, 0), (400, 1000), 5)
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        update = sort_drop.draw(window, events)
        mode_update = False
        if keys[pygame.K_TAB]:
            if tab_start != mode:
                mode = "CREATE" if mode == "VISUALIZE" else "VISUALIZE"
                button.text = "CREATE" if mode == "VISUALIZE" else "VISUALIZE"
                mode_update = True
                tab_start = mode
        else:
            tab_start = None
        if button.update(window, events):
            mode = "CREATE" if mode == "VISUALIZE" else "VISUALIZE"
            button.text = "CREATE" if mode == "VISUALIZE" else "VISUALIZE"
            mode_update = True
        reset.y = 147 + sort_drop.pop_size[1] if sort_drop.popped else 147
        reset.update(window, events)
        reverse.y = 210 + sort_drop.pop_size[1] if sort_drop.popped else 210
        reverse.update(window, events)
        speed.loc[1] = 280 + sort_drop.pop_size[1] if sort_drop.popped else 280
        speed.update(window, events)
        draw.wheel_pos[1] = 400 + sort_drop.pop_size[1] if sort_drop.popped else 400
        draw.slider_pos[1] = 400 + sort_drop.pop_size[1] if sort_drop.popped else 400
        draw.update(window)
        text = color_label_font.render("Draw color", 1, draw.get_rgb() if sum(draw.get_rgb()) > 80 else (255, 255, 255))
        window.blit(text, (200 - text.get_width()/2, 370 + sort_drop.pop_size[1] if sort_drop.popped else 370))
        fourier.wheel_pos[1] = 650 + sort_drop.pop_size[1] if sort_drop.popped else 650
        fourier.slider_pos[1] = 650 + sort_drop.pop_size[1] if sort_drop.popped else 650
        fourier.update(window)
        text = color_label_font.render("Fourier color", 1, fourier.get_rgb() if sum(fourier.get_rgb()) > 80 else (255, 255, 255))
        window.blit(text, (200 - text.get_width()/2, 620 + sort_drop.pop_size[1] if sort_drop.popped else 620))
        interface.speed = speed.value
        interface.update(window, events, mode, reset.checked, sort_drop.selected, update, mode_update, reverse.checked, draw.get_rgb(), fourier.get_rgb())
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.display.update()


main(WINDOW)
