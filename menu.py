import pygame

from settings import *
import copy
from copy import *


class MenuOption (pygame.font.Font):
    """
    a MenuOption object class
    """
    def __init__(self, text, function,
                 position=(0, 0), font=None, font_size=36, font_color=WHITE):
        """
        constructs a new menu option class with the given arguments
        :param text:
        :param function:
        :param position:
        :param font:
        :param font_size:
        :param font_color:
        """
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
        """
        sets the position of the menu option
        :param x:
        :param y:
        :return:
        """
        self.position = (x, y)
        self.rect = self.label.get_rect(left=x, top=y)

    def highlight(self, color=RED):
        """
        highlights the given menu option in given color
        :param color:
        :return:
        """
        self.font_color = color
        self.label = self.render(self.text, 1, self.font_color)
        self.is_selected = True

    def unhighlight(self):
        """
        stop highliighting given menu option
        :return:
        """
        self.font_color = WHITE
        self.label = self.render(self.text, 1, self.font_color)
        self.is_selected = False

    def check_for_mouse_selection(self, mouse_pos):
        """
        if mouse is  hovering over the menu option, highight it. otherwis, don't
        :param mouse_pos:
        :return:
        """
        if self.rect.collidepoint(mouse_pos):
            self.highlight()
        else:
            self.unhighlight()


class Menu():
    """
    the main menu of the game
    """
    def __init__(self, screen, functions, bg_color=BLACK, image_name='1_bubble_trouble.png'):
        """
        creates a new main menu with given arguments
        :param screen:
        :param functions:
        :param bg_color:
        :param image_name:
        """
        self.is_active = True
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        # self.bg_color = bg_color
        self.image = pygame.image.load(IMAGES_PATH + image_name)
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
        """
        draws the main menu
        :return:
        """
        #self.screen.fill(self.image)
        self.screen.blit(self.image,(0,0))
        for option in self.options:
            option.check_for_mouse_selection(pygame.mouse.get_pos())
            if self.current_option is not None:
                self.options[self.current_option].highlight()
            self.screen.blit(option.label, option.position)