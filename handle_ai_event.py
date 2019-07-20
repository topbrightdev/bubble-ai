from a_star import *
from game import *
from heuristics import *

ai_spot_counter = 0
ai_path_size = 0
ai_path = None
AI_PLAYER_NUM = 0


def handle_ai_game_event(game):
    global ai_spot_counter, ai_path_size, ai_path
    # if we finish the current path, construct a new one
    if (ai_spot_counter // LOOP_AT_EACH_SUCCESSOR_UPDATES >= ai_path_size):
        ai_path, ai_path_size = a_star(game, goal=None, heuristic=blow_up_balls_and_dont_die) # TODO check what is goal, here
        ai_spot_counter = 0
    if len(ai_path) == 0:
        print("ai path len is 0")
        return

    real_spot_at_path = ai_spot_counter // LOOP_AT_EACH_SUCCESSOR_UPDATES
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