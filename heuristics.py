import math
from settings import *
from a_star_utils import *
import numpy as np


DANGER_DIST_FROM_BUBBLE = 300
DANGER_X_DIST_FROM_BUBBLE = 40
SHOOT_FACTOR = 5
DANGER_X_DIST_AT_SHOOT_HEURISTIC = 55
DANGER_Y_DIST_FROM_BUBBLE = 80
DANGER_TIME_FROM_BUBBLE = 7
X_TOO_FAR_FOR_SHOOTING = 80

# heuristics:

def zero_heuristic(game, start):
    """
    ZERO
    a base line heuristic
    :param game: the current game state
    :param start: the start game state for th current A* call
    :return: zero
    """
    return 0


def stay_in_ball_area_but_not_too_close_x_axis_not_admissible_heuristic(game, start):
    """
    X AXIS
    follow bubbles and avoid danger in x axis
    :param game: the current game state
    :param start: the start game state for th current A* call
    :return:0 if goal.very high value that depends on agents distance from ball in x axis if it's < DANGER_X_DIST_FROM_BUBBLE.
     otherwise - agents distance from ball in x axis/PLAYER_SPEED/
    """
    if not game.balls and not game.hexagons:
        return 0
    agent_dist = find_the_distance_from_the_closest_ball_at_x_axis(game)[1]
    if agent_dist < DANGER_X_DIST_FROM_BUBBLE:
        return (DANGER_X_DIST_FROM_BUBBLE - agent_dist) * 1000
    elif is_sub_goal_score_bonuses(game, start):
        return 0
    return agent_dist/PLAYER_SPEED


def stay_in_ball_area_but_not_too_close_both_axis_not_admissible_heuristic(game, start):
    """
    BOTH AXES
    follow bubbles and avoid danger in x axis considering Y axis as well
    :param game: the current game state
    :param start: the start game state for th current A* call
    :return:0 if goal.very high value that depends on agents distance from ball in both axes if it's < DANGER_X_DIST_FROM_BUBBLE.
     otherwise - agents distance from ball in x axis/PLAYER_SPEED/
    """
    if not game.balls and not game.hexagons:
        return 0
    close_bubble, agent_dist = find_the_distance_from_the_closest_ball_at_x_axis(game)
    if agent_dist < DANGER_X_DIST_FROM_BUBBLE:
        return ((WINDOWHEIGHT - dist_from_bubble_and_player(close_bubble, game.players[0], axis=1))+(DANGER_X_DIST_FROM_BUBBLE - agent_dist)) * 1000
    elif is_sub_goal_score_bonuses(game, start):
        return 0
    return agent_dist/PLAYER_SPEED


def stay_in_ball_area_but_not_too_close_heuristic_time_admissible(game, start):
    """
    TIME
    follow bubbles and bonuses and avoid danger in by worst case scenario time to collision
    :param game: the current game state
    :param start: the start game state for th current A* call
    :return:0 if goal. very high value if time eo collision is very small. otherwise - the min of the time it'll take
    the player to catch bonus and the time it'll take a ball to reach the shot.
    """
    if not game.balls and not game.hexagons:
        return 0
    time_to_closest_bubble = get_time_to_closest_bubble(game)
    if time_to_closest_bubble < DANGER_TIME_FROM_BUBBLE:
            return (DANGER_TIME_FROM_BUBBLE-time_to_closest_bubble) * 1000
    elif is_sub_goal_score_bonuses(game, start):
        return 0
    ai_player = game.players[0]
    if len(game.bonuses) != 0:
        x_dist_to_closest_bonus = min([min(abs(ai_player.rect.left - bonus.rect.right),
                                         abs(ai_player.rect.right - bonus.rect.left)) for bonus in game.bonuses])
        time_to_closest_bonus = x_dist_to_closest_bonus / PLAYER_SPEED
    else:
        time_to_closest_bonus = np.inf
    if ai_player.weapon.is_active:
        ai_weapon = ai_player.weapon
        x_dist_from_weapon_to_bubble = min([min(abs(bubble.rect.left - ai_weapon.rect.right),
                                              abs(bubble.rect.right - ai_weapon.rect.left)) for bubble in game.balls + game.hexagons])
        time_from_weapon_to_bubble = x_dist_from_weapon_to_bubble / PLAYER_SPEED # hosem bubble max_speed
    else:
        time_from_weapon_to_bubble = np.inf
    return min(time_from_weapon_to_bubble, time_to_closest_bonus, time_to_closest_bonus)


def bonus_and_ball_but_not_too_close_heuristic(game, start):
    """
    BONUS
    follow bubbles and avoid danger in x axis, while trying to collect bonuses if exist.
    :param game: the current game state
    :param start: the start game state for th current A* call
    :return: 0 if goal.very high value that depends on agents distance from ball in x axis if it's < DANGER_X_DIST_FROM_BUBBLE.
     otherwise - dist_from_bonus/PLAYER_SPEED if bonus exists and  dist_from_bonus/PLAYER_SPEED if there are no bonuses.
    """
    if not game.balls and not game.hexagons:
        return 0
    agent_dist = find_the_distance_from_the_closest_ball_at_x_axis(game)[1]
    if agent_dist < DANGER_X_DIST_FROM_BUBBLE + 10:
        return (DANGER_X_DIST_FROM_BUBBLE + 10 - agent_dist) * 1000
    elif is_sub_goal_score_bonuses(game, start):
        return 0

    dist_from_bonus = pick_up_bonuses(game)
    if dist_from_bonus == WINDOWWIDTH + 1:
        return agent_dist/PLAYER_SPEED
    return dist_from_bonus/PLAYER_SPEED


def stay_in_center_heuristic(game, start):
    """
    CENTER
    follow bubbles and avoid danger in x axis while trying to avoid the edges of the screen
    :param game: the current game state
    :param start: the start game state for th current A* call
    :return: 0 if goal.very high value that depends on agents distance from ball in x axis if it's < DANGER_X_DIST_FROM_BUBBLE.
     otherwise - dist_from_center/PLAYER_SPEED if player is in the right/left quarters of the screen and
     dist_from_bonus/PLAYER_SPEED if it's in the middle half.
    """
    if not game.balls and not game.hexagons:
        return 0
    agent_dist = find_the_distance_from_the_closest_ball_at_x_axis(game)[1]
    if agent_dist < DANGER_X_DIST_FROM_BUBBLE:
        return (DANGER_X_DIST_FROM_BUBBLE - agent_dist) * 1000
    elif is_sub_goal_score_bonuses(game, start):
        return 0

    x_center = WINDOWWIDTH // 2
    dist_from_center = abs(game.players[0].rect.centerx - x_center)
    if dist_from_center > WINDOWWIDTH // 4:
        return dist_from_center/PLAYER_SPEED
    else:
        return agent_dist/PLAYER_SPEED


def shoot_on_small_balls_heuristic(game, start):
    """
    SMALL BALLS
    follow small bubbles and avoid danger in x axis
    :param game: the current game state
    :param start: the start game state for th current A* call
    :return:0 if goal.very high value that depends on agents distance from ball in x axis if it's < DANGER_X_DIST_FROM_BUBBLE.
     otherwise - agents distance from a ball of minimal size in x axis/PLAYER_SPEED
    """
    if not game.balls and not game.hexagons:
        return 0
    if not game.balls and not game.hexagons:
        return 0
    agent_dist = find_the_distance_from_the_closest_ball_at_x_axis(game)[1]
    if agent_dist < DANGER_X_DIST_FROM_BUBBLE:
        return (DANGER_X_DIST_FROM_BUBBLE - agent_dist) * 1000
    elif is_sub_goal_score_bonuses(game, start):
        return 0

    agent_dist_from_smallest_ball = find_the_distance_from_the_closest_smallest_ball_x_axis(game)[1]

    return agent_dist_from_smallest_ball/PLAYER_SPEED


def shoot_heuristic(game, start):
    """
    SHOOT
    follow bubbles and avoid danger in x axis, while trying to shoot only when the weapon is close to a bubble
    :param game: the current game state
    :param start: the start game state for th current A* call
    :return:0 if goal.very high value that depends on agents distance from ball in x axis if it's < DANGER_X_DIST_FROM_BUBBLE.
    if there is a shot in the air and it's too far from a buuble - a very high value that depends on the agent's distance
    from the closest bubble and the shot's distance from the closest bubble
    otherwise - agents distance from the closest ball in x axis/PLAYER_SPEED
    """
    if not game.balls and not game.hexagons:
        return 0
    agent_dist = find_the_distance_from_the_closest_ball_at_x_axis(game)[1]
    if agent_dist < DANGER_X_DIST_AT_SHOOT_HEURISTIC:
        euclidean_dist = find_the_distance_from_the_closest_bubble(game)[1]
        if euclidean_dist < DANGER_DIST_FROM_BUBBLE:
            return (DANGER_X_DIST_AT_SHOOT_HEURISTIC - agent_dist) * 1000
    elif is_sub_goal_score_bonuses(game, start):
        return 0

    if game.players[0].weapon.is_active:
        dist_from_weapon_to_closest_bubble = distance_from_weapon_and_bubble(game)
        if dist_from_weapon_to_closest_bubble > X_TOO_FAR_FOR_SHOOTING:
            return (agent_dist + (SHOOT_FACTOR*dist_from_weapon_to_closest_bubble))/PLAYER_SPEED

    return agent_dist/PLAYER_SPEED


def distance_from_weapon_and_bubble(game):
    """
    :param game:
    :return: distance of shot from closest bubble. WINDOWWIDTH if there is no shot on screen
    """
    if game.players[0].weapon.is_active:
        return distance_from_weapon_and_bubbles_list(game, game.balls + game.hexagons)
    return WINDOWWIDTH


def distance_from_weapon_and_bubbles_list(game, bubbles_list):
    """
    :param game:
    :return: distance of shot from closest bubble in the given list. WINDOWWIDTH if there is no shot on screen
    """
    return min([abs(bubble.rect.centerx - game.players[0].weapon.rect.centerx) for bubble in bubbles_list])


def find_the_distance_from_the_closest_ball_at_x_axis(game, index = 0):
    """
    :param game:
    :param index: player index
    :return: distance of player from closest bubble
    """
    bubbles = game.balls + game.hexagons
    return find_x_axis_closest_bubble_from_list(game, bubbles)


def distance_between_bonus_and_player(bonus, game, index=0):
    """
    :param bonus:
    :param game:
    :param index: player index
    :return: x axis distance between agent  and bonus
    """
    distance = abs(bonus.rect.centerx - game.players[index].rect.centerx)
    return distance


def find_the_distance_from_the_closest_bubble(game, index = 0):
    """
    :param game:
    :param index:
    :return: euclidean distance of agent and closest bubble
    """
    bubbles = game.balls + game.hexagons
    return find_euclidian_closest_bubble_from_list(game, bubbles)


def find_euclidian_closest_bubble_from_list(game, bubbles_list):
    bubbles_dist = [euclidean_dist_bubble_and_player(bubble, game.players[0]) for bubble in bubbles_list]
    min_dist_bubble_index = int(np.argmin(np.array(bubbles_dist)))
    return bubbles_list[min_dist_bubble_index], bubbles_dist[min_dist_bubble_index]


def find_x_axis_closest_bubble_from_list(game, bubbles_list):
    bubbles_dist = [dist_from_bubble_and_player(bubble, game.players[0], axis=0) for bubble in bubbles_list]
    min_dist_bubble_index = int(np.argmin(np.array(bubbles_dist)))
    return bubbles_list[min_dist_bubble_index], bubbles_dist[min_dist_bubble_index]


def find_the_distance_from_the_closest_smallest_ball_x_axis(game):
    bubbles = game.balls + game.hexagons
    min_size = min([bubble.size for bubble in bubbles])
    small_bubbles = [bubble for bubble in bubbles if bubble.size == min_size]
    return find_x_axis_closest_bubble_from_list(game, small_bubbles)


def time_from_bubble_and_player(game, bubble, axis=0, player_index=0):
    dist_from_bubble = dist_from_bubble_and_player(bubble, game.players[0], axis)
    bubble_axis_speed = abs(bubble.speed[axis])
    if axis == 0:
        total_speed = max(PLAYER_SPEED + bubble_axis_speed, 1)
    else:
        if bubble.image_name == BALL_IMAGE_NAME:
            # TODO: it's for addmissable
            total_speed = max(bubble_axis_speed + 2 * np.sqrt(dist_from_bubble), 1)
        else:
            total_speed = max(bubble_axis_speed, 1)
    time_from_bubble = int(np.ceil(dist_from_bubble / total_speed))
    return time_from_bubble


def dist_from_bubble_and_player(bubble, player, axis=0):
    if axis == 0:
        player_spot = player.rect.centerx
        pos_bubble_spot = bubble.rect.left
        neg_bubble_spot = bubble.rect.right
        return min(abs(player_spot - pos_bubble_spot), abs(player_spot - neg_bubble_spot))
    else:
        return abs(bubble.rect.bottom - player.rect.top)


def euclidean_dist_bubble_and_player(bubble, player):
    return math.sqrt(math.pow(dist_from_bubble_and_player(bubble, player, 0),2) + math.pow(dist_from_bubble_and_player(bubble, player, 1),2))


def get_time_to_closest_bubble(game, player_index=0):
    return min([max(time_from_bubble_and_player(game, cur_bubble, 0, player_index),
                    time_from_bubble_and_player(game, cur_bubble, 1, player_index)) for cur_bubble in game.balls + game.hexagons])


def pick_up_bonuses(game):
    distance_from_closest_bonus = WINDOWWIDTH + 1
    if len(game.bonuses) == 0:
        return distance_from_closest_bonus
    for bonus in game.bonuses:
        if abs(game.players[0].rect.top - bonus.rect.centery) > 10:
            continue
        else:
            distance_from_bonus = distance_between_bonus_and_player(bonus, game)
        if distance_from_bonus < distance_from_closest_bonus:
            distance_from_closest_bonus = distance_from_bonus
    return distance_from_closest_bonus

