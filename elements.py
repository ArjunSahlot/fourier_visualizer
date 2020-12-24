import pygame

pygame.init()

class Dropdown:

    def __init__(self,
                loc,
                size,
                pop_size,
                bg_col=(255, 255, 255),
                initial_text="Select",
                choices=("A", "B", "C", "D", "E", "F", "G", "H"),
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
        self.pop_loc = (loc[0] + size[0]//2 - pop_size[0]//2, loc[1] + size[1] - pop_border)
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
        self.silder_y = 0
        self.view = view

    def draw(self, window, events):
        pygame.draw.rect(window, self.bg_col, (*self.loc, *self.size), border_radius=self.rounding)

        self._update(window, events)

        pygame.draw.rect(window, self.border_col, (*self.loc, *self.size), self.border, border_top_left_radius=self.rounding, border_top_right_radius=self.rounding)
        text = self.font.render(self.selected, 1, self.color)
        window.blit(text, (self.loc[0] + self.size[0]//2 - text.get_width()//2, self.loc[1] + self.size[1]//2 - text.get_height()//2))


        left = self.tri_rect[0]
        middle = self.tri_rect[0] + self.tri_rect[2]//2
        right = self.tri_rect[0] + self.tri_rect[2]
        top = self.tri_rect[1]
        bottom = self.tri_rect[1] + self.tri_rect[3]

        if self.popped:
            pygame.draw.polygon(window, self.border_col, ((middle, top), (left, bottom), (right, bottom)))
            self.draw_surf()
            window.blit(self.surf, self.pop_loc)
            pygame.draw.rect(window, self.border_col, (*self.pop_loc, *self.pop_size), self.pop_border, border_bottom_left_radius=self.rounding, border_bottom_right_radius=self.rounding)
        else:
            pygame.draw.polygon(window, self.border_col, ((middle, bottom), (left, top), (right, top)))

    def get_selection(self):
        return self.selected

    def draw_surf(self):
        self.surf.fill(self.bg_col)
        mx, my = pygame.mouse.get_pos()
        for i, text in enumerate(self.choices):
            y = i * self.textbox_size[1] + self.silder_y
            if pygame.Rect(self.pop_loc[0], y + self.pop_loc[1], *self.textbox_size).collidepoint(mx, my) or self.choices[i] == self.selected:
                pygame.draw.rect(self.surf, self.hightlight_col, (self.textbox_padding//2, y + self.textbox_padding//2, self.textbox_size[0] - self.textbox_padding, self.textbox_size[1] - self.textbox_padding), border_radius=self.rounding)
            text = self.font.render(text, 1, self.color)
            self.surf.blit(text, (self.textbox_size[0]//2 - text.get_width()//2, y + self.textbox_size[1]//2 - text.get_height()//2))

    def _update(self, window, events):
        mx, my = pygame.mouse.get_pos()
        if pygame.Rect(*self.loc, *self.size).collidepoint(mx, my):
            pygame.draw.rect(window, self.hightlight_col, (*self.loc, *self.size), border_radius=self.rounding)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.popped = not self.popped
        else:
            if self.popped:
                for i in range(len(self.choices)):
                    y = i * self.textbox_size[1] + self.silder_y
                    if pygame.Rect(self.pop_loc[0], y + self.pop_loc[1], *self.textbox_size).collidepoint(mx, my):
                        for event in events:
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                self.selected = self.choices[i]

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.popped = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(*self.pop_loc, *self.pop_size).collidepoint(mx, my):
                    if event.button == 4:
                        self.silder_y += self.sensitivity
                    if event.button == 5:
                        self.silder_y -= self.sensitivity
                self.silder_y = min(self.silder_y, 0)
                self.silder_y = max(self.silder_y, -self.textbox_size[1]*(len(self.choices)-self.view))
