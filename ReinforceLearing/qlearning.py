import basic
import numpy as np


class QLearning(basic.WithoutModel):
    def __init__(self, obstacle_reward, final_reward, loop_time=100000, alpha=0.5, gamma=0.5, epsilon=0.5):
        super(QLearning, self).__init__(obstacle_reward, final_reward, loop_time, epsilon)

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.loop_time = loop_time
        self.init_map()
        print(self.reward_map)

    def generate_action_map(self):
        for i in range(10):
            for j in range(15):
                if (self.map2array(i, j) == self.obstacles_series).any():
                    continue
                else:
                    self.action_map[i, j] = self.policy([i, j], 'greedy')

    def loop(self):
        loop_time = 0
        while True:
            # index = np.random.randint(self.map_size[0]*self.map_size[1])
            # if (index == self.obstacles_series).any():
            if False:
                continue
            else:
                loop_time += 1
                # state = np.array(self.array2map(index))
                state = np.array([0, 0])

                mini_loop = 0
                while True:
                    action = self.policy(state, 'epsilon_greedy')

                    state_ = state + self.action[int(action)]
                    reward = self.reward_map[state_[0] + 1, state_[1] + 1]
                    if not self.is_obstacle(state_):
                        mini_loop += 1
                        # print(state_)

                        action_ = self.policy(state_, 'greedy')
                        tmp = self.gamma * self.Q[state_[0], state_[1], action_] - self.Q[state[0], state[1], action]
                        # print(tmp, reward)
                        self.Q[state[0], state[1], action] += self.alpha * (reward + tmp)
                        state = state_
                    else:
                        # reward = self.reward_map[state_[0] + 1, state_[1] + 1]
                        # self.Q[state[0], state[1], action] += self.alpha * reward
                        self.Q[state[0], state[1], action] += self.alpha * (reward - self.Q[state[0], state[1], action])
                        break

            print("loop_time", loop_time)
            if loop_time > self.loop_time:

                break

if __name__ == "__main__":
    agent = QLearning(-100, 500, 2500, 0.5, 0.9, 0.5)
    agent.loop()
    agent.generate_action_map()
    # print(agent.Q)
    print(agent.action_map)

    view = basic.ViewGame(agent.action_map)
    view.screen()
