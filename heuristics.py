import math

def dont_die_heuristic(game):
    closest_ball = game.balls[0]
    for ball in game.balls:
        if distance_between_ball_and_player(ball, game) < distance_between_ball_and_player(closest_ball, game):
            closest_ball = ball
    return -closest_ball * 100

def distance_between_ball_and_player(ball, game, index = 0):
    distance_x = ball.rect.centerx - game.players[index].rect.centerx
    distance_y = ball.rect.centery - game.players[index].rect.centery
    return math.sqrt(math.pow(distance_x, 2) + math.pow(distance_y, 2))

