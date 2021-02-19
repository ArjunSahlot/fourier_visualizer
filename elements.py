import numpy as np
import pygame
from constants import *
from colorsys import rgb_to_hsv, hsv_to_rgb

pygame.init()

class Dropdown:
    def __init__(self,
                loc,
                size,
                pop_size,
                bg_col=(255, 255, 255),
                initial_text="Select",
                choices=[],
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
                view=1,
                type="sort"):

        self.loc, self.size = loc, size
        self.selected = initial_text
        self.pop_loc = (loc[0] + size[0]/2 - pop_size[0]/2, loc[1] + size[1] - pop_border)
        self.pop_size = pop_size
        self.choices = list(choices)
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
        self.type = type
        if type == "draw":
            self.selected = "Untitled"

    def draw(self, window, events):
        left = self.tri_rect[0]
        middle = self.tri_rect[0] + self.tri_rect[2]/2
        right = self.tri_rect[0] + self.tri_rect[2]
        top = self.tri_rect[1]
        bottom = self.tri_rect[1] + self.tri_rect[3]

        if self.popped: self.draw_surf(window)
        pygame.draw.rect(window, self.bg_col, (*self.loc, *self.size), border_radius=self.rounding)

        if (update := self._update(window, events)) is not None:
            return update

        pygame.draw.rect(window, self.border_col, (*self.loc, *self.size), self.border, border_top_left_radius=self.rounding, border_top_right_radius=self.rounding)
        if isinstance(self.selected, str):
            text = self.font.render(self.selected, 1, self.color)
            window.blit(text, (self.loc[0] + self.size[0]/2 - text.get_width()/2, self.loc[1] + self.size[1]/2 - text.get_height()/2))
        else:
            self.selected.update(window, *self.loc, self.size[0] - 30, self.size[1])

        if self.popped:
            pygame.draw.polygon(window, self.border_col, ((middle, top), (left, bottom), (right, bottom)))
            pygame.draw.rect(window, self.border_col, (*self.pop_loc, *self.pop_size), self.pop_border, border_bottom_left_radius=self.rounding, border_bottom_right_radius=self.rounding)
        else:
            pygame.draw.polygon(window, self.border_col, ((middle, bottom), (left, top), (right, top)))


    def get_selection(self):
        return self.selected

    def draw_surf(self, window):
        self.surf.fill(self.bg_col)
        mx, my = pygame.mouse.get_pos()
        for i, text in enumerate(self.choices):
            y = i * self.textbox_size[1] + self.slider_y
            if pygame.Rect(self.pop_loc[0], y + self.pop_loc[1], *self.textbox_size).collidepoint(mx, my) or self.choices[i] == self.selected:
                pygame.draw.rect(self.surf, self.hightlight_col, (self.textbox_padding/2, y + self.textbox_padding/2, self.textbox_size[0] - self.textbox_padding, self.textbox_size[1] - self.textbox_padding), border_radius=self.rounding)
            if self.type != "sort":
                text = self.font.render(text, 1, self.color)
                self.surf.blit(text, (self.textbox_size[0]//2 - text.get_width()//2, y + self.textbox_size[1]//2 - text.get_height()//2))
        window.blit(self.surf, self.pop_loc)
        if self.type == "sort":
            for i, text in enumerate(self.choices):
                y = i * self.textbox_size[1] + self.slider_y + self.pop_loc[1]
                if y > self.pop_loc[0]:
                    text.update(window, self.pop_loc[0], y, *self.textbox_size)

    def _update(self, window, events):
        mx, my = pygame.mouse.get_pos()
        if pygame.Rect(*self.loc, *self.size).collidepoint(mx, my):
            pygame.draw.rect(window, self.hightlight_col, (*self.loc, *self.size), border_radius=self.rounding)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.popped = not self.popped
                    if event.button == 3:
                        if self.type == "sort":
                            if hasattr(self.selected, "dir"):
                                self.selected.dir = not self.selected.dir
                                return True
                        else:
                            self.selected = "Untitled"
                            return True
        else:
            if pygame.Rect(*self.pop_loc, *self.pop_size).collidepoint(mx, my) and self.popped:
                for i in range(len(self.choices)):
                    y = i * self.textbox_size[1] + self.slider_y
                    if pygame.Rect(self.pop_loc[0], y + self.pop_loc[1], *self.textbox_size).collidepoint(mx, my):
                        for event in events:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    self.selected = self.choices[i]
                                    self.popped = False
                                    return True
                                if event.button == 3:
                                    if self.type == "sort":
                                        self.choices[i].dir = not self.choices[i].dir
                                        if self.selected == self.choices[i]:
                                            return True
                                    else:
                                        return self.choices.pop(i)

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.popped = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(*self.pop_loc, *self.pop_size).collidepoint(mx, my) and self.popped:
                    if event.button == 4:
                        self.slider_y += self.sensitivity
                    if event.button == 5:
                        self.slider_y -= self.sensitivity
                self.slider_y = min(self.slider_y, 0)
                self.slider_y = max(self.slider_y, -self.textbox_size[1]*(len(self.choices)-self.view))
    
    def clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(self.loc + self.size).collidepoint(event.pos):
                    return True
                if self.popped:
                    return pygame.Rect(self.pop_loc + self.pop_size).collidepoint(event.pos)

        return False


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
    
    def clicked(self, events):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
        return False


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
                    return True

    def draw(self, window):
        text_surf = pygame.font.SysFont("comicsans", self.height - 8).render(self.text, 1, WHITE)
        pygame.draw.rect(window, WHITE, (self.x, self.y, self.width, self.height), 5, 1)
        if self.checked:
            window.blit(self.surf, (self.x, self.y))
        window.blit(text_surf, (self.x + self.width + 8, self.y + self.height/2 - text_surf.get_height()/2))
    
    def clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(event.pos):
                    return True


class Slider:
    def __init__(self, loc, size, circle_size, font, label, default_val, val_range):
        self.loc = loc
        self.size = size
        self.circle_size = circle_size
        self.font = font
        self.label = label
        self.value = default_val
        self.range = val_range
        self.dragging = False

    def update(self, window, events):
        self.draw(window)
        mx, my = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.loc[0] <= mx <= self.loc[0]+self.size[0] and self.loc[1] <= my <= self.loc[1]+self.size[1]:
                    self.dragging = True

        clicking = pygame.mouse.get_pressed()[0]
        if not clicking:
            self.dragging = False

        if clicking and self.dragging:
            self.value = self.loc_to_value(mx)
    
    def draw(self, window):
        text = self.font.render(f"{self.label}: {self.value}", 1, WHITE)
        text_loc = (self.loc[0] + (self.size[0]-text.get_width())//2, self.loc[1]+self.size[1]+7)
        pygame.draw.rect(window, GREY, tuple(self.loc)+tuple(self.size))
        pygame.draw.circle(window, WHITE, (self.value_to_loc(), self.loc[1]+self.size[1]//2), self.circle_size)
        window.blit(text, text_loc)

    def loc_to_value(self, x):
        return int(np.interp(x, (self.loc[0], self.loc[0] + self.size[0]), self.range))

    def value_to_loc(self):
        return int(np.interp(self.value, self.range, (self.loc[0], self.loc[0] + self.size[0])))


class TextInput:
    def __init__(self,
                 loc,
                 size,
                 bg_col,
                 border_width=5,
                 border_col=(0, 0, 0),
                 initial_text="",
                 label="",
                 font=pygame.font.SysFont("comicsans", 35),
                 text_col=(0, 0, 0),
                 cursor_col=(0, 0, 1),
                 repeat_initial=400,
                 repeat_interval=35,
                 max_len=-1,
                 password=False,
                 editing=False):

        self.password_field = password

        self.loc, self.size = loc, size

        self.editing = editing

        self.text_col = text_col
        self.password = password
        self.text = initial_text
        self.label = label
        self.max_len = max_len

        self.rect = pygame.Rect(*loc, *size)
        self.bg_col = bg_col
        self.border_col, self.border_width = border_col, border_width

        self.font = font

        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        self.key_repeat_counters = {}
        self.key_repeat_initial = repeat_initial
        self.key_repeat_interval = repeat_interval

        self.cursor_surf = pygame.Surface(
            (int(font.get_height() / 20 + 1), font.get_height()))
        self.cursor_surf.fill(cursor_col)
        self.cursor_pos = len(initial_text)
        self.cursor_visible = True
        self.cursor_switch = 500
        self.cursor_counter = 0

        self.clock = pygame.time.Clock()

    def draw(self, window, events):
        pygame.draw.rect(window, self.bg_col, self.rect)
        if self.border_width:
            pygame.draw.rect(window, self.border_col,
                             self.rect, self.border_width)

        text_pos = (int(self.loc[0] + self.size[0]//2 - self.surface.get_width()/2),
                   int(self.loc[1] + self.size[1]//2 - self.surface.get_height()/2))
        window.blit(self.surface, text_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.editing = True
                else:
                    self.editing = False

            if not self.text:
                self.password = False
                self.text = self.label

            if self.editing and self.text == self.label:
                self.clear_text()
                self.password = True if self.password_field else False

            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True

                if event.key not in self.key_repeat_counters:
                    if not event.key == pygame.K_RETURN:
                        self.key_repeat_counters[event.key] = [0, event.unicode]

                if self.editing:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = (
                                self.text[:max(self.cursor_pos - 1, 0)]
                            + self.text[self.cursor_pos:]
                        )

                        self.cursor_pos = max(self.cursor_pos - 1, 0)
                    elif event.key == pygame.K_DELETE:
                        self.text = (
                                self.text[:self.cursor_pos]
                            + self.text[self.cursor_pos + 1:]
                        )

                    elif event.key == pygame.K_RETURN:
                        return True

                    elif event.key == pygame.K_RIGHT:
                        self.cursor_pos = min(
                            self.cursor_pos + 1, len(self.text))

                    elif event.key == pygame.K_LEFT:
                        self.cursor_pos = max(self.cursor_pos - 1, 0)

                    elif event.key == pygame.K_END:
                        self.cursor_pos = len(self.text)

                    elif event.key == pygame.K_HOME:
                        self.cursor_pos = 0

                    elif len(self.text) < self.max_len or self.max_len == -1:
                        self.text = (
                                self.text[:self.cursor_pos]
                            + event.unicode
                            + self.text[self.cursor_pos:]
                        )
                        self.cursor_pos += len(event.unicode)

            elif event.type == pygame.KEYUP:
                if event.key in self.key_repeat_counters:
                    del self.key_repeat_counters[event.key]

        for key in self.key_repeat_counters:
            self.key_repeat_counters[key][0] += self.clock.get_time()

            if self.key_repeat_counters[key][0] >= self.key_repeat_initial:
                self.key_repeat_counters[key][0] = (
                    self.key_repeat_initial
                    - self.key_repeat_interval
                )

                event_key, event_unicode = key, self.key_repeat_counters[key][1]
                pygame.event.post(pygame.event.Event(
                    pygame.KEYDOWN, key=event_key, unicode=event_unicode))

        string = self.text
        if self.password:
            string = "*" * len(self.text)
        if self.text:
            self.surface = self.font.render(str(string), 1, self.text_col)
        else:
            self.surface = pygame.Surface(self.cursor_surf.get_size(), pygame.SRCALPHA)
            self.surface.fill((0, 0, 0, 0))

        self.cursor_counter += self.clock.get_time()
        if self.cursor_counter >= self.cursor_switch:
            self.cursor_counter %= self.cursor_switch
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_y = self.font.size(self.text[:self.cursor_pos])[0]
            if self.cursor_pos > 0:
                cursor_y -= self.cursor_surf.get_width()
            if self.editing:
                self.surface.blit(self.cursor_surf, (cursor_y, 0))

        self.clock.tick()
        return False

    def get_cursor_pos(self):
        return self.cursor_pos

    def set_text_color(self, color):
        self.text_col = color

    def set_cursor_color(self, color):
        self.cursor_surf.fill(color)

    def clear_text(self):
        self.text = ""
        self.cursor_pos = 0
    
    def clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return self.rect.collidepoint(event.pos)

        return False 

    def __repr__(self):
        return self.text


class PlayButton:
    width = height = 80
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.pause_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.play_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.status = False
        self.create_surfs()
    
    def create_surfs(self):
        # pause
        self.pause_surf.fill((0, 0, 0, 0))
        pygame.draw.rect(self.pause_surf, WHITE, (10, 10, 25, 60))
        pygame.draw.rect(self.pause_surf, WHITE, (45, 10, 25, 60))

        # play
        self.play_surf.fill((0, 0, 0, 0))
        pygame.draw.polygon(self.play_surf, WHITE, ((15, 15), (65, 40), (15, 65)))
    
    def update(self, window, events):
        color = (0, 0, 0)
        if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(pygame.mouse.get_pos()):
            color = (80, 80, 80)
        
        if self.clicked(events):
            self.status = not self.status

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.status = not self.status

        self.draw(window, color)
    
    def draw(self, window, color):
        pygame.draw.rect(window, color, (self.x, self.y, self.width, self.height))
        window.blit(self.pause_surf if self.status else self.play_surf, (self.x, self.y))
    
    def clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(event.pos):
                    return True


class ColorPicker:
    def __init__(self, wheel_pos, wheel_rad, slider_pos, slider_size, slider_horiz, slider_invert, cursor_rad, display_rect_loc, display_rect_size, start):
        self.wheel_pos, self.wheel_rad = list(wheel_pos), wheel_rad
        self.slider_pos, self.slider_size, self.slider_horiz, self.slider_invert = list(slider_pos), slider_size, slider_horiz, slider_invert
        self.cursor_rad = cursor_rad
        self.display_rect_loc, self.display_rect_size = display_rect_loc, display_rect_size
        self.start = start
        self.set_wheel_cursor()
        self.set_slider_cursor()
        self.slider_surf = pygame.Surface(slider_size)
        self.wheel_surf = pygame.transform.scale(pygame.image.load(os.path.join(os.path.realpath(os.path.dirname(__file__)), "assets", "color_picker.png")), (wheel_rad * 2,) * 2)
        self.cursor_surf = pygame.Surface((self.cursor_rad*2,)*2, pygame.SRCALPHA)
        self.wheel_darken = pygame.Surface((wheel_rad * 2,) * 2, pygame.SRCALPHA)
        self._create_wheel()
        self._create_slider()
        self.update_wheel()
    
    def set_wheel_cursor(self):
        if self.start is None:
            self.wheel_cursor = np.array((self.wheel_rad,)*2)
        elif self.start == "red":
            self.wheel_cursor = np.array((self.wheel_rad, self.wheel_rad*2-2))

    def set_slider_cursor(self):
        if self.start is None:
            self.slider_cursor = np.array((self.slider_size[0]//2, self.slider_size[1]//2))
        elif self.start == "red":
            self.slider_cursor = np.array((self.slider_size[0]//2, 1))

    def draw(self, window):
        pygame.draw.rect(window, self.get_rgb(), (*self.display_rect_loc, *self.display_rect_size))
        window.blit(self.slider_surf, self.slider_pos)
        self._draw_cursor(window, np.array(self.slider_pos) + np.array(self.slider_cursor))
        window.blit(self.wheel_surf, self.wheel_pos)
        window.blit(self.wheel_darken, self.wheel_pos)
        self._draw_cursor(window, np.array(self.wheel_pos) + np.array(self.wheel_cursor))

    def update(self, window):
        self.draw(window)
        if any(pygame.mouse.get_pressed()):
            x, y = pygame.mouse.get_pos()
            if ((self.wheel_pos[0] + self.wheel_rad - x) ** 2 + (self.wheel_pos[1] + self.wheel_rad - y) ** 2)**0.5 < self.wheel_rad - 2:
                if pygame.mouse.get_pressed()[0]:
                    self.wheel_cursor = (x - self.wheel_pos[0], y - self.wheel_pos[1])
                else:
                    self.set_wheel_cursor()
                return True
            elif self.slider_pos[0] < x < self.slider_pos[0] + self.slider_size[0] and self.slider_pos[1] < y < self.slider_pos[1] + self.slider_size[1]:
                if pygame.mouse.get_pressed()[0]:
                    self.slider_cursor[1] = (y - self.slider_pos[1])*((self.slider_size[1]-1)/self.slider_size[1])
                else:
                    self.set_slider_cursor()
                self.update_wheel()
                return True

    def get_rgb(self):
        wrgb = self.wheel_surf.get_at(self.wheel_cursor)
        srgb = self.slider_surf.get_at(self.slider_cursor)
        whsv = rgb_to_hsv(*(np.array(wrgb)/255)[:3])
        shsv = rgb_to_hsv(*(np.array(srgb)/255)[:3])
        hsv = (whsv[0], whsv[1], shsv[2])
        rgb = np.array(hsv_to_rgb(*hsv))*255
        return rgb

    def get_hsv(self):
        rgb = (np.array(self.get_rgb())/255)[:3]
        return np.array(rgb_to_hsv(*rgb))*255

    def update_wheel(self):
        pygame.draw.circle(self.wheel_darken, (0, 0, 0, np.interp(self.get_hsv()[2], (0, 255), (255, 0))), (self.wheel_rad,)*2, self.wheel_rad)

    def _create_wheel(self):
        return

    def _create_slider(self):
        w, h = self.slider_size
        if self.slider_horiz:
            for x in range(w):
                if self.slider_invert:
                    value = np.interp(x, (0, w), (0, 255))
                else:
                    value = np.interp(x, (0, w), (255, 0))
                pygame.draw.rect(self.slider_surf, (value,)*3, (x, 0, 1, h))

        else:
            for y in range(h):
                if self.slider_invert:
                    value = np.interp(y, (0, h), (0, 255))
                else:
                    value = np.interp(y, (0, h), (255, 0))
                pygame.draw.rect(self.slider_surf, (value,)*3, (0, y, w, 1))
        pygame.draw.rect(self.slider_surf, (255, 255, 255), (0, 0, w, h), 1)

    def _draw_cursor(self, window, pos):
        pygame.draw.circle(window, (255, 255, 255), pos, self.cursor_rad)
        pygame.draw.circle(window, (0, 0, 0), pos, self.cursor_rad, 2)
