BALL_WORTH_BY_SIZE = {1: 1,
                      2: 3,
                      3: 7,
                      4: 15,
                      5: 31}


def g_function_by_score_and_time(game):
    return game.get_score() + game.time_left


def is_sub_goal_by_score(game, start):
    return game.get_score() > start.get_score()


def is_sub_goal_by_blow_up_ball(game, start):
    return calc_worth_of_balls(game) < calc_worth_of_balls(start)


# TODO implement efficient
def calc_worth_of_balls(game):
    worth = 0
    for ball in game.balls + game.hexagons:
        worth += BALL_WORTH_BY_SIZE[ball.size]
    return worth
