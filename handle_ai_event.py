from a_star import *
from game import *
from heuristics import *
from settings import *
from a_star_utils import *
import copy
from copy import *

ai_spot_counter = 0
ai_path_size = 0
ai_path = None


def handle_ai_game_event(game, font, clock, screen, main_menu, load_level_menu, heuristic, is_goal_func):
    """
    handles game event using AI. if a path of unperformed actions(the output of A*) exists, it performs the next action in the path
    using a global index. otherwise it calls A* and gets such path of instructions.
    :param game:
    :param font:
    :param clock:
    :param screen:
    :param main_menu:
    :param load_level_menu:
    :param heuristic:
    :param is_goal_func:
    :return: the number of nodes opened in A* (for analysis)
    """
    global ai_spot_counter, ai_path_size, ai_path
    # if we finish the current path, construct a new one
    open_nodes = 0
    if (ai_spot_counter // LOOP_AT_EACH_MOVE_UPDATE >= ai_path_size):
        ai_path, ai_path_size, open_nodes = a_star(start=game, is_goal=is_goal_func,
                                       heuristic=heuristic,
                                       g_function=g_function_by_steps)
        if ai_path_size > REAL_PATH_LEN:
            ai_path = ai_path[0:REAL_PATH_LEN]
            ai_path_size = len(ai_path)
        ai_spot_counter = 0
    # AI couldn't find a path
    if len(ai_path) == 0:
        return open_nodes

    real_spot_at_path = ai_spot_counter // LOOP_AT_EACH_MOVE_UPDATE
    cur_action = ai_path[real_spot_at_path]
    play_single_action(game, cur_action, player_num=AI_PLAYER_NUM)
    ai_spot_counter += 1
    return open_nodes


def play_single_action(game, cur_action, player_num=0):
    """
    sets the proper boolean values so the player number player_num will perform the cur_action in the given game.
    :param game:
    :param cur_action:
    :param player_num:
    :return:
    """
    if cur_action == MOVE_LEFT:
        game.players[player_num].moving_left = True
        game.players[player_num].moving_right = False
    elif cur_action == MOVE_RIGHT:
        game.players[player_num].moving_right = True
        game.players[player_num].moving_left = False
    elif cur_action == SHOOT and not game.players[player_num].weapon.is_active:
        game.players[player_num].moving_left = False
        game.players[player_num].moving_right = False
        game.players[player_num].shoot()


def handle_random_game_event(game, player_num=0):
    """
    picks a random action for player number player_num in the given game.
    :param game:
    :param player_num:
    :return:
    """
    game.players[player_num].moving_left = random.getrandbits(1)
    game.players[player_num].moving_right = random.getrandbits(1)
    if random.getrandbits(1) and not game.players[player_num].weapon.is_active:
        game.players[player_num].shoot()
