from settings import *

BALL_WORTH_BY_SIZE = {1: 1,
                      2: 3,
                      3: 7,
                      4: 15,
                      5: 31}


def g_function_by_steps(game, start):
    """
    :param game: the state of the game when A* was called
    :param start: the state represented by the current node in the search
    :return: number of game iterations passed between these states
    """
    return (start.time_left - game.time_left) / TIME_UNIT

### subgoals functions

def is_sub_goal_score_bonuses(game, start):
    """
    :param game: the state of the game when A* was called
    :param start: the state represented by the current node in the search
    :return: True if a bonus was collected or a bubble was blown between the start state to the current state(game).
    False otherwise
    """
    return is_sub_goal_by_bonuses(game, start) or is_sub_goal_by_score(game, start)


def is_sub_goal_steps_score_bonuses(game, start,steps=MAX_PATH_SIZE):
    """
    :param game: the state of the game when A* was called
    :param start: the state represented by the current node in the search
    :return: True if a bonus was collected, a bubble was blown or a set number of game iterations passed between the
    start state to the current state(game). False otherwise
    """
    return is_sub_goal_by_bonuses(game, start) or is_sub_goal_score_or_steps(game, start, steps=steps)


def is_sub_goal_by_bonuses(game, start):
    """
    :param game: the state of the game when A* was called
    :param start: the state represented by the current node in the search
    :return: True if a bonus was collected. False otherwise
    """
    return is_sub_goal_life_bonus(game, start) or is_sub_goal_time_bonus(game, start)


def is_sub_goal_life_bonus(game, start):
    """
    :param game: the state of the game when A* was called
    :param start: the state represented by the current node in the search
    :return: True if a life bonus was collected. False otherwise
    """
    return start.players[0].lives < game.players[0].lives


def is_sub_goal_time_bonus(game, start):
    """
    :param game: the state of the game when A* was called
    :param start: the state represented by the current node in the search
    :return: True if a time bonus was collected. False otherwise
    """
    return start.time_left < game.time_left


def is_sub_goal_by_score(game, start):
    """
    :param game: the state of the game when A* was called
    :param start: the state represented by the current node in the search
    :return: True if a bubble was blown. False otherwise
    """
    return game.get_score() > start.get_score() or game.level_completed


def is_sub_goal_score_or_steps(game, start, steps=MAX_PATH_SIZE):
    """
    :param game: the state of the game when A* was called
    :param start: the state represented by the current node in the search
    :return: True if a bubble was blown or a set number of game iterations passed between the start state to the
    current state(game). False otherwise
    """
    return is_sub_goal_by_score(game, start) or is_sub_goal_by_steps(game, start, steps=steps)


def is_sub_goal_by_steps(game, start, steps=MAX_PATH_SIZE):
    """
    :param game: the state of the game when A* was called
    :param start: the state represented by the current node in the search
    :return: True if a set number of game iterations passed between the start state to the current state(game).
     False otherwise
    """
    return start.time_left - game.time_left >= steps * TIME_UNIT
