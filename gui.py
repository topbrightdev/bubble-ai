from pygame.locals import *
from collections import OrderedDict

from menu import *
from handle_ai_event import *
total_open_nodes = 0


def init_gui():
    pygame.init()
    pygame.display.set_caption('Bubble Trouble')
    pygame.mouse.set_visible(True)
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('monospace', 30)
    game = Game()

    main_menu = Menu(
        screen, OrderedDict(
            [('Single Player', start_single_player_level_menu),
                ('Two Players', start_multiplayer_level_menu),
                ('AI Player', start_ai_player_level_menu),
                ('Quit', quit_game)]
        )
    )
    levels_available = [(str(lvl), (start_level, lvl))
                        for lvl in range(1, game.max_level_available + 1)]
    levels_available.append(('Back', back))
    load_level_menu = Menu(screen, OrderedDict(levels_available))

    return game, font, clock, screen, main_menu, load_level_menu


def start_level(level, game, font, clock, screen, main_menu, load_level_menu,
                calc_stats=False,
                heuristic=stay_in_ball_area_but_not_too_close_x_axis_not_admissible_heuristic,
                is_goal_func=is_sub_goal_steps_score_bonuses):
    if calc_stats:
        cur_level = level # TODO
        list_of_open_nodes = []
    game.load_level(level)
    main_menu.is_active = False
    pygame.mouse.set_visible(False)
    while game.is_running:
        game.update()
        if calc_stats:
            if game.level_completed or game.is_completed: # TODO
                print("------------------Finished level %s------------------" % cur_level) # TODO
                cur_level += 1 # TODO
            if game.is_completed or game.game_over:
                final_score = game.get_score()
                return list_of_open_nodes, cur_level, final_score
        draw_world(game, font, clock, screen, main_menu, load_level_menu)
        pygame.display.update()
        if calc_stats:
            cur_open_nodes = handle_game_event(game, font, clock, screen, main_menu, load_level_menu, heuristic,
                                               calc_stats, is_goal_func) # TODO
            if cur_open_nodes != 0:
                list_of_open_nodes.append(cur_open_nodes) # TODO
        else:
            handle_game_event(game, font, clock, screen, main_menu, load_level_menu, heuristic=heuristic, is_goal_func=is_goal_func) # TODO
        if game.is_completed or game.game_over or \
                game.level_completed or game.is_restarted:
            pygame.time.delay(3000)
        if game.dead_player:
            pygame.time.delay(1000)
        if game.is_restarted:
            game.is_restarted = False


def start_main_menu(game, font, clock, screen, main_menu, load_level_menu):
    main_menu.is_active = True
    while main_menu.is_active:
        main_menu.draw()
        handle_menu_event(main_menu, game, font, clock, screen, main_menu, load_level_menu)
        pygame.display.update()


def start_load_level_menu(game, font, clock, screen, main_menu, load_level_menu):
    load_level_menu.is_active = True
    while load_level_menu.is_active:
        load_level_menu.draw()
        handle_menu_event(load_level_menu, game, font, clock, screen, main_menu, load_level_menu)
        pygame.display.update()


def start_single_player_level_menu(game, font, clock, screen, main_menu, load_level_menu):
    game.is_multiplayer = False
    start_load_level_menu(game, font, clock, screen, main_menu, load_level_menu)


def start_ai_player_level_menu(game, font, clock, screen, main_menu, load_level_menu):
    game.is_multiplayer = False
    game.is_ai = True
    start_load_level_menu(game, font, clock, screen, main_menu, load_level_menu)


def start_multiplayer_level_menu(game, font, clock, screen, main_menu, load_level_menu):
    game.is_multiplayer = True
    start_load_level_menu(game, font, clock, screen, main_menu, load_level_menu)


def quit_game(game, font, clock, screen, main_menu, load_level_menu):
    pygame.quit()
    sys.exit()


def back(game, font, clock, screen, main_menu, load_level_menu):
    load_level_menu.is_active = False


def draw_ball(ball, game, font, clock, screen, main_menu, load_level_menu):
    screen.blit(ball.image, ball.rect)


def draw_hex(hexagon, game, font, clock, screen, main_menu, load_level_menu):
    screen.blit(hexagon.image, hexagon.rect)


def draw_player(player, game, font, clock, screen, main_menu, load_level_menu):
    screen.blit(player.image, player.rect)


def draw_weapon(weapon, game, font, clock, screen, main_menu, load_level_menu):
    screen.blit(weapon.image, weapon.rect)


def draw_bonus(bonus, game, font, clock, screen, main_menu, load_level_menu):
    screen.blit(bonus.image, bonus.rect)


def draw_message(message, colour, game, font, clock, screen, main_menu, load_level_menu):
    label = font.render(message, 1, colour)
    rect = label.get_rect()
    rect.centerx = screen.get_rect().centerx
    rect.centery = screen.get_rect().centery
    screen.blit(label, rect)


def draw_timer(game, font, clock, screen, main_menu, load_level_menu):
    timer = font.render(str(game.get_time_left()), 1, BLACK)
    rect = timer.get_rect()
    rect.bottomleft = 10, WINDOWHEIGHT - 10
    screen.blit(timer, rect)


def draw_score(game, font, clock, screen, main_menu, load_level_menu):
    score = font.render("score: " + str(game.get_score()), 1, BLUE)
    rect = score.get_rect()
    rect.topright = WINDOWWIDTH - 10, 10
    screen.blit(score, rect)


def draw_players_lives(player, game, font, clock, screen, main_menu, load_level_menu, is_main_player=True):
    player_image = pygame.transform.scale(player.image, (20, 20))
    rect = player_image.get_rect()
    for life_num in range(player.lives):
        if not is_main_player:
            screen.blit(player_image, ((life_num + 1) * 20, 10))
        else:
            screen.blit(
                player_image,
                (WINDOWWIDTH - (life_num + 1) * 20 - rect.width, 10)
            )


def draw_world(game, font, clock, screen, main_menu, load_level_menu):
    #screen.fill(WHITE)
    image = pygame.image.load(IMAGES_PATH + 'background_level.png')
    screen.blit(image,(0,0))
    for hexagon in game.hexagons:
        draw_hex(hexagon, game, font, clock, screen, main_menu, load_level_menu)
    for ball in game.balls:
        draw_ball(ball, game, font, clock, screen, main_menu, load_level_menu)
    for player_index, player in enumerate(game.players):
        if player.weapon.is_active:
            draw_weapon(player.weapon, game, font, clock, screen, main_menu, load_level_menu)
        draw_player(player, game, font, clock, screen, main_menu, load_level_menu)
        draw_players_lives(player, game, font, clock, screen, main_menu, load_level_menu, player_index)
    for bonus in game.bonuses:
        draw_bonus(bonus, game, font, clock, screen, main_menu, load_level_menu)
    draw_timer(game, font, clock, screen, main_menu, load_level_menu)
    draw_score(game, font, clock, screen, main_menu, load_level_menu)
    if game.game_over:
        draw_message('Game over!', RED, game, font, clock, screen, main_menu, load_level_menu)
        pygame.display.update()
        pygame.time.delay(3000)
        print('cur level is: ', str(game.level))
        print("number of open nodes: %s" % total_open_nodes)
        print('time left: ',str(game.get_time_left()))
        print('lost!')
        print('score is: ', str(game.get_score()))
        start_main_menu(Game(), font, clock, screen, main_menu, load_level_menu)
    if game.is_completed:
        draw_message('Congratulations! You won!!!', PURPLE, game, font, clock, screen, main_menu, load_level_menu)
        pygame.display.update()
        pygame.time.delay(3000)
        print('cur level is: ', str(game.level))
        print("number of open nodes: %s" % total_open_nodes)
        print('time left: ', str(game.get_time_left()))
        print('win!')
        game.add_to_score(TIME_LEFT_SCORE_FACTOR * game.get_time_left())
        print('score is: ', str(game.get_score()))
        start_main_menu(Game(), font, clock, screen, main_menu, load_level_menu)
    if game.level_completed and not game.is_completed:
        draw_message('Well done! Level completed!', BLUE, Game(), font, clock, screen, main_menu, load_level_menu)
    if game.is_restarted:
        draw_message('Get ready!', BLUE, Game(), font, clock, screen, main_menu, load_level_menu)



def handle_game_event(game, font, clock, screen, main_menu, load_level_menu, heuristic=None, calc_stats=False, is_goal_func=None):
    if game.is_ai and not game.is_nn:
        global total_open_nodes
        if heuristic is None:
            raise ValueError("You Have to give heuristic if you want to use AI player")
        open_nodes = handle_ai_game_event(game, font, clock, screen, main_menu, load_level_menu, heuristic, is_goal_func)
        total_open_nodes += open_nodes
        return open_nodes
        # for event in pygame.event.get():
        #     # TODO maybe dont need quit option
        #     if event.type == KEYDOWN and event.key == K_ESCAPE:
        #         quit_game(game, font, clock, screen, main_menu, load_level_menu)
    else:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    game.players[0].moving_left = True
                elif event.key == K_RIGHT:
                    game.players[0].moving_right = True
                elif event.key == K_SPACE and not game.players[0].weapon.is_active:
                    game.players[0].is_shoot = True
                    game.players[0].shoot()
                elif event.key == K_ESCAPE:
                    quit_game(game, font, clock, screen, main_menu, load_level_menu)
                if game.is_multiplayer:
                    if event.key == K_a:
                        game.players[1].moving_left = True
                    elif event.key == K_d:
                        game.players[1].moving_right = True
                    elif event.key == K_LCTRL and \
                            not game.players[1].weapon.is_active:
                        game.players[1].shoot()
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    game.players[0].moving_left = False
                elif event.key == K_RIGHT:
                    game.players[0].moving_right = False
                elif event.key == K_SPACE:
                    game.players[0].is_shoot = False
                if game.is_multiplayer:
                    if event.key == K_a:
                        game.players[1].moving_left = False
                    elif event.key == K_d:
                        game.players[1].moving_right = False
            if event.type == QUIT:
                quit_game(game, font, clock, screen, main_menu, load_level_menu)


def handle_menu_event(menu, game, font, clock, screen, main_menu, load_level_menu):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game(game, font, clock, screen, main_menu, load_level_menu)

        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if menu == main_menu:
                    quit_game(game, font, clock, screen, main_menu, load_level_menu)
                else:
                    start_main_menu(game, font, clock, screen, main_menu, load_level_menu)
            if (event.key == pygame.K_UP or event.key == pygame.K_DOWN)\
                    and menu.current_option is None:
                menu.current_option = 0
                pygame.mouse.set_visible(False)
            elif event.key == pygame.K_UP and menu.current_option > 0:
                menu.current_option -= 1
            elif event.key == pygame.K_UP and menu.current_option == 0:
                menu.current_option = len(menu.options) - 1
            elif event.key == pygame.K_DOWN \
                    and menu.current_option < len(menu.options) - 1:
                menu.current_option += 1
            elif event.key == pygame.K_DOWN \
                    and menu.current_option == len(menu.options) - 1:
                menu.current_option = 0
            elif event.key == pygame.K_RETURN and \
                    menu.current_option is not None:
                option = menu.options[menu.current_option]
                if not isinstance(option.function, tuple):
                    option.function()
                else:
                    option.function[0](option.function[1])

        elif event.type == MOUSEBUTTONUP:
            for option in menu.options:
                if option.is_selected:
                    if not isinstance(option.function, tuple):
                        option.function(game, font, clock, screen, main_menu, load_level_menu)
                    else:
                        option.function[0](option.function[1], game, font, clock, screen, main_menu, load_level_menu)

        if pygame.mouse.get_rel() != (0, 0):
            pygame.mouse.set_visible(True)
            menu.current_option = None
