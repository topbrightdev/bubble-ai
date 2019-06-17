from weapon import *


class Player(pygame.sprite.Sprite):

    def __init__(self, image_name='player.png'):
        self.image = pygame.image.load(IMAGES_PATH + image_name)
        self.rect = self.image.get_rect()
        self.weapon = Weapon()
        self.moving_left = False
        self.moving_right = False
        self.lives = STARTING_LIVES
        self.set_position()
        self.is_alive = True

    def shoot(self):
        self.weapon = Weapon(self.rect.centerx, self.rect.top)
        self.weapon.is_active = True

    def update(self):
        if self.moving_left and self.rect.left >= 0:
            self.rect = self.rect.move(-PLAYER_SPEED, 0)
        if self.moving_right and self.rect.right <= WINDOWWIDTH:
            self.rect = self.rect.move(PLAYER_SPEED, 0)
        if self.weapon.is_active:
            self.weapon.update()

    def set_position(self, x=WINDOWWIDTH/2, y=WINDOWHEIGHT):
        self.rect.centerx, self.rect.bottom = x, y
        self.weapon.is_active = False
