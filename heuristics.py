import math
from settings import *

def dont_die_heuristic(game, starting_score, path_size):
    if len(game.balls) == 0:
        return -1000000
    distance_from_closest_ball = distance_between_ball_and_player( game.balls[0], game)
    for ball in game.balls:
        if distance_between_ball_and_player(ball, game) < distance_from_closest_ball:
            distance_from_closest_ball = distance_between_ball_and_player(ball, game)
    if distance_from_closest_ball < 150:
        return 100000 * (150 - distance_from_closest_ball)
    return -distance_from_closest_ball

def distance_between_ball_and_player(ball, game, index = 0):
    distance_x = ball.rect.centerx - game.players[index].rect.centerx
    distance_y = ball.rect.centery - game.players[index].rect.centery
    return math.sqrt(math.pow(distance_x, 2) + math.pow(distance_y, 2))

def blow_up_ball_heuristic(game, starting_score, path_size):
    if len(game.balls) == 0:
        return -1000000
    count_balls = 0
    for ball in game.balls:
        if ball.size == 1:
            count_balls += 4
        elif ball.size == 2:
            count_balls += 12
        elif ball.size == 3:
            count_balls += 28
        elif ball.size == 4:
            count_balls += 60
    return count_balls

def stay_in_center_heuristic(game, starting_score, path_size):
    x_center = WINDOWWIDTH // 2
    return abs(game.players[0].rect.centerx - x_center)

# def shoot_heuristic(game, starting_score, path_size):

def pick_up_bonuses_heuristic(game, starting_score, path_size):
    if len(game.bonuses) == 0:
        return 0
    distance_from_closest_bonus = WINDOWWIDTH + 1
    for bonus in game.bonuses:
        if distance_between_ball_and_player(bonus, game) < distance_from_closest_bonus:
            distance_from_closest_bonus = distance_between_ball_and_player(bonus, game)
    return distance_from_closest_bonus * 100


def distance_between_bonus_and_player(bonus, game, index = 0):
    distance = abs(bonus.rect.centerx - game.players[index].rect.centerx)
    return distance


def main_heuristic(game, starting_score, path_size):
    return blow_up_ball_heuristic(game, starting_score, path_size) * 2 +\
           dont_die_heuristic(game, starting_score, path_size) * 6 +\
           stay_in_center_heuristic(game, starting_score, path_size) * 3
