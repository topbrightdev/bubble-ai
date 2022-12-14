import pygame
import copy

from settings import *


class Bubble(pygame.sprite.Sprite):
    """
    an object that needs to be blown up by the player. bubbles move in a certain way and when blown up they split into 2
    smaller bubbles (unless they are of minimal size)
    """
    def __init__(self, x, y, size, speed, image_name):
        """
        :param x:
        :param y:
        :param size:
        :param speed:
        :param image_name:
        """
        pygame.sprite.Sprite.__init__(self)
        self.image_name = image_name
        self.image = pygame.image.load(IMAGES_PATH + image_name)
        self.image = pygame.transform.scale(self.image, (size*15, size*15))
        self.rect = self.image.get_rect(centerx=x, centery=y)
        self.size = size
        self.speed = speed

    def update(self):
        """
        updates the movement of a bubble according to it's type, current position and speed

        """
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > WINDOWWIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > WINDOWHEIGHT:
            if self.image_name == BALL_IMAGE_NAME:
                self.speed[1] = - min(3 * (self.size+5), 27)
            else:
                self.speed[1] = -self.speed[1]
        self.rect.left = self._clip(self.rect.left, 0, WINDOWWIDTH)
        self.rect.right = self._clip(self.rect.right, 0, WINDOWWIDTH)
        self.rect.top = self._clip(self.rect.top, 0, WINDOWHEIGHT)
        self.rect.bottom = self._clip(self.rect.bottom, 0, WINDOWHEIGHT)

    @staticmethod
    def _clip(val, min_value, max_value):
        """
        :param val:
        :param min_value:
        :param max_value:
        :return: val clipped so it'll be <= max_value and >= min_value
        """
        return min(max(val, min_value), max_value)


class Ball(Bubble):
    """
    a ball object
    """
    def __init__(self, x, y, size, speed):
        """
        :param x:
        :param y:
        :param size:
        :param speed:
        creates a new ball object with location (x,y), and the given speed and size.
        """
        Bubble.__init__(self, x, y, size, speed, BALL_IMAGE_NAME)

    def update(self):
        """
        the new location of the ball
        :return:
        """
        self.speed[1] += GRAVITY
        Bubble.update(self)

    def deep_copy_bubble(self):
        """
        :return: a deep copy of the ball
        """
        speed = copy.deepcopy(self.speed)
        return Ball(self.rect.centerx, self.rect.centerx, self.size, speed)


class Hexagon(Bubble):
    """ a hexagon object"""
    def __init__(self, x, y, size, speed):
        """
        :param x:
        :param y:
        :param size:
        :param speed:
        creates a new hexagon object with location (x,y), and the given speed and size.
        """
        Bubble.__init__(self, x, y, size, speed, HEXAGON_IMAGE_NAME)

    def deep_copy_bubble(self):
        """
        :return: a deep copy of the hexagon
        """
        speed = copy.deepcopy(self.speed)
        return Hexagon(self.rect.centerx, self.rect.centerx, self.size, speed)
