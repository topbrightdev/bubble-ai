from a_star import *
from game import *
from heuristics import *
from settings import *
from a_star_utils import *

ai_spot_counter = 0
ai_path_size = 0
ai_path = None


def handle_ai_game_event(game, font, clock, screen, main_menu, load_level_menu):
    global ai_spot_counter, ai_path_size, ai_path
    # if we finish the current path, construct a new one
    if (ai_spot_counter // LOOP_AT_EACH_MOVE_UPDATE >= ai_path_size):
        ai_path, ai_path_size = a_star(start=game, is_goal=is_sub_goal_score_or_steps, heuristic=zero_heuristic,
                                       g_function=g_function_by_score_and_time)
        if ai_path_size > REAL_PATH_LEN:
            ai_path = ai_path[0:REAL_PATH_LEN]
            ai_path_size = len(ai_path)
        ai_spot_counter = 0
    if len(ai_path) == 0:
        print("ai path len is 0")
        return

    real_spot_at_path = ai_spot_counter // LOOP_AT_EACH_MOVE_UPDATE
    cur_action = ai_path[real_spot_at_path]
    play_single_action(game, cur_action, player_num=AI_PLAYER_NUM)
    ai_spot_counter += 1


def play_single_action(game, cur_action, player_num=0):
    if cur_action == MOVE_LEFT:
        game.players[player_num].moving_left = True
        game.players[player_num].moving_right = False
    elif cur_action == MOVE_RIGHT:
        game.players[player_num].moving_right = True
        game.players[player_num].moving_left = False
    if cur_action == SHOOT and not game.players[player_num].weapon.is_active:
        game.players[player_num].moving_left = False
        game.players[player_num].moving_right = False
        game.players[player_num].shoot()


def handle_random_game_event(game, player_num=0):
    game.players[player_num].moving_left = random.getrandbits(1)
    game.players[player_num].moving_right = random.getrandbits(1)
    if random.getrandbits(1) and not game.players[player_num].weapon.is_active:
        game.players[player_num].shoot()
