import math
from settings import *
import numpy as np


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


def distance_between_bonus_and_player(bonus, game, index = 0):
    distance = abs(bonus.rect.centerx - game.players[index].rect.centerx)
    return distance


def distance_sign_between_ball_and_player(ball,game,index=0):
    return ball.rect.centerx - game.players[index].rect.centerx


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


def time_from_bubble_and_player(game, bubble, axis=0, player_index=0):
    if axis == 0:
        player_spot = game.players[player_index].rect.centerx
        bubble_spot = bubble.rect.centerx
    else:
        player_spot = 0
        bubble_spot = bubble.rect.centery
    bubble_axis_speed = abs(bubble.speed[axis])
    dist_from_bubble = abs(player_spot - bubble_spot)
    if axis == 0:
        total_speed = max(PLAYER_SPEED + bubble_axis_speed, 1)
    else:
        # TODO: it's for addmissable
        total_speed = max(bubble_axis_speed + 2 * np.sqrt(dist_from_bubble), 1)
    time_from_bubble = int(np.ceil(dist_from_bubble / total_speed))
    return time_from_bubble


def time_from_closest_bubble_at_axis(game, axis=0, player_index=0):
    if len(game.balls) != 0:
        cur_bubble = game.balls[0]
        time_from_closest_bubble = time_from_bubble_and_player(game, cur_bubble, axis, player_index)
        closest_bubble = cur_bubble
    else:
        cur_bubble = game.hexagons[0]
        time_from_closest_bubble = time_from_bubble_and_player(game, cur_bubble, axis, player_index)
        closest_bubble = cur_bubble
    for i in range(1, len(game.balls)):
        cur_bubble = game.balls[i]
        time_from_bubble = time_from_bubble_and_player(game, cur_bubble, axis, player_index)
        if time_from_bubble < time_from_closest_bubble:
            time_from_closest_bubble = time_from_bubble
            closest_bubble = cur_bubble
    for i in range(1, len(game.hexagons)):
        cur_bubble = game.hexagons[i]
        time_from_bubble = time_from_bubble_and_player(game, cur_bubble, axis, player_index)
        if time_from_bubble < time_from_closest_bubble:
            time_from_closest_bubble = time_from_bubble
            closest_bubble = cur_bubble
    return closest_bubble, time_from_closest_bubble


def stay_in_ball_area_but_not_too_close_heuristic(game):
    if not game.balls and not game.hexagons:
        return - BLOW_UP_BALL_SCORE
    TOO_CLOSE_X_DIST = 10
    TOO_CLOSE_Y_DIST = 10
    closest_ball_at_x, time_to_collide_at_x = time_from_closest_bubble_at_axis(game, axis=0)
    if time_to_collide_at_x < TOO_CLOSE_X_DIST:
        time_to_collide_at_y = time_from_bubble_and_player(game, closest_ball_at_x, axis=1, player_index=0)
        if time_to_collide_at_y < TOO_CLOSE_Y_DIST:
            return (max(TOO_CLOSE_X_DIST-time_to_collide_at_x, TOO_CLOSE_Y_DIST-time_to_collide_at_y)) * 1000
    return time_to_collide_at_x


def stay_in_ball_area_but_not_too_close_no_admissible_x_axis_heuristic(game):
    if not game.balls and not game.hexagons:
        return - BLOW_UP_BALL_SCORE
    agent_dist = find_the_distance_from_the_closest_ball_at_x_axis(game)[1]
    if agent_dist < 50:
        return (50 - agent_dist) * 1000
    return agent_dist


def player_bonus_and_ball_heuristic(game):
    if not game.balls and not game.hexagons:
        return - 50
    agent_dist = find_the_distance_from_the_closest_ball_at_x_axis(game)[1]
    if agent_dist < 50:
        return (50-agent_dist) * 1000
    dist_from_bonus = pick_up_bonuses_heuristic(game)
    return min(dist_from_bonus, agent_dist)


def stay_in_center_heuristic(game):
    if not game.balls and not game.hexagons:
        return - BLOW_UP_BALL_SCORE
    x_center = WINDOWWIDTH // 2
    agent_dist = find_the_distance_from_the_closest_ball(game)[1]
    if agent_dist < 80:
        return (80 - agent_dist) * 1000
    return abs(game.players[0].rect.centerx - x_center)


def shoot_on_small_balls_heuristic(game):
    if not game.balls and not game.hexagons:
        return - BLOW_UP_BALL_SCORE
    closest_ball, agent_dist = find_the_distance_from_the_closest_ball_at_x_axis(game)
    if agent_dist < 50:
        return (50 - agent_dist) * 1000
    return agent_dist / (100*(5 - closest_ball.size))


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
    distance_from_closest_bonus = WINDOWWIDTH + 1
    if len(game.bonuses) == 0:
        return distance_from_closest_bonus
    for bonus in game.bonuses:
        distance_from_bonus = distance_between_bonus_and_player(bonus, game)
        if distance_from_bonus < distance_from_closest_bonus:
            distance_from_closest_bonus = distance_from_bonus
    return distance_from_closest_bonus


def zero_heuristic(game):
    return 0
