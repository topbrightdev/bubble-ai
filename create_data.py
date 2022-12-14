import pandas as pd
import main
from heuristics import *


ALL_HEURISTICS = [
    (stay_in_ball_area_but_not_too_close_heuristic_time_admissible, "stay_in_ball_area_but_not_too_close_heuristic_time_admissible"),
    (stay_in_ball_area_but_not_too_close_x_axis_not_admissible_heuristic, "stay_in_ball_area_but_not_too_close_x_axis_not_admissible_heuristic"),
    (stay_in_ball_area_but_not_too_close_both_axis_not_admissible_heuristic, "stay_in_ball_area_but_not_too_close_both_axis_not_admissible_heuristic"),
    (bonus_and_ball_but_not_too_close_heuristic, "bonus_and_ball_but_not_too_close_heuristic"),
    (stay_in_center_heuristic, "stay_in_center_heuristic"),
    (shoot_on_small_balls_heuristic, "shoot_on_small_balls_heuristic"),
    (shoot_heuristic, "shoot_heuristic"),
    (zero_heuristic, "zero_heuristic")
    ]

MAX_STEPS_OPTION = list(range(1,11))
NUM_OF_LOOPS_FOR_EACH_HEURISTIC = 10
# goal func, to run stats of
IS_GOAL_FUNC = is_sub_goal_steps_score_bonuses

HEURISTIC_FOLDER = 'heuristics_data/'
CSV_SUF = '.csv'
FINAL_DF_NAME = 'all_heuristics_data'

OPEN_NODES_AXIS = 'open_nodes'
FINAL_LEVEL_AXIS = 'last_level_reached'
FINAL_SCORE_AXIS = 'final_score'
PLAYER_DIES_COUNT_AXIS = 'player_dies_count'

TOTAL_OPEN_NODES = 'total_open_nodes'
MAX_OPEN_NODES = 'max_open_nodes'
MEAN_OPEN_NODES = 'mean_open_nodes'
COUNT_OPEN_NODES = 'count_open_nodes'
MEDIAN_OPEN_NODES = 'median_open_nodes'
FINAL_LEVEL = 'final_level'
PLAYER_DIES_COUNT = 'player_dies_count'
FINAL_SCORE = 'final_score'
FINAL_PLAYER_LIVES = 'final_player_lives'
MAX_PATH_SIZE_COL = 'max_path_size'
LOOP_AT_EACH_MOVE_UPDATE_COL = 'loop_at_each_update'
HEURISTIC_COL = 'heuristic'


def generate_data_from_csv(file_path):
    """
    generate all heuristics data from a given path.
    :param file_path: path to a csv file, that contains heuristics data - created by create_heuristic_data
    :return: dataframe that represent the data
    """
    df = pd.read_csv(file_path)
    total_open_nodes = df[OPEN_NODES_AXIS].sum()
    max_open_nodes = df[OPEN_NODES_AXIS].max()
    mean_open_nodes = df[OPEN_NODES_AXIS].mean()
    count_open_nodes = df[OPEN_NODES_AXIS].count()
    median_open_nodes = df[OPEN_NODES_AXIS].median()
    final_level = df[FINAL_LEVEL_AXIS].unique()[0]
    player_dies_count = df[PLAYER_DIES_COUNT_AXIS].unique()[0]
    final_player_lives = df[FINAL_PLAYER_LIVES].unique()[0]
    final_score = df[FINAL_SCORE_AXIS].unique()[0]
    max_path_size = df[MAX_PATH_SIZE_COL].unique()[0]

    cur_dict = {TOTAL_OPEN_NODES: total_open_nodes,
               MAX_OPEN_NODES: [max_open_nodes],
               MEAN_OPEN_NODES: [mean_open_nodes],
               COUNT_OPEN_NODES: [count_open_nodes],
               MEDIAN_OPEN_NODES: [median_open_nodes],
               FINAL_LEVEL: [final_level],
                FINAL_SCORE: [final_score],
                MAX_PATH_SIZE_COL: [max_path_size],
                PLAYER_DIES_COUNT: [player_dies_count],
                FINAL_PLAYER_LIVES: [final_player_lives]}
    df_row = pd.DataFrame(cur_dict)
    return df_row


def create_heuristic_data(heuristic, file_path, is_goal_func, max_steps):
    """
    create heuristic statistics data, save as csv file, and return the resulted dataframe
    :param heuristic: heuristic to calc stats on
    :param file_path: a path to save the csv data to
    :param is_goal_func: goal function to calc data on
    :param max_steps: max a_star depth
    :return: a dataframe representing the data
    """
    STARTING_LEVEL = 1
    cur_goal_func = lambda x, y: is_goal_func(x, y, max_steps)
    list_of_open_nodes, final_level, final_score, player_dies_count, final_lives = \
        main.run_ai_game_and_return_data(STARTING_LEVEL, heuristic, cur_goal_func)
    df = pd.DataFrame(list_of_open_nodes, columns=[OPEN_NODES_AXIS])
    df[FINAL_LEVEL_AXIS] = final_level
    df[FINAL_SCORE_AXIS] = final_score
    df[MAX_PATH_SIZE_COL] = max_steps
    df[PLAYER_DIES_COUNT_AXIS] = player_dies_count
    df[FINAL_PLAYER_LIVES] = final_lives

    ensure_dir_exists(file_path)
    df.to_csv(file_path, index=False)

    return generate_data_from_csv(file_path)


def create_list_of_heuristics_data(heuristics):
    """
    create heuristics statistics data, from a given heuristic list.
    save the data as csv file, and return the resulted dataframe
    :param heuristics: heuristic to calc stats on
    :return: a dataframe representing the data
    """
    all_heuristics_df = pd.DataFrame(columns=[TOTAL_OPEN_NODES, MAX_OPEN_NODES, MEAN_OPEN_NODES, COUNT_OPEN_NODES,
                                            MEDIAN_OPEN_NODES, FINAL_LEVEL, FINAL_SCORE, MAX_PATH_SIZE_COL, PLAYER_DIES_COUNT, FINAL_PLAYER_LIVES, HEURISTIC_COL])
    for (heuristic, heuristic_name) in heuristics:
        cur_heuristic_df = pd.DataFrame(columns=[TOTAL_OPEN_NODES, MAX_OPEN_NODES, MEAN_OPEN_NODES, COUNT_OPEN_NODES,
                                               MEDIAN_OPEN_NODES, FINAL_LEVEL, FINAL_SCORE, MAX_PATH_SIZE_COL, PLAYER_DIES_COUNT, FINAL_PLAYER_LIVES])
        for iter in range(1, NUM_OF_LOOPS_FOR_EACH_HEURISTIC + 1):
            for num_step in MAX_STEPS_OPTION:
                print(heuristic_name)
                print('iteration: ', str(iter))
                print('num of steps', str(num_step))
                iter_file_path = HEURISTIC_FOLDER + heuristic_name + ('/iter_%s_steps_%s' % (iter, num_step)) + CSV_SUF
                cur_df_row = create_heuristic_data(heuristic, iter_file_path, IS_GOAL_FUNC, num_step)
                cur_heuristic_df = cur_heuristic_df.append(cur_df_row, ignore_index=True)

        cur_heuristic_df[HEURISTIC_COL] = heuristic_name

        heuristic_file_path = HEURISTIC_FOLDER + heuristic_name + '/' + heuristic_name + CSV_SUF
        ensure_dir_exists(heuristic_file_path)
        cur_heuristic_df.to_csv(heuristic_file_path, index=False)

        all_heuristics_df = all_heuristics_df.append(cur_heuristic_df, ignore_index=True)

    all_heuristics_file_path = HEURISTIC_FOLDER + FINAL_DF_NAME + CSV_SUF
    ensure_dir_exists(all_heuristics_file_path)
    all_heuristics_df.to_csv(all_heuristics_file_path, index=False)

    return pd.read_csv(all_heuristics_file_path)


def ensure_dir_exists(file_path):
    """
    ensure that the given path exists, and if not - create the path
    :param file_path: path to file
    :return: None
    """
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))


if __name__ == '__main__':
    create_list_of_heuristics_data(ALL_HEURISTICS)
