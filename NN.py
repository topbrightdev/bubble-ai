# -*- coding: utf-8 -*-
import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from main import *

EPISODES = 1000
SHOW_NN_GUI = False


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
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


if __name__ == "__main__":
    state_size = STATE_LEN # TODO
    action_size = 3 # TODO
    agent = DQNAgent(state_size, action_size)
    agent.load("./save/bubble_nn-dqn60.h5")
    batch_size = 32 # TODO

    for e in range(EPISODES):
        done = False
        level = random.randint(1,7)
        if SHOW_NN_GUI:
            game, font, clock, screen, main_menu, load_level_menu = start_nn_game(level)
        else:
            game = start_nn_game_without_gui(level)

        while game.is_running:
            game.update()
            if SHOW_NN_GUI:
                draw_world(game, font, clock, screen, main_menu, load_level_menu)

            state = game.get_represented_state()
            state = np.reshape(state, [1, state_size])
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
                cur_action = 0
            play_single_action(game, cur_action, AI_PLAYER_NUM)
            next_state = game.get_represented_state()
            next_state = np.reshape(next_state, [1, state_size])
            reward = game.get_score() - cur_game_score
            if game.is_completed or game.game_over or \
                    game.level_completed or game.dead_player:
                done = True
                reward = -500

            if SHOW_NN_GUI:
                pygame.display.update()

            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                # pygame.quit()
                print("episode: {}/{}, level: {}, score: {}, e: {:.2}"
                      .format(e, EPISODES, level, game.get_score(), agent.epsilon))
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
        if e % 10 == 0:
            agent.save("./save/bubble_nn-dqn_e_"+str(e)+"_score"+str(game.get_score())+"_.h5")
