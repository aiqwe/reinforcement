from kaggle_environments import make
import gym


class ConnectX(gym.Env):
    def __init__(self, switch_prob=0.5):
        self.env = make('connectx', debug=False)
        self.pair = [None, 'random']
        self.model_train = self.env.train(self.pair)

        self.action_space = gym.spaces.Discrete(self.env.configuration.columns)
        self.observation_space = gym.spaces.Discrete(self.env.configuration.columns * self.env.configuration.rows)

    def step(self, action):
        return self.model_train.step(action)

    def reset(self):
        return self.model_train.reset()