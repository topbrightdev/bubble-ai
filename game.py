import operator
import sys
from threading import Timer
import random
import json
import copy
import numpy as np

import heuristics
from bubbles import *
from player import *
from bonuses import *
from settings import *
import copy
from copy import *


class Game:
    """ stands for a bubble trouble game"""
    def __init__(self, level=1):
        """
        :param self:
        :param level: the starting level of the game
        :return:
        """
        self.score = 0
        self.g_score = np.inf
        self.h_score = np.inf
        self.balls = []
        self.hexagons = []
        self.players = [Player()]
        self.bonuses = []
        self.level = level
        self.game_over = False
        self.level_completed = False
        self.is_running = True
        self.is_completed = False
        self.max_level = MAX_LEVEL
        self.is_multiplayer = False
        self.is_ai = False
        self.is_nn = False
        self.is_restarted = False
        self.dead_player = False
        self.mode = 'Classic'
        with open(APP_PATH + 'max_level_available', 'r') as \
                max_completed_level_file:
            max_level_available = max_completed_level_file.read()
            if max_level_available:
                self.max_level_available = int(max_level_available)
            else:
                self.max_level_available = 1

    def __lt__(self, other):
        """
        compares two game objects (states) according to their F score
        :param self:
        :param other:
        :return:  True if f(self)<f(other), False if f(self)>f(other) and True or False rndomly if f(self)==f(other)
        """
        if bool(random.getrandbits(1)):
            return self.get_f_score() < other.get_f_score()
        else:
            return self.get_f_score() <= other.get_f_score()

    def check_if_equal(self, other):
        """
        compares two game objects (states) and checks if they are equal
        :param self:
        :param other:
        :return: True if states are equal, False otherwise
        """
        if self.get_time_left() == other.get_time_left():
            if len(self.balls) == len(other.balls) and len(self.hexagons) == len(other.hexagons):
                for player in self.players:
                    does_have_equal_player = False
                    for other_player in other.players:
                        if player == other_player:
                            does_have_equal_player = True
                            break
                    if not does_have_equal_player:
                        return False
                for bubble in self.balls:
                    does_have_equal_bubble = False
                    for other_bubble in other.balls:
                        if bubble == other_bubble:
                            does_have_equal_bubble = True
                            break
                    if not does_have_equal_bubble:
                        return False
                for bubble in self.hexagons:
                    does_have_equal_bubble = False
                    for other_bubble in other.hexagons:
                        if bubble == other_bubble:
                            does_have_equal_bubble = True
                            break
                    if not does_have_equal_bubble:
                        return False
                return True
        return False


    def add_to_score(self, to_add):
        """
        adds to_add to game's current score
        :param self:
        :param to_add: amount of points to be added to score
        :return:
        """
        self.score += to_add

    def get_score(self):
        """
        :param self:
        :return: game's current score
        """
        return int(self.score)

    def update_g_score(self, value):
        """
        sets the g score
        :param self:
        :param value:
        :return:
        """
        self.g_score = value

    def get_g_score(self):
        """
        :param self:
        :return: g score
        """
        return self.g_score

    def update_h_score(self, value):
        """
        sets h_score
        :param value:
        :return:
        """
        self.h_score = value

    def get_h_score(self):
        """
        :return: game's h score
        """
        return self.h_score

    def get_f_score(self):
        """
        :return: f score
        """
        return self.get_g_score() + self.get_h_score()

    def load_level(self, level):
        """
        :param level: level number
        :return:
        """
        self.is_restarted = True
        if self.is_multiplayer and len(self.players) == 1:
            self.players.append(Player('player2.png'))
        self.balls = []
        self.hexagons = []
        self.bonuses = []
        self.dead_player = False
        for index, player in enumerate(self.players):
            player_number = index + 1
            num_of_players = len(self.players)
            player.set_position(
                (WINDOWWIDTH / (num_of_players + 1)) * player_number
            )
            player.is_alive = True
        self.level_completed = False
        self.level = level
        if self.level > self.max_level_available:
            self.max_level_available = self.level
            with open(APP_PATH + 'max_level_available', 'w') as \
                    max_completed_level_file:
                max_completed_level_file.write(str(self.max_level_available))
        with open(APP_PATH + 'levels.json', 'r') as levels_file:
            levels = json.load(levels_file)
            level = levels[str(self.level)]
            self.time_left = level['time']
            for ball in level['balls']:
                x, y = ball['x'], ball['y']
                size = ball['size']
                speed = ball['speed']
                self.balls.append(Ball(x, y, size, speed))
            for hexagon in level['hexagons']:
                x, y = hexagon['x'], hexagon['y']
                size = hexagon['size']
                speed = hexagon['speed']
                self.hexagons.append(Hexagon(x, y, size, speed))

    def _check_for_collisions(self):
        """
        checks for collisions with bubbles or bonuses
        :return:
        """
        for player in self.players:
            self._check_for_bubble_collision(self.balls, True, player)
            self._check_for_bubble_collision(self.hexagons, False, player)
            self._check_for_bonus_collision(player)

    def _check_for_bubble_collision(self, bubbles, is_ball, player):
        for bubble_index, bubble in enumerate(bubbles):
            if pygame.sprite.collide_rect(bubble, player.weapon) \
                    and player.weapon.is_active:
                self.add_to_score(50)
                player.weapon.is_active = False
                if is_ball:
                    self._split_ball(bubble_index)
                else:
                    self._split_hexagon(bubble_index)
                return True
            if pygame.sprite.collide_mask(bubble, player):
                player.is_alive = False
                self._decrease_lives(player)
                return True
        return False

    def _check_for_bonus_collision(self, player):
        """
        checks if player caught a bonus
        :param player:
        :return: True if it did. False otherwise
        """
        for bonus_index, bonus in enumerate(self.bonuses):
            if pygame.sprite.collide_mask(bonus, player):
                self._activate_bonus(bonus.type, player)
                del self.bonuses[bonus_index]
                return True
        return False

    def _decrease_lives(self, player):
        """
        decrease players lives in 1. if player had 0 lives left, game is over
        :param player:
        :return:
        """
        player.lives -= 1
        if player.lives:
            self.dead_player = True
            player.is_alive = False
        else:
            self.game_over = True

    def _restart(self):
        """
        restarts game
        :return:
        """
        self.load_level(self.level)

    @staticmethod
    def _drop_bonus():
        """
        randomly drops a bonus, and randomly chooses bonus type
        :return: bonus type
        """
        if random.randrange(BONUS_DROP_RATE) == 0:
            bonus_type = random.choice(bonus_types)
            return bonus_type

    def _activate_bonus(self, bonus, player):
        """
        activates bonus
        :param bonus: bonus type
        :param player: the player that caught the bonus
        :return:
        """
        if bonus == BONUS_LIFE:
            player.lives += 1
        elif bonus == BONUS_TIME:
            self.time_left += 50

    def _split_ball(self, ball_index):
        """
        splits ball into to smaller balls
        :param ball_index:
        :return:
        """
        ball = self.balls[ball_index]
        if ball.size > 1:
            self.balls.append(Ball(
                ball.rect.left + ball.size,
                ball.rect.top - 10, ball.size - 1, [-3, -5])
            )
            self.balls.append(
                Ball(ball.rect.right - ball.size,
                     ball.rect.top - 10, ball.size - 1, [3, -5])
            )
        del self.balls[ball_index]
        bonus_type = self._drop_bonus()
        if bonus_type:
            bonus = Bonus(ball.rect.centerx, ball.rect.centery, bonus_type)
            self.bonuses.append(bonus)

    def _split_hexagon(self, hex_index):
        """
        splits hexagon into to smaller hexagons

        :param hex_index:
        :return:
        """
        hexagon = self.hexagons[hex_index]
        if hexagon.size > 1:
            self.hexagons.append(
                Hexagon(hexagon.rect.left + hexagon.size, hexagon.rect.centery,
                        hexagon.size - 1, [-3, -5]))
            self.hexagons.append(
                Hexagon(hexagon.rect.right - hexagon.size, hexagon.rect.centery,
                        hexagon.size - 1, [3, -5]))
        del self.hexagons[hex_index]
        bonus_type = self._drop_bonus()
        if bonus_type:
            bonus = Bonus(hexagon.rect.centerx, hexagon.rect.centery,
                          bonus_type)
            self.bonuses.append(bonus)

    def update(self, is_a_star=False):
        """
        updates the location and state of all
        :param is_a_star: True if updating as part of A* finding best steps or as part of the game itself
        :return: self
        """
        if self.level_completed or self.is_completed:
            self.add_to_score(TIME_LEFT_SCORE_FACTOR * self.get_time_left())
        if self.level_completed and not self.is_completed:
            self.load_level(self.level + 1)
        if self.game_over:
            self.is_running = False
            if not is_a_star:
                pygame.quit()
                sys.exit()
        if self.dead_player:
            self._restart()
        self._check_for_collisions()
        for ball in self.balls:
            ball.update()
        for hexagon in self.hexagons:
            hexagon.update()
        for player in self.players:
            player.update()
        for bonus in self.bonuses:
            bonus.update()
        if not self.balls and not self.hexagons:
            self.level_completed = True
            if self.level == self.max_level:
                self.is_completed = True
        self.tick_time_unit()

        return self

    def tick_time_unit(self):
        """
        adds 1 to the game's clock
        :return:
        """
        self.time_left -= TIME_UNIT
        if self.time_left <= 0:
            for player in self.players:
                self._decrease_lives(player)

    def get_time_left(self):
        """

        :return: time left to complete level
        """
        return int(np.ceil(self.time_left))

    def deep_copy_game(self):
        """

        :return: a deep copy of the game
        """
        game_copy = Game(level=self.level)

        game_copy.balls = []
        for ball in self.balls:
            game_copy.balls.append(ball.deep_copy_bubble())
        game_copy.hexagons = []
        for hexagon in self.hexagons:
            game_copy.hexagons.append(hexagon.deep_copy_bubble())

        game_copy.players = []
        for player in self.players:
            game_copy.players.append(player.deep_copy_player())

        game_copy.bonuses = []
        for bonus in self.bonuses:
            game_copy.bonuses.append(bonus.deep_copy_bonus())

        # copy fields
        game_copy.score = self.score
        game_copy.game_over = self.game_over
        game_copy.level_completed = self.level_completed
        game_copy.is_running = self.is_running
        game_copy.is_completed = self.is_completed
        game_copy.max_level = self.max_level
        game_copy.is_multiplayer = self.is_multiplayer
        game_copy.is_ai = self.is_ai
        game_copy.is_nn = self.is_nn
        game_copy.is_restarted = self.is_restarted
        game_copy.dead_player = self.dead_player
        game_copy.mode = self.mode
        game_copy.level = self.level
        game_copy.time_left = self.time_left

        return game_copy

    def play_step(self, action):
        """
        plays 1 step according to given action
        :param action:
        :return:
        """
        self.players[0].moving_left = False
        self.players[0].moving_right = False
        if action == MOVE_LEFT:
            self.players[0].moving_left = True
            for i in range(LOOP_AT_EACH_MOVE_UPDATE):
                self.update(is_a_star=True)
                if self.dead_player or not self.players[0].is_alive:
                    break
            self.players[0].moving_left = False
            if self.dead_player or  not self.players[0].is_alive:
                return
        elif action == MOVE_RIGHT:
            self.players[0].moving_right = True
            for i in range(LOOP_AT_EACH_MOVE_UPDATE):
                self.update(is_a_star=True)
                if self.dead_player or not self.players[0].is_alive:
                    break
            self.players[0].moving_right = False
            if self.dead_player or not self.players[0].is_alive:
                return
        elif action == SHOOT:
            if self.dead_player or not self.players[0].is_alive:
                self.update(is_a_star=True)
                return
            if not self.players[0].weapon.is_active:
                self.players[0].shoot()
            for i in range(LOOP_AT_EACH_MOVE_UPDATE):
                self.update(is_a_star=True)
                if self.dead_player or not self.players[0].is_alive:
                    break
            if self.dead_player or not self.players[0].is_alive:
                return

    def get_successors(self):
        """
        gets the children states of the given state
        :return:
        """
        successors_list = []
        random.shuffle(A_STAR_ACTION_LIST)
        for action in A_STAR_ACTION_LIST:
            successor = self.deep_copy_game()
            successor.play_step(action)
            successors_list.append([successor, action])

        return successors_list
