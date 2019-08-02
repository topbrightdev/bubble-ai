# -*- coding: utf-8 -*-
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from main import *


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.99    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.9995 # TODO check if good
        self.learning_rate = 0.002
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

def player_action():
    handle_game_event(game, font, clock, screen, main_menu, load_level_menu)
    if game.players[0].moving_left:
        return 0
    elif game.players[0].moving_right:
        return 1
    elif game.players[0].is_shoot:
        return 2
    else:
        return 3

if __name__ == "__main__":
    state_size = STATE_LEN # TODO
    action_size = ACTIONS_LEN # TODO
    agent = DQNAgent(state_size, action_size)
    agent_name = "bubble_nn-dqn.h5"
    if RUN_LOCAL:
        # agent.load("./save/" + agent_name)
        pass
    else:
        # agent.load("./" + agent_name)
        pass
    batch_size = 32 # TODO check if good

    if PLAY_BY_MYSELF:
        play_arr = []
    for e in range(EPISODES):
        done = False
        level = random.randint(1, 7)
        # level = 5
        if SHOW_NN_GUI:
            game, font, clock, screen, main_menu, load_level_menu = start_nn_game(level)
        else:
            game = start_nn_game_without_gui(level)

        total_game_reward = 0
        while game.is_running:
            cur_game_score = game.get_score()

            state = game.get_represented_state()
            state = np.reshape(state, [1, state_size])
            if PLAY_BY_MYSELF:
                action = player_action()
            else:
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
                reward = (game.get_score() - cur_game_score) -0.5 #each turn cost
            total_game_reward += reward
            if SHOW_NN_GUI:
                pygame.display.update()

            if PLAY_BY_MYSELF:
                play_arr.append((state, action, reward, next_state, done))
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                # pygame.quit()
                print("episode: {}/{}, level: {}, score: {}, e: {:.2}, total_reward: {}"
                      .format(e, EPISODES, level, game.get_score(), agent.epsilon, total_game_reward))
                # if PLAY_BY_MYSELF:
                    # with open("play_by_myself_level_"+str(level)+"_total_reward_"+str(total_game_reward), 'w') as f:
                    #     for item in play_arr:
                    #         f.write("%s\n" % item)
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
        if PLAY_BY_MYSELF:
            for i in range(5):
                for item in play_arr:
                    state, action, reward, next_state, done = item
                    agent.remember(state, action, reward, next_state, done)
                    if len(agent.memory) > batch_size:
                        agent.replay(batch_size)
        if e % 50 == 0:
            if RUN_LOCAL:
                agent.save("./save/bubble_nn-dqn_e"+str(e)+"_level"+str(level)+"_score"+str(game.get_score())+"_.h5")
                pass
            else:
                agent.save("./bubble_nn-dqn_e"+str(e)+"_level"+str(level)+"_score"+str(game.get_score())+"_.h5")
                pass
