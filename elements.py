import pygame
from constants import *

pygame.init()

class Dropdown:

    def __init__(self,
                loc,
                size,
                pop_size,
                bg_col=(255, 255, 255),
                initial_text="Select",
                choices=(),
                font=pygame.font.SysFont("comicsans", 35),
                color=(0, 0, 0),
                hightlight_col=(80, 80, 255),
                border_col=(0, 0, 0),
                border = 5,
                pop_border = 3,
                rounding=10,
                text_padding=10,
                textbox_padding=10,
                tri_padding=15,
                sensitivity=5,
                view=1):

        self.loc, self.size = loc, size
        self.selected = initial_text
        self.pop_loc = (loc[0] + size[0]/2 - pop_size[0]/2, loc[1] + size[1] - pop_border)
        self.pop_size = pop_size
        self.choices = choices
        self.font = font
        self.color = color
        self.bg_col = bg_col
        self.hightlight_col = hightlight_col
        self.tri_padding = tri_padding
        self.border = border
        self.pop_border = pop_border
        self.border_col = border_col
        self.textbox_size = (self.pop_size[0], self.font.render("A", 1, (0, 0, 0)).get_height() + text_padding*2)
        self.textbox_padding = textbox_padding
        self.sensitivity, self.rounding = sensitivity, rounding
        self.popped = False
        width = self.size[1] - self.tri_padding*2
        self.tri_rect = (self.loc[0] + self.size[0] - self.tri_padding - width, self.loc[1] + self.tri_padding, width, width)
        self.surf = pygame.Surface(pop_size, pygame.SRCALPHA)
        self.slider_y = 0
        self.view = view

    def draw(self, window, events):
        pygame.draw.rect(window, self.bg_col, (*self.loc, *self.size), border_radius=self.rounding)

        self._update(window, events)

        pygame.draw.rect(window, self.border_col, (*self.loc, *self.size), self.border, border_top_left_radius=self.rounding, border_top_right_radius=self.rounding)
        if isinstance(self.selected, str):
            text = self.font.render(self.selected, 1, self.color)
            window.blit(text, (self.loc[0] + self.size[0]/2 - text.get_width()/2, self.loc[1] + self.size[1]/2 - text.get_height()/2))
        else:
            self.selected.update(window, *self.loc, self.size[0] - 30, self.size[1])


        left = self.tri_rect[0]
        middle = self.tri_rect[0] + self.tri_rect[2]/2
        right = self.tri_rect[0] + self.tri_rect[2]
        top = self.tri_rect[1]
        bottom = self.tri_rect[1] + self.tri_rect[3]

        if self.popped:
            pygame.draw.polygon(window, self.border_col, ((middle, top), (left, bottom), (right, bottom)))
            self.draw_surf(window)
            pygame.draw.rect(window, self.border_col, (*self.pop_loc, *self.pop_size), self.pop_border, border_bottom_left_radius=self.rounding, border_bottom_right_radius=self.rounding)
        else:
            pygame.draw.polygon(window, self.border_col, ((middle, bottom), (left, top), (right, top)))

    def get_selection(self):
        return self.selected

    def draw_surf(self, window):
        self.surf.fill(self.bg_col)
        mx, my = pygame.mouse.get_pos()
        for i in range(len(self.choices)):
            y = i * self.textbox_size[1] + self.slider_y
            if pygame.Rect(self.pop_loc[0], y + self.pop_loc[1], *self.textbox_size).collidepoint(mx, my) or self.choices[i] == self.selected:
                pygame.draw.rect(self.surf, self.hightlight_col, (self.textbox_padding/2, y + self.textbox_padding/2, self.textbox_size[0] - self.textbox_padding, self.textbox_size[1] - self.textbox_padding), border_radius=self.rounding)
        window.blit(self.surf, self.pop_loc)
        for i, text in enumerate(self.choices):
            text.update(window, self.pop_loc[0], i * self.textbox_size[1] + self.slider_y + self.pop_loc[1], *self.textbox_size)

    def _update(self, window, events):
        mx, my = pygame.mouse.get_pos()
        if pygame.Rect(*self.loc, *self.size).collidepoint(mx, my):
            pygame.draw.rect(window, self.hightlight_col, (*self.loc, *self.size), border_radius=self.rounding)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.popped = not self.popped
                    if event.button == 3:
                        if hasattr(self.selected, "dir"):
                            self.selected.dir = not self.selected.dir
        else:
            if pygame.Rect(*self.pop_loc, *self.pop_size).collidepoint(mx, my) and self.popped:
                for i in range(len(self.choices)):
                    y = i * self.textbox_size[1] + self.slider_y
                    if pygame.Rect(self.pop_loc[0], y + self.pop_loc[1], *self.textbox_size).collidepoint(mx, my):
                        for event in events:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    self.selected = self.choices[i]
                                if event.button == 3:
                                    self.choices[i].dir = not self.choices[i].dir

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.popped = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(*self.pop_loc, *self.pop_size).collidepoint(mx, my):
                    if event.button == 4:
                        self.slider_y += self.sensitivity
                    if event.button == 5:
                        self.slider_y -= self.sensitivity
                self.slider_y = min(self.slider_y, 0)
                self.slider_y = max(self.slider_y, -self.textbox_size[1]*(len(self.choices)-self.view))


class Button:
    def __init__(self,
                x,
                y,
                width,
                height,
                text,
                font_size=35,
                text_col=WHITE,
                bg_col=BLACK,
                bg_col_hover=BLACK,
                border=5,
                border_col=WHITE,
                rounding=1):

        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(x, y, width, height)
        self.text, self.text_col = text, text_col
        self.font = pygame.font.SysFont("comicsans", font_size)
        self.bg_col, self.bg_col_hover = bg_col, bg_col_hover
        self.border = border
        self.rounding = rounding
        self.border_col = border_col
    
    def update(self, window, events):
        color = self.bg_col
        clicked = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = self.bg_col_hover
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
        
        pygame.draw.rect(window, color, self.rect, border_radius=self.rounding)
        if self.border > 0:
            pygame.draw.rect(window, self.border_col, self.rect, self.border, border_radius=self.rounding)
        text = self.font.render(self.text, 1, self.text_col)
        window.blit(text, (self.x + self.width/2 - text.get_width()/2, self.y + self.height/2 - text.get_height()/2))

        return clicked

class Check:
    width = height = 50

    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.checked = False
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 0))
        pygame.draw.polygon(self.surf, WHITE, [(9.7, 19.8), (3.4, 29.3), (21.5, 38.2), (45.3, 16.4), (38.6, 9.9), (22.5, 26.9)])
        self.text = text

    def update(self, window, events):
        self.draw(window)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(event.pos):
                    self.checked = not self.checked

    def draw(self, window):
        text_surf = pygame.font.SysFont("comicsans", self.height - 8).render(self.text, 1, WHITE)
        pygame.draw.rect(window, WHITE, (self.x, self.y, self.width, self.height), 5, 1)
        if self.checked:
            window.blit(self.surf, (self.x, self.y))
        window.blit(text_surf, (self.x + self.width + 8, self.y + self.height/2 - text_surf.get_height()/2))