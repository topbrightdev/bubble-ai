import unittest
from player import *


class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_player_has_image(self):
        self.assertIsNotNone(self.player.image,
                             'Player does not have an image')

    def test_player_weapon_has_image(self):
        self.assertIsNotNone(self.player.weapon.image,
                             'Player\'s weapon does not have an image')

    def test_player_movement(self):
        start_player_x = self.player.rect.centerx
        self.player.moving_right = True
        self.player.update()
        self.assertEqual(
            start_player_x + PLAYER_SPEED,
            self.player.rect.centerx, 'Player moving right is wrong'
        )
        self.player.moving_right = False
        self.player.moving_left = True
        start_player_x = self.player.rect.centerx
        self.player.update()
        self.assertEqual(
            start_player_x - PLAYER_SPEED,
            self.player.rect.centerx, 'Player moving left is wrong'
        )
        self.player.moving_left = False
        start_player_x = self.player.rect.centerx
        self.player.update()
        self.assertEqual(start_player_x, self.player.rect.centerx,
                         'Player should not have moved')

    def test_player_reset_position(self):
        self.player.rect.move(10, 0)
        self.player.set_position()
        self.assertEqual((self.player.rect.centerx, self.player.rect.bottom),
                         (WINDOWWIDTH / 2, WINDOWHEIGHT))

    def test_player_shoots(self):
        self.player.shoot()
        self.assertIsNotNone(self.player.weapon)
        weapon_rect = self.player.weapon.rect
        player_rect = self.player.rect
        self.assertEqual((weapon_rect.centerx, weapon_rect.top),
                         (player_rect.centerx, player_rect.top))

    def test_player_weapon_movement(self):
        self.player.shoot()
        start_weapon_x, start_weapon_y = \
            self.player.weapon.rect.centerx, self.player.weapon.rect.top
        self.player.weapon.update()
        end_weapon_x, end_weapon_y = \
            self.player.weapon.rect.centerx, self.player.weapon.rect.top
        self.assertEqual(start_weapon_x, end_weapon_x)
        self.assertEqual(start_weapon_y, end_weapon_y + WEAPON_SPEED)

    def test_weapon_disappears(self):
        self.player.weapon = Weapon(WEAPON_SPEED - 1, self.player.rect.centerx)
        self.player.weapon.update()
        self.assertFalse(self.player.weapon.is_active)

# if __name__ == '__main__':
#     unittest.main()
