import numpy as np

class Agent:

    def __init__(self, TrainNet):
        self.TrainNet = TrainNet

    def agent(self, observation, configuration):
        state = observation.board[:]
        state.append(observation.mark)

        out = self.TrainNet.predict(np.atleast_2d(self.TrainNet.preprocess(observation)))[0].detach().numpy()

        for i in range(configuration.columns):
            if observation.board[i] != 0:
                out[i] = -1e7

        return int(np.argmax(out))