import pygame

from settings import *

BONUS_LIFE = 'bonus life'
BONUS_TIME = 'bonus time'

bonus_types = [BONUS_LIFE, BONUS_TIME]


class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        self.image = pygame.image.load(IMAGES_PATH + type + '.png')
        self.rect = self.image.get_rect(centerx=x, centery=y)
        self.type = type

    def update(self):
        if self.rect.bottom < WINDOWHEIGHT:
            self.rect = self.rect.move(0, BONUS_SPEED)