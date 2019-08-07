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


class Game:

    def __init__(self, level=1):
        self.score = 0
        self.g_score = 0
        self.f_score = 0
        self.balls = []
        self.hexagons = []
        self.players = [Player()]
        self.bonuses = []
        self.level = level
        self.game_over = False
        self.level_completed = False
        self.is_running = True
        self.is_completed = False
        self.max_level = MAX_LEVEL # TODO change if we want to add levels
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
        if bool(random.getrandbits(1)):
            return self.get_f_score() < other.get_f_score()
        else:
            return self.get_f_score() <= other.get_f_score()

    def check_if_equal(self, other):
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
        self.score += to_add

    def get_score(self):
        return int(self.score)

    def update_f_score(self, value):
        self.f_score = value

    def get_f_score(self):
        return self.f_score

    def load_level(self, level):
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
        for bonus_index, bonus in enumerate(self.bonuses):
            if pygame.sprite.collide_mask(bonus, player):
                self._activate_bonus(bonus.type, player)
                del self.bonuses[bonus_index]
                return True
        return False

    def _decrease_lives(self, player):
        player.lives -= 1
        if player.lives:
            self.dead_player = True
            player.is_alive = False
        else:
            self.game_over = True

    def _restart(self):
        self.load_level(self.level)

    @staticmethod
    def _drop_bonus():
        if random.randrange(BONUS_DROP_RATE) == 0:
            bonus_type = random.choice(bonus_types)
            return bonus_type

    def _activate_bonus(self, bonus, player):
        if bonus == BONUS_LIFE:
            player.lives += 1
        elif bonus == BONUS_TIME:
            self.time_left += 50

    def _split_ball(self, ball_index):
        ball = self.balls[ball_index]
        if ball.size > 1:
            self.balls.append(Ball(
                ball.rect.left - ball.size**2,
                ball.rect.top - 10, ball.size - 1, [-3, -5])
            )
            self.balls.append(
                Ball(ball.rect.left + ball.size**2,
                     ball.rect.top - 10, ball.size - 1, [3, -5])
            )
        del self.balls[ball_index]
        bonus_type = self._drop_bonus()
        if bonus_type:
            bonus = Bonus(ball.rect.centerx, ball.rect.centery, bonus_type)
            self.bonuses.append(bonus)

    def _split_hexagon(self, hex_index):
        hexagon = self.hexagons[hex_index]
        if hexagon.size > 1:
            self.hexagons.append(
                Hexagon(hexagon.rect.left, hexagon.rect.centery,
                        hexagon.size - 1, [-3, -5]))
            self.hexagons.append(
                Hexagon(hexagon.rect.right, hexagon.rect.centery,
                        hexagon.size - 1, [3, -5]))
        del self.hexagons[hex_index]
        bonus_type = self._drop_bonus()
        if bonus_type:
            bonus = Bonus(hexagon.rect.centerx, hexagon.rect.centery,
                          bonus_type)
            self.bonuses.append(bonus)

    def update(self):
        if self.level_completed:
            self.add_to_score(TIME_LEFT_SCORE_FACTOR * self.get_time_left())
        if self.level_completed and not self.is_completed:
            self.load_level(self.level + 1)
        if self.game_over:
            self.is_running = False
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
        self.time_left -= TIME_UNIT
        if self.time_left <= 0:
            for player in self.players:
                self._decrease_lives(player)

    def get_time_left(self):
        return int(np.ceil(self.time_left))

    def deep_copy_game(self): # TODO check if ok
        game_copy = Game(level=self.level)

        # TODO check if deep working
        game_copy.balls = []
        for ball in self.balls:
            game_copy.balls.append(ball.deep_copy_bubble())
        game_copy.hexagons = []
        for hexagon in self.hexagons:
            game_copy.hexagons.append(hexagon.deep_copy_bubble())
        # TODO
        game_copy.players = []
        for player in self.players:
            game_copy.players.append(player.deep_copy_player())
        #TODO
        game_copy.bonuses = []
        for bonus in self.bonuses:
            game_copy.bonuses.append(bonus.deep_copy_bonus())

        # copy fields
        game_copy.score = self.score
        game_copy.g_score = self.g_score
        game_copy.f_score = self.f_score
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
        self.players[0].moving_left = False
        self.players[0].moving_right = False
        if action == MOVE_LEFT:
            self.players[0].moving_left = True
            for i in range(LOOP_AT_EACH_MOVE_UPDATE):
                if self.dead_player or not self.players[0].is_alive:
                    break
                self.update()
            self.players[0].moving_left = False
            if self.dead_player or  not self.players[0].is_alive:
                return
        elif action == MOVE_RIGHT:
            self.players[0].moving_right = True
            for i in range(LOOP_AT_EACH_MOVE_UPDATE):
                if self.dead_player or not self.players[0].is_alive:
                    break
                self.update()
            self.players[0].moving_right = False
            if self.dead_player or not self.players[0].is_alive:
                return
        elif action == SHOOT:
            if self.dead_player or not self.players[0].is_alive:
                return
            if not self.players[0].weapon.is_active:
                self.players[0].shoot()
            for i in range(LOOP_AT_EACH_MOVE_UPDATE):
                if self.dead_player or not self.players[0].is_alive:
                    break
                self.update()
            if self.dead_player or not self.players[0].is_alive:
                return

    def get_successors(self):
        # TODO maybe update X times faster (by increase speed, at astar)
        successors_list = []
        for action in A_STAR_ACTION_LIST:
            successor = self.deep_copy_game()
            successor.play_step(action)
            successors_list.append([successor, action])

        return successors_list

    def get_represented_state(self):
        # (ball1x, ball1y, ball1size, ball1dir, ball2x, ball2y, ball2size, ball2dir, ..., p1x, isshot)
        cur_state = []
        cur_player_x = self.players[AI_PLAYER_NUM].rect.centerx
        cur_player_y = self.players[AI_PLAYER_NUM].rect.centery
        x_closest_bubbles = self.get_x_closest_bubbles(BALLS_AT_STATE)
        for i in range(BALLS_AT_STATE):
            if i < len(x_closest_bubbles):
                bubble = x_closest_bubbles[i]
                if 'ball' in bubble.image_name:
                    bubble_type = 1
                elif 'hexagon' in bubble.image_name:
                    bubble_type = -1
                else:
                    print('invalid bubble type')
                if bubble.speed[0] > 0:
                    bubble_dir = 1
                else:
                    bubble_dir = -1
                cur_state.append(bubble_type)
                cur_state.append(bubble.size)
                cur_state.append(bubble.rect.centerx - cur_player_x)
                cur_state.append(bubble.rect.centery - cur_player_y)
                cur_state.append(bubble_dir)
            else:
                cur_state += [0, 0, 0, 0, 0]

        if self.players[AI_PLAYER_NUM].weapon.is_active:
            weapon_active = 1
        else:
            weapon_active = -1

        num_of_bubbles = len(self.balls) + len(self.hexagons)

        cur_state.append(num_of_bubbles)
        cur_state.append(cur_player_x)
        cur_state.append(weapon_active)

        return cur_state

    def get_x_closest_bubbles(self, x):
        closest_x_balls = []
        all_balls_list = []
        for ball in self.balls:
            all_balls_list.append((ball, heuristics.distance_between_ball_and_player(ball, self))) # TODO move here
        for ball in self.hexagons:
            all_balls_list.append((ball, heuristics.distance_between_ball_and_player(ball, self))) # TODO move here

        sorted_balls = sorted(all_balls_list, key=operator.itemgetter(1))
        for i in range(min(x, len(sorted_balls))):
            closest_x_balls.append(sorted_balls[i][0])

        return closest_x_balls
