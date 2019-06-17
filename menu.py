import pygame

from settings import *


class MenuOption (pygame.font.Font):
    def __init__(self, text, function,
                 position=(0, 0), font=None, font_size=36, font_color=WHITE):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.function = function
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, font_color)
        self.rect = self.label.get_rect(left=position[0], top=position[1])
        self.position = position
        self.is_selected = False

    def set_position(self, x, y):
        self.position = (x, y)
        self.rect = self.label.get_rect(left=x, top=y)

    def highlight(self, color=RED):
        self.font_color = color
        self.label = self.render(self.text, 1, self.font_color)
        self.is_selected = True

    def unhighlight(self):
        self.font_color = WHITE
        self.label = self.render(self.text, 1, self.font_color)
        self.is_selected = False

    def check_for_mouse_selection(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.highlight()
        else:
            self.unhighlight()


class Menu():
    def __init__(self, screen, functions, bg_color=BLACK):
        self.is_active = True
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.bg_color = bg_color
        self.options = []
        self.current_option = None
        self.functions = functions
        for index, option in enumerate(functions.keys()):
            menu_option = MenuOption(option, functions[option])
            width = menu_option.rect.width
            height = menu_option.rect.height
            total_height = len(functions) * height
            pos_x = self.scr_width/2 - width/2
            pos_y = self.scr_height/2 - total_height/2 + index*height
            if menu_option.text == 'Back':
                menu_option.set_position(20, self.scr_height - 40)
            else:
                menu_option.set_position(pos_x, pos_y)
            self.options.append(menu_option)

    def draw(self):
        self.screen.fill(self.bg_color)
        for option in self.options:
            option.check_for_mouse_selection(pygame.mouse.get_pos())
            if self.current_option is not None:
                self.options[self.current_option].highlight()
            self.screen.blit(option.label, option.position)