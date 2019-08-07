import math
from settings import *
import random


def is_level_completed(game, starting_score, path_size):
    if len(game.balls) == 0 and len(game.hexagons) == 0:
        return -1000000
    return 0


def dont_die_heuristic(game, starting_score, path_size):
    if len(game.balls) == 0 and len(game.hexagons) == 0:
        return 0
    distance_from_closest_ball = find_the_distance_from_the_closest_ball(game)[1]
    if distance_from_closest_ball < 200:
        return pow(200, 2) - pow(distance_from_closest_ball, 2)
    return 0


def find_the_distance_from_the_closest_ball(game, index = 0):
    if len(game.balls) != 0:
        distance_from_closest_ball = distance_between_ball_and_player(game.balls[0], game)
        closest_ball = game.balls[0]
    else:
        distance_from_closest_ball = distance_between_ball_and_player(game.hexagons[0], game)
        closest_ball = game.hexagons[0]
    for i in range(1, len(game.balls)):
        cur_ball = game.balls[i]
        cur_dist = distance_between_ball_and_player(cur_ball, game)
        if cur_dist < distance_from_closest_ball:
            distance_from_closest_ball = cur_dist
            closest_ball = cur_ball
    for i in range(len(game.hexagons)):
        cur_ball = game.hexagons[i]
        cur_dist = distance_between_ball_and_player(cur_ball, game)
        if cur_dist < distance_from_closest_ball:
            distance_from_closest_ball = cur_dist
            closest_ball = cur_ball
    return closest_ball, distance_from_closest_ball


def time_from_closest_bubble_at_x_axis(game, player_index = 0):
    player_x = game.players[player_index].rect.centerx
    if len(game.balls) != 0:
        cur_bubble = game.balls[0]
        bubble_x = cur_bubble.rect.centerx
        bubble_x_speed = cur_bubble.speed[0]
        dist_from_bubble = abs(player_x - bubble_x)
        total_speed = PLAYER_SPEED + bubble_x_speed
        time_from_closest_bubble = dist_from_bubble / total_speed
        closest_bubble = cur_bubble
    else:
        cur_bubble = game.hexagons[0]
        bubble_x = cur_bubble.rect.centerx
        bubble_x_speed = cur_bubble.speed[0]
        dist_from_bubble = abs(player_x - bubble_x)
        total_speed = PLAYER_SPEED + bubble_x_speed
        time_from_closest_bubble = dist_from_bubble / total_speed
        closest_bubble = cur_bubble
    for i in range(1, len(game.balls)):
        cur_bubble = game.balls[i]
        bubble_x = cur_bubble.rect.centerx
        bubble_x_speed = cur_bubble.speed[0]
        dist_from_bubble = abs(player_x - bubble_x)
        total_speed = PLAYER_SPEED + bubble_x_speed
        time_from_bubble = dist_from_bubble / total_speed

        if time_from_bubble < time_from_closest_bubble:
            time_from_closest_bubble = time_from_bubble
            closest_bubble = cur_bubble
    for i in range(1, len(game.hexagons)):
        cur_bubble = game.hexagons[i]
        bubble_x = cur_bubble.rect.centerx
        bubble_x_speed = cur_bubble.speed[0]
        dist_from_bubble = abs(player_x - bubble_x)
        total_speed = PLAYER_SPEED + bubble_x_speed
        time_from_bubble = dist_from_bubble / total_speed

        if time_from_bubble < time_from_closest_bubble:
            time_from_closest_bubble = time_from_bubble
            closest_bubble = cur_bubble
    return closest_bubble, time_from_closest_bubble


def stay_in_ball_area_but_not_too_close_heuristic(game):
    if not game.balls and not game.hexagons:
        return - BLOW_UP_BALL_SCORE
    TOO_CLOSE_DIST = 10
    time_to_collide = time_from_closest_bubble_at_x_axis(game)[1]
    if time_to_collide < TOO_CLOSE_DIST:
        return (TOO_CLOSE_DIST-time_to_collide) * 1000
    return time_to_collide

def player_bonus_and_ball_heuristic(game):
    if not game.balls and not game.hexagons:
        return - 50
    agent_dist = find_the_distance_from_the_closest_ball_at_x_axis(game)[1]
    if agent_dist < 50:
        return (50-agent_dist) * 1000
    if agent_dist > pick_up_bonuses_heuristic(game) and pick_up_bonuses_heuristic(game) != 0:
        return pick_up_bonuses_heuristic(game)
    return agent_dist



def random_player_heuristic(game):
    return random.randrange(1, 50)


def distance_from_weapon_and_ball(game):
    if game.players[0].weapon.is_active:
        return min([abs(ball.rect.centerx - game.players[0].weapon.rect.centerx) for ball in game.balls + game.hexagons])
    return WINDOWWIDTH


def find_the_distance_from_the_closest_ball_at_x_axis(game, index = 0):
    if len(game.balls) != 0:
        distance_from_closest_ball = abs(game.players[0].rect.centerx - game.balls[0].rect.centerx)
        closest_ball = game.balls[0]
    else:
        distance_from_closest_ball = abs(game.players[0].rect.centerx - game.hexagons[0].rect.centerx)
        closest_ball = game.hexagons[0]
    for i in range(1, len(game.balls)):
        cur_ball = game.balls[i]
        cur_dist = abs(game.players[0].rect.centerx - cur_ball.rect.centerx)
        if cur_dist < distance_from_closest_ball:
            distance_from_closest_ball = cur_dist
            closest_ball = cur_ball
    for i in range(len(game.hexagons)):
        cur_ball = game.hexagons[i]
        cur_dist = abs(game.players[0].rect.centerx - cur_ball.rect.centerx)
        if cur_dist < distance_from_closest_ball:
            distance_from_closest_ball = cur_dist
            closest_ball = cur_ball
    return closest_ball, distance_from_closest_ball


def distance_between_ball_and_player(ball, game, index = 0):
    distance_x = ball.rect.centerx - game.players[index].rect.centerx
    distance_y = ball.rect.centery - game.players[index].rect.bottom
    return math.sqrt(math.pow(distance_x, 2) + math.pow(distance_y, 2))


def blow_up_ball_heuristic(game, starting_score, path_size):
    if len(game.balls) == 0 and len(game.hexagons) == 0:
        return 0
    count_balls = 0
    for ball in game.balls:
        if ball.size == 1:
            count_balls += 10
        elif ball.size == 2:
            count_balls += 25
        elif ball.size == 3:
            count_balls += 53
        elif ball.size == 4:
            count_balls += 108
    for ball in game.hexagons:
        if ball.size == 1:
            count_balls += 10
        elif ball.size == 2:
            count_balls += 25
        elif ball.size == 3:
            count_balls += 53
        elif ball.size == 4:
            count_balls += 108
    return count_balls


def stay_in_center_heuristic(game, starting_score, path_size):
    x_center = WINDOWWIDTH // 2
    return abs(game.players[0].rect.centerx - x_center)


def shoot_heuristic(game, starting_score, path_size):
    if len(game.balls) == 0 and len(game.hexagons) == 0:
        return 0
    ball, distance_from_closest_ball = find_the_distance_from_the_closest_ball_at_x_axis(game)
    if distance_from_closest_ball < 70 and game.players[0].weapon.is_active:
        return -(70-distance_from_closest_ball)
    elif distance_from_closest_ball >= 70 and game.players[0].weapon.is_active:
        return distance_from_closest_ball
    return 0


def pick_up_bonuses_heuristic(game):
    if len(game.bonuses) == 0:
        return 0
    distance_from_closest_bonus = WINDOWWIDTH + 1
    for bonus in game.bonuses:
        if distance_between_bonus_and_player(bonus, game) < distance_from_closest_bonus:
            distance_from_closest_bonus = distance_between_bonus_and_player(bonus, game)
    if distance_from_closest_bonus == WINDOWWIDTH + 1:
        return 0
    return distance_from_closest_bonus


def distance_between_bonus_and_player(bonus, game, index = 0):
    distance = abs(bonus.rect.centerx - game.players[index].rect.centerx)
    return distance


def distance_sign_between_ball_and_player(ball,game,index=0):
    return ball.rect.centerx - game.players[index].rect.centerx


def keep_balls_on_one_side(game, starting_score, path_size):
    distances_sign = []
    for cur_ball in game.balls + game.hexagons:
        distances_sign.append(distance_sign_between_ball_and_player(cur_ball, game))
    all_pos = True
    all_neg = True
    for dist in distances_sign:
        if dist > 0:
            all_neg = False
        else:
            all_pos = False
        if not all_pos or not all_neg:
            return 100
    return - 10**len(game.balls + game.hexagons)


def zero_heuristic(game):
    return 0


def main_heuristic(game, starting_score, path_size):
    if not game.players[0].is_alive:
        return 1000000
    return stay_in_center_heuristic(game, starting_score, path_size) * 0 +\
            blow_up_ball_heuristic(game, starting_score, path_size) * 0 +\
           pick_up_bonuses_heuristic(game, starting_score, path_size) * 0 +\
           shoot_heuristic(game, starting_score, path_size) * 0 + \
           is_level_completed(game, starting_score, path_size) * 0 +\
           dont_die_heuristic(game, starting_score, path_size) * 0
