from pygame.locals import *
from collections import OrderedDict

from game import *
from menu import *

pygame.init()
pygame.display.set_caption('Bubble Trouble')
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('monospace', 30)
game = Game()


def start_level(level):
    game.load_level(level)
    main_menu.is_active = False
    pygame.mouse.set_visible(False)
    while game.is_running:
        game.update()
        draw_world()
        handle_game_event()
        pygame.display.update()
        if game.is_completed or game.game_over or \
                game.level_completed or game.is_restarted:
            pygame.time.delay(3000)
        if game.dead_player:
            pygame.time.delay(1000)
        if game.is_restarted:
            game.is_restarted = False
            game._start_timer()
        clock.tick(FPS)


def start_main_menu():
    while main_menu.is_active:
        main_menu.draw()
        handle_menu_event(main_menu)
        pygame.display.update()
        clock.tick(FPS)


def start_load_level_menu():
    load_level_menu.is_active = True
    while load_level_menu.is_active:
        load_level_menu.draw()
        handle_menu_event(load_level_menu)
        pygame.display.update()
        clock.tick(FPS)


def start_single_player_level_menu():
    game.is_multiplayer = False
    start_load_level_menu()


def start_ai_player_level_menu():
    game.is_multiplayer = False
    game.is_ai = True
    start_load_level_menu()


def start_multiplayer_level_menu():
    game.is_multiplayer = True
    start_load_level_menu()


def quit_game():
    pygame.quit()
    sys.exit()


def back():
    load_level_menu.is_active = False

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


def draw_ball(ball):
    screen.blit(ball.image, ball.rect)


def draw_hex(hexagon):
    screen.blit(hexagon.image, hexagon.rect)


def draw_player(player):
    screen.blit(player.image, player.rect)


def draw_weapon(weapon):
    screen.blit(weapon.image, weapon.rect)


def draw_bonus(bonus):
    screen.blit(bonus.image, bonus.rect)


def draw_message(message, colour):
    label = font.render(message, 1, colour)
    rect = label.get_rect()
    rect.centerx = screen.get_rect().centerx
    rect.centery = screen.get_rect().centery
    screen.blit(label, rect)


def draw_timer():
    timer = font.render(str(game.time_left), 1, RED)
    rect = timer.get_rect()
    rect.bottomleft = 10, WINDOWHEIGHT - 10
    screen.blit(timer, rect)


def draw_score():
    score = font.render("score: " + str(game.get_score()), 1, BLUE)
    rect = score.get_rect()
    rect.topright = WINDOWWIDTH - 10, 10
    screen.blit(score, rect)


def draw_players_lives(player, is_main_player=True):
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


def draw_world():
    screen.fill(WHITE)
    for hexagon in game.hexagons:
        draw_hex(hexagon)
    for ball in game.balls:
        draw_ball(ball)
    for player_index, player in enumerate(game.players):
        if player.weapon.is_active:
            draw_weapon(player.weapon)
        draw_player(player)
        draw_players_lives(player, player_index)
    for bonus in game.bonuses:
        draw_bonus(bonus)
    draw_timer()
    draw_score()
    if game.game_over:
        draw_message('Game over!', RED)
        start_main_menu()
    if game.is_completed:
        game.add_to_score(10*game.get_time_left())
        draw_message('Congratulations! You win!!!', PURPLE)
        start_main_menu()
    if game.level_completed and not game.is_completed:
        game.add_to_score(10*game.get_time_left())
        draw_message('Well done! Level completed!', BLUE)
    if game.is_restarted:
        draw_message('Get ready!', BLUE)


def handle_game_event():
    if game.is_ai:
        handle_ai_game_event()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                game.players[0].moving_left = True
            elif event.key == K_RIGHT:
                game.players[0].moving_right = True
            elif event.key == K_SPACE and not game.players[0].weapon.is_active:
                game.players[0].shoot()
            elif event.key == K_ESCAPE:
                quit_game()
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
            if game.is_multiplayer:
                if event.key == K_a:
                    game.players[1].moving_left = False
                elif event.key == K_d:
                    game.players[1].moving_right = False
        if event.type == QUIT:
            quit_game()


def handle_ai_game_event():
    game.players[0].moving_left = random.getrandbits(1)
    game.players[0].moving_right = random.getrandbits(1)
    if random.getrandbits(1) and not game.players[0].weapon.is_active:
        game.players[0].shoot()


def handle_menu_event(menu):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if menu == main_menu:
                    quit_game()
                else:
                    start_main_menu()
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
                        option.function()
                    else:
                        option.function[0](option.function[1])

        if pygame.mouse.get_rel() != (0, 0):
            pygame.mouse.set_visible(True)
            menu.current_option = None
