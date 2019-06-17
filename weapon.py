import pygame
from settings import *


class Weapon(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0):
        self.is_active = False
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(IMAGES_PATH + 'arrow.png')
        self.rect = self.image.get_rect(centerx=x, top=y)

    def update(self):
        if self.is_active:
            if self.rect.top <= 0:
                self.is_active = False
            else:
                self.rect = self.rect.move(0, -WEAPON_SPEED)
