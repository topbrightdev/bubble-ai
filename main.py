from gui import *
import sys


def start_player_game(heuristic):
    """
    starts a new game (not for data collection)
    :param heuristic:
    :return:
    """
    game, font, clock, screen, main_menu, load_level_menu = init_gui(heuristic=heuristic)
    start_main_menu(game, font, clock, screen, main_menu, load_level_menu)


## Create Data
def run_ai_game_and_return_data(level, heuristic, is_goal_func):
    """
    starts a game for data collection
    :param level: level to start with
    :param heuristic: the heuristic to be used
    :param is_goal_func: goal function
    :return:
    """
    game, font, clock, screen, main_menu, load_level_menu = init_gui(heuristic=heuristic)
    game.is_ai = True
    return start_level(level, game, font, clock, screen, main_menu, load_level_menu, heuristic=heuristic, calc_stats=True, is_goal_func=is_goal_func)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        heuristic = bonus_and_ball_but_not_too_close_heuristic
    else:
        heuristic = sys.argv[1]
        if heuristic == 'zero':
            heuristic = zero_heuristic
        elif heuristic == 'x_axis':
            heuristic = stay_in_ball_area_but_not_too_close_x_axis_not_admissible_heuristic
        elif heuristic == 'both_axes':
            heuristic = stay_in_ball_area_but_not_too_close_both_axis_not_admissible_heuristic
        elif heuristic == 'time':
            heuristic = time_from_bubble_and_player
        elif heuristic == 'bonus':
            heuristic = bonus_and_ball_but_not_too_close_heuristic
        elif heuristic == 'center':
            heuristic = stay_in_center_heuristic
        elif heuristic == 'small_balls':
            heuristic = shoot_on_small_balls_heuristic
        elif heuristic == 'shoot':
            heuristic = shoot_heuristic
        else:
            print('please choose heuristic from the list,\nif you dont know what to choose, '
                  'keep this arg empty.\n\nThe list:\nzero\nx_axis\nboth_axes\ntime\nbonus\ncenter\nsmall_balls\nshoot')
            exit()
    start_player_game(heuristic=heuristic)
