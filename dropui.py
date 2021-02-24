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

from constants import WHITE
import pygame
pygame.init()


class SortUI:
    def __init__(self, text, default):
        self.dir = default
        self.text = text
    
    def update(self, window, x, y, width, height):
        font = pygame.font.SysFont("comicsans", height - 10)
        tri_padding = 17
        tri_width = height - tri_padding*2
        tri_surf = pygame.Surface((tri_width, tri_width), pygame.SRCALPHA)
        tri_surf.fill((0, 0, 0, 0))
        tri_left = tri_top = 0
        tri_right =  tri_bottom = tri_width
        tri_middle = tri_width/2
        tri_up = (tri_middle, tri_top), (tri_left, tri_bottom), (tri_right, tri_bottom)
        tri_down = (tri_middle, tri_bottom), (tri_left, tri_top), (tri_right, tri_top)
        tri = tri_up if self.dir else tri_down
        pygame.draw.polygon(tri_surf, WHITE, tri)
        window.blit(tri_surf, (x + width - tri_padding - tri_width, y + tri_padding))
        text = font.render(self.text, 1, WHITE)
        window.blit(text, (x + 10, (y + height/2 - text.get_height()/2)))
