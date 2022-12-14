import pygame
from settings import *
import copy
from copy import *


class Weapon(pygame.sprite.Sprite):
    """ a class representing a player's weapon"""
    def __init__(self, x=0, y=0):
        self.is_active = False
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(IMAGES_PATH + 'arrow.png')
        self.rect = self.image.get_rect(centerx=x, top=y)

    def __eq__(self, other):
        """
        comperator
        :param other:
        :return: True if weapons are identical and False otherwise.
        """
        return self.rect.centerx == other.rect.centerx and self.rect.top == other.rect.top

    def update(self):
        """
        updates the location and activeness of the weapon object
        :return:
        """
        if self.is_active:
            if self.rect.top <= 0:
                self.is_active = False
            else:
                self.rect = self.rect.move(0, -WEAPON_SPEED)

    def deep_copy_weapon(self):
        """

        :return: a deep copy of the given weapon
        """
        copy_weapon = Weapon(self.rect.centerx, self.rect.top)
        copy_weapon.is_active = self.is_active
        return copy_weapon
