import pygame
pygame.init()


class SortUI:
    def __init__(self, text, default):
        self.dir = default
        self.text = text
    
    def update(self, window, events, x, y, width, height):
        font = pygame.font.SysFont("comicsans", height - 6)
        