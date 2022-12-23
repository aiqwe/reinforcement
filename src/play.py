import gym
from . import environment

class Play:

    def __init__(self, env, TrainNet, TargetNet, epsilon_greedy, copy_step):
        self.env = env
        self.TrainNet = TrainNet
        self.TargetNet = TargetNet
        self.epsilon_greedy = epsilon_greedy
        self.copy_step = copy_step

    def play_game(self):
        rewards = 0
        cnt = 0
        done = False
        obs = self.env.reset()
        # obs = self.state

        while not done:
            action = self.TrainNet.get_action(obs, self.epsilon_greedy)
            prev_obs = obs
            obs, reward, done, _ = self.env.step(action)

            # Reward Rules
            if done:
                if reward == 1:
                    reward = 1
                elif reward == 0:
                    reward = -1
                else:
                    reward = 0
            else:
                reward = 0

            rewards += reward

            buffer = {'s': prev_obs, 'a': action, 'r': reward, 's_next': obs, 'done': done}
            self.TrainNet.add_buffer(buffer)
            self.TrainNet.train(self.TargetNet)
            cnt += 1
            if cnt % self.copy_step == 0:
                self.TargetNet.copy_weights(self.TrainNet)
        return rewards


