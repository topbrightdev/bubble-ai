import unittest

from game import *


class GameEngineTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        ball = Ball(50, WINDOWHEIGHT - 20, 2, [0, 3])
        self.game.balls.append(ball)
        hex = Hexagon(20, WINDOWHEIGHT - 20, 2, [3, 3])
        self.game.hexagons.append(hex)

    @staticmethod
    def load_bubble(bubble):
        bubble_properties = {}
        bubble_properties['x'] = bubble.rect.centerx
        bubble_properties['y'] = bubble.rect.centery
        bubble_properties['size'] = bubble.size
        bubble_properties['speed'] = bubble.speed
        return bubble_properties

    def test_load_level(self):
        self.game.load_level(1)
        with open(APP_PATH + 'levels.json', 'r') as levels_file:
            levels = json.load(levels_file)
            level = levels[str(self.game.level)]
        self.assertEqual(self.game.time_left, level['time'])
        for ball_index, ball in enumerate(self.game.balls):
            ball_properties = self.load_bubble(ball)
            self.assertEqual(ball_properties, level['balls'][ball_index])
        for hex_index, hex in enumerate(self.game.hexagons):
            hex_properties = self.load_bubble(hex)
            self.assertEqual(hex_properties, level['balls'][hex_index])

    def test_bubble_collision(self):
        ball_rect = self.game.balls[0].rect
        ball_center_x, ball_center_y = ball_rect.centerx, ball_rect.centery
        self.game.players[0].set_position(ball_center_x)
        self.assertTrue(self.game._check_for_bubble_collision(
            self.game.balls, True, self.game.players[0])
        )
        self.game.players[0].set_position(ball_center_x - ball_rect.width)
        self.assertFalse(self.game._check_for_bubble_collision(
            self.game.balls, True, self.game.players[0])
        )
        self.assertTrue(self.game._check_for_bubble_collision(
            self.game.hexagons, False, self.game.players[0])
        )
        self.game.players[0].weapon = Weapon(ball_center_x, ball_center_y)
        self.game.players[0].weapon.is_active = True
        self.assertTrue(self.game._check_for_bubble_collision(
            self.game.balls, True, self.game.players[0])
        )
        self.game.players[0].weapon = Weapon(
            ball_center_x, ball_center_y + ball_rect.height
        )
        self.game.players[0].weapon.is_active = True
        self.assertFalse(self.game._check_for_bubble_collision(
            self.game.balls, True, self.game.players[0])
        )

    def test_split_ball(self):
        start_num_balls = len(self.game.balls)
        start_ball_size = self.game.balls[0].size
        self.game._split_ball(0)
        self.assertEqual(len(self.game.balls), start_num_balls + 1)
        self.assertEqual(self.game.balls[0].size, start_ball_size - 1)
        self.assertEqual(self.game.balls[1].size, start_ball_size - 1)

    def test_split_hexagon(self):
        start_num_hexes = len(self.game.balls)
        start_hex_size = self.game.hexagons[0].size
        self.game._split_hexagon(0)
        self.assertEqual(len(self.game.hexagons), start_num_hexes + 1)
        self.assertEqual(self.game.hexagons[0].size, start_hex_size - 1)
        self.assertEqual(self.game.hexagons[1].size, start_hex_size - 1)

    def test_level_completed(self):
        while self.game.balls:
            for ball_index in range(len(self.game.balls)):
                self.game._split_ball(ball_index)
                return
        while self.game.hexagons:
            for hex_index in range(len(self.game.balls)):
                self.game._split_hexagon(hex_index)
                return
        self.game.update()
        self.assertTrue(self.game.level_completed)

    def test_decrease_lives(self):
        startLives = self.game.players[0].lives
        self.game._decrease_lives(self.game.players[0])
        self.assertEqual(self.game.players[0].lives, startLives - 1)

    def test_player_dies(self):
        player = self.game.players[0]
        ballRect = self.game.balls[0].rect
        ball_center_x, ball_center_y = ballRect.centerx, ballRect.centery
        self.game.players[0].set_position(ball_center_x, WINDOWHEIGHT)
        self.game._check_for_bubble_collision(
            self.game.balls, True, self.game.players[0]
        )
        self.assertFalse(player.is_alive)
        self.assertTrue(self.game.dead_player)

    def test_game_over(self):
        player = self.game.players[0]
        player.lives = 1
        self.game._decrease_lives(player)
        self.assertTrue(self.game.game_over)

    def test_game_completed(self):
        max_level_available = self.game.max_level_available
        self.game.load_level(self.game.max_level)
        self.game.balls = []
        self.game.hexagons = []
        self.game.update()
        self.assertTrue(self.game.is_completed)
        with open('max_level_available', 'w') as max_completed_level_file:
            max_completed_level_file.write(str(max_level_available))

    def test_tick_second(self):
        self.game.load_level(1)
        start_time = self.game.time_left
        self.game._tick_second()
        self.assertEqual(self.game.time_left, start_time - 1)

    def test_max_level_available_file_read(self):
        with open('max_level_available', 'r') as max_completed_level_file:
            max_level_available = max_completed_level_file.read()
            if max_level_available:
                max_level_available = int(max_level_available)
            else:
                max_level_available = 1
            self.assertEqual(max_level_available,
                             self.game.max_level_available)

    def test_activate_bonus_life(self):
        player = self.game.players[0]
        start_lives = player.lives
        self.game._activate_bonus(BONUS_LIFE, player)
        end_lives = player.lives
        self.assertEqual(start_lives + 1, end_lives)

    def test_activate_bonus_time(self):
        self.game.load_level(1)
        start_time_left = self.game.time_left
        self.game._activate_bonus(BONUS_TIME, self.game.players[0])
        end_time_left = self.game.time_left
        self.assertEqual(start_time_left + 10, end_time_left)

    def test_bonus_collision(self):
        bonus = Bonus(50, WINDOWHEIGHT, BONUS_LIFE)
        self.game.bonuses.append(bonus)
        self.game.players[0].set_position(50)
        self.assertTrue(
            self.game._check_for_bonus_collision(self.game.players[0])
        )
        self.game.players[0].set_position(50 - bonus.rect.width/2)
        self.assertFalse(
            self.game._check_for_bonus_collision(self.game.players[0])
        )

    def test_multiplayer(self):
        self.game.is_multiplayer = True
        self.game.load_level(1)
        self.assertEqual(len(self.game.players), 2)
        self.assertIsNotNone(self.game.players[1].image)

# if __name__ == '__main__':
#     unittest.main()
