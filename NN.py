# -*- coding: utf-8 -*-
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from main import *
import pickle


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.999995 # TODO check if good
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(32, input_dim=self.state_size, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


def player_action(game, font, clock, screen, main_menu, load_level_menu):
    handle_game_event(game, font, clock, screen, main_menu, load_level_menu)
    if game.players[0].is_shoot:
        return 2
    elif game.players[0].moving_left:
        return 0
    elif game.players[0].moving_right:
        return 1
    else:
        return 3


def replay_load_level(level_arr, agent, replay_num, batch_size):
    for i in range(replay_num):
        print(i)
        for item in level_arr:
            state, action, reward, next_state, done = item
            agent.remember(state, action, reward, next_state, done)
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
    if RUN_LOCAL:
        agent.save("./save/bubble_nn-dqn_after_replay.h5")
    else:
        agent.save("./bubble_nn-dqn_after_replay.h5")


def train_agent_on_load_level(agent, batch_size):
    replay_num = 1
    won_levels = ["elad_level_1_total_reward_970_steps_131.arr", "elad_level_2_total_reward_1263_steps_388.arr",
                  "elad_level_3_total_reward_1159_steps_542.arr", "elad_level_4_total_reward_1321_steps_380.arr",
                  "elad_level_5_total_reward_1315_steps_686.arr", "elad_level_6_total_reward_1440_steps_911.arr"]
    loss_levels = ["elad_level_1_total_reward_-161_steps_62.arr", "elad_level_2_total_reward_-138_steps_89.arr",
                   "elad_level_3_total_reward_-143_steps_44.arr", "elad_level_4_total_reward_-160_steps_61.arr",
                   "elad_level_5_total_reward_-289_steps_190.arr", "elad_level_6_total_reward_-118_steps_19.arr"]
    all_levels = won_levels + loss_levels
    for loop in range(len(all_levels)*2):
        level_name = random.choice(all_levels)
        print(level_name)
        print(loop)
        if RUN_LOCAL:
            level_path = "./pickle/" + level_name
            with open(level_path, 'rb') as read_file:
                level_arr = pickle.load(read_file)
        else:
            level_path = "./" + level_name
            with open(level_path, 'rb') as read_file:
                level_arr = pickle.load(read_file)
        replay_load_level(level_arr, agent, replay_num, batch_size)


def create_new_play_level(level):
    done = False
    play_arr = []
    game, font, clock, screen, main_menu, load_level_menu = start_nn_game(level)
    total_game_reward = 0
    steps = 0

    state = game.get_represented_state()
    state = np.reshape(state, [1, state_size])
    while game.is_running:
        steps += 1
        cur_game_score = game.get_score()
        action = player_action(game, font, clock, screen, main_menu, load_level_menu)

        if action == 0:
            cur_action = MOVE_LEFT
        elif action == 1:
            cur_action = MOVE_RIGHT
        elif action == 2:
            cur_action = SHOOT
        elif action == 3:
            cur_action = STAY
            action = random.randint(0, 1)
        else:
            print("invalid action")
            cur_action = 0

        play_single_action(game, cur_action, AI_PLAYER_NUM)

        game.update() # TODO maybe add update_nn
        draw_world(game, font, clock, screen, main_menu, load_level_menu)

        next_state = game.get_represented_state()
        next_state = np.reshape(next_state, [1, state_size])
        if game.is_completed or game.level_completed:
            done = True
            reward = 1000
        elif game.game_over or game.dead_player:
            done = True
            reward = -100
        else:
            reward = (game.get_score() - cur_game_score) - EACH_TURN_REDUCE  # each turn cost
        total_game_reward += reward

        pygame.display.update()

        play_arr.append((state, action, reward, next_state, done))

        state = next_state
        if done:
            # pygame.quit()
            print("level: {}, score: {}, e: {:.2}, total_reward: {}, steps: {}"
                  .format(level, game.get_score(), agent.epsilon, total_game_reward, steps))
            try:
                file_name = "./pickle/elad_level_" + str(level) + "_total_reward_" + str(
                    total_game_reward) + "_steps_" + str(steps) + '.arr'
                with open(file_name, 'wb') as f:
                    pickle.dump(play_arr, f)
            except Exception as ex:
                print(ex)
                print("-----------------------------Pickle does not work-----------------------------")
            return


def train_agent_by_play(agent, batch_size):
    for e in range(EPISODES):
        done = False
        level = random.randint(1, 8)
        # level = 6
        if SHOW_NN_GUI:
            game, font, clock, screen, main_menu, load_level_menu = start_nn_game(level)
        else:
            game = start_nn_game_without_gui(level)

        total_game_reward = 0
        steps = 0

        state = game.get_represented_state()
        state = np.reshape(state, [1, state_size])
        while game.is_running:
            steps += 1
            cur_game_score = game.get_score()

            action = agent.act(state)

            if action == 0:
                cur_action = MOVE_LEFT
            elif action == 1:
                cur_action = MOVE_RIGHT
            elif action == 2:
                cur_action = SHOOT
            else:
                print("invalid action")
                cur_action = ''
            play_single_action(game, cur_action, AI_PLAYER_NUM)

            game.update()
            if SHOW_NN_GUI:
                draw_world(game, font, clock, screen, main_menu, load_level_menu)

            next_state = game.get_represented_state()
            next_state = np.reshape(next_state, [1, state_size])
            if game.is_completed or game.level_completed:
                done = True
                reward = 1000
            elif game.game_over or game.dead_player:
                done = True
                reward = -100
            else:
                reward = (game.get_score() - cur_game_score) - EACH_TURN_REDUCE  # each turn cost
            total_game_reward += reward
            if SHOW_NN_GUI:
                pygame.display.update()

            agent.remember(state, action, reward, next_state, done)

            state = next_state
            if done:
                # pygame.quit()
                print("episode: {}/{}, level: {}, score: {}, e: {:.2}, total_reward: {}, steps: {}"
                      .format(e, EPISODES, level, game.get_score(), agent.epsilon, total_game_reward, steps))

            if len(agent.memory) > batch_size or done:
                agent.replay(batch_size)
                if done:
                    break
        if e % 1000 == 0:
            if RUN_LOCAL:
                agent.save("/mnt/ssd/OTHER/tmp/e" + str(e) + "_l" + str(level) + "_s" + str(
                    game.get_score()) + "_.h5")
            else:
                agent.save(
                    "./bubble_nn-dqn_e" + str(e) + "_level" + str(level) + "_score" + str(game.get_score()) + "_.h5")


if __name__ == "__main__":
    state_size = STATE_LEN # TODO
    action_size = ACTIONS_LEN # TODO
    agent = DQNAgent(state_size, action_size)
    agent_name = "bubble_nn-dqn_after_replay.h5"
    if RUN_LOCAL:
        # agent.load("./save/" + agent_name)
        pass
    else:
        # agent.load("./" + agent_name)
        pass
    batch_size = 32 # TODO check if good

    if PLAY_LOAD_LEVEL:
        train_agent_on_load_level(agent, batch_size)
    elif PLAY_BY_MYSELF:
        level = 6
        create_new_play_level(level)
    else:
        train_agent_by_play(agent, batch_size)
