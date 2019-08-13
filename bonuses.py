import pygame

from settings import *

BONUS_LIFE = 'bonus life'
BONUS_TIME = 'bonus time'

bonus_types = [BONUS_LIFE, BONUS_TIME]


class Bonus(pygame.sprite.Sprite):
    """
    this class represents a bonus in the game. a bonus can be dropped to the ground when a bubble is blown up. the
    player can take it and get extra life\time
    """
    def __init__(self, x, y, type):
        """
        :param x: x axis location
        :param y: y axis location
        :param type: 'bonus life' or 'bonus time'
        """
        self.image = pygame.image.load(IMAGES_PATH + type + '.png')
        self.rect = self.image.get_rect(centerx=x, centery=y)
        self.type = type

    def update(self):
        """
        moves the bonus down if the it didn't get to the floor yet
        """
        if self.rect.bottom < WINDOWHEIGHT:
            self.rect = self.rect.move(0, BONUS_SPEED)

    def deep_copy_bonus(self):
        """
        :return: a deepcopy
        """
        return Bonus(self.rect.centerx, self.rect.centery, self.type)
