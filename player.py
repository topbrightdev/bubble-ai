from weapon import *
import copy
from copy import *


class Player(pygame.sprite.Sprite):
    """
    a class representing a player object
    """
    def __init__(self, image_name='player.png'):
        """
        creates a new player with the given image
        :param image_name:
        """
        self.image = pygame.image.load(IMAGES_PATH + image_name)
        self.rect = self.image.get_rect()
        self.weapon = Weapon()
        self.moving_left = False
        self.moving_right = False
        self.is_shoot = False
        self.lives = STARTING_LIVES
        self.set_position()
        self.is_alive = True

    def __eq__(self, other):
        """
        compares two players. returns True if players are identical an False otherwise
        :param other:
        :return:
        """
        if self.rect.centerx == other.rect.centerx:
            if self.is_shoot == other.is_shoot:
                if self.weapon == other.weapon:
                    return True
        return False

    def shoot(self):
        """
        shoots if there is no other shots on the screen
        :return:
        """
        self.weapon = Weapon(self.rect.centerx, self.rect.top)
        self.weapon.is_active = True

    def update(self):
        """
        updates players location
        :return:
        """
        if self.moving_left and self.rect.left >= 0:
            self.rect = self.rect.move(-PLAYER_SPEED, 0)
        if self.moving_right and self.rect.right <= WINDOWWIDTH:
            self.rect = self.rect.move(PLAYER_SPEED, 0)
        if self.weapon.is_active:
            self.weapon.update()

    def set_position(self, x=WINDOWWIDTH/2, y=WINDOWHEIGHT):
        """
        sets player's position on the screen. default position is the middle of X axis
        :param x:
        :param y:
        :return:
        """
        self.rect.centerx, self.rect.bottom = x, y
        self.weapon.is_active = False

    def deep_copy_player(self):
        """
        :return: a deep copy of the given player object
        """
        player_copy = Player()
        player_copy.image = self.image
        player_copy.rect = deepcopy(player_copy.rect)
        player_copy.set_position(self.rect.centerx, self.rect.bottom)

        player_copy.weapon = self.weapon.deep_copy_weapon()
        player_copy.lives = self.lives
        player_copy.is_alive = self.is_alive

        return player_copy
