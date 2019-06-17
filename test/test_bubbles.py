import unittest

from bubbles import *
from bonuses import *


class BubbleTest(unittest.TestCase):
    def setUp(self):
        self.ball = Ball(200, 200, 3, [3, 5])
        self.hexagon = Hexagon(250, 250, 2, [4, 4])

    def test_ball_has_image(self):
        self.assertIsNotNone(self.ball.image, 'Ball has no image')

    def test_hex_has_image(self):
        self.assertIsNotNone(self.hexagon.image, 'Hexagon has no image')

    @staticmethod
    def move_bubble(bubble):
        bubble.update()
        end_rect = bubble.rect
        return end_rect

    def test_ball_movement(self):
        start_rect = self.ball.rect
        end_rect = self.move_bubble(self.ball)
        self.assertEqual(start_rect.move(self.ball.speed), end_rect)

    def test_hex_movement(self):
        start_rect = self.hexagon.rect
        end_rect = self.move_bubble(self.hexagon)
        self.assertEqual(start_rect.move(self.hexagon.speed), end_rect)


class BonusTest(unittest.TestCase):
    def setUp(self):
        self.life_bonus = Bonus(20, 20, BONUS_LIFE)
        self.time_bonus = Bonus(10, 10, BONUS_TIME)

    def test_life_bonus_has_image(self):
        self.assertIsNotNone(self.life_bonus.image, 'Ball has no image')

    def test_time_bonus_has_image(self):
        self.assertIsNotNone(self.time_bonus.image, 'Hexagon has no image')

    def test_bonus_movement(self):
        start_rect = self.life_bonus.rect
        end_rect = BubbleTest.move_bubble(self.life_bonus)
        self.assertEqual(start_rect.move([0, BONUS_SPEED]), end_rect)

# if __name__ == '__main__':
#     unittest.main()
