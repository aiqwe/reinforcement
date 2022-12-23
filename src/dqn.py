import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random


class Network(nn.Module):
    def __init__(self, input_state: int, output_action: int, hidden_layer: list):
        super(Network, self).__init__()
        self.fc = nn.ModuleList([])
        self.fc = self.fc.append(nn.Linear(input_state + 1, hidden_layer[0]))
        for i in range(1, len(hidden_layer)):
            self.fc.append(nn.Linear(hidden_layer[i - 1], hidden_layer[i]))
        self.output_layer = nn.Linear(hidden_layer[-1], output_action)

    def forward(self, x):
        for layer in self.fc:
            x = torch.tanh(layer(x))
        x = self.output_layer(x)
        return x

    def sample_action(self, obs, epsilon_greedy):
        out = self.forward(obs)
        prob = random.random()
        if prob < epsilon_greedy:
            return random.randint(0, 1)
        else:
            return out.argmax().item()


class DQN:
    def __init__(self, state_n, action_n, hidden_layer, gamma, max_buffer, min_buffer, batch_size, lr):
        self.action_n = action_n
        self.batch_size = batch_size
        self.gamma = gamma
        self.model = Network(input_state=state_n, hidden_layer=hidden_layer, output_action=action_n)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        self.replay_buffer = {'s': [], 'a': [], 'r': [], 's_next': [], 'done': []}  # The buffer
        self.max_buffer = max_buffer
        self.min_buffer = min_buffer

    def predict(self, inputs):
        return self.model(torch.from_numpy(inputs).float())

    def train(self, train_net):
        if len(self.replay_buffer['s']) < self.min_buffer:
            # Only start the training process when we have enough experiences in the buffer
            return 0

        # Randomly select n experience in the buffer, n is batch-size
        random_sample = np.random.randint(low=0, high=len(self.replay_buffer['s']), size=self.batch_size)
        states = np.asarray([self.preprocess(self.replay_buffer['s'][i]) for i in random_sample])
        actions = np.asarray([self.replay_buffer['a'][i] for i in random_sample])
        rewards = np.asarray([self.replay_buffer['r'][i] for i in random_sample])

        states_next = np.asarray([self.preprocess(self.replay_buffer['s_next'][i]) for i in random_sample])
        dones = np.asarray([self.replay_buffer['done'][i] for i in random_sample])
        value_next = np.max(train_net.predict(states_next).detach().numpy(), axis=1)
        actual_values = np.where(dones, rewards, rewards + self.gamma * value_next)

        actions = np.expand_dims(actions, axis=1)
        actions_one_hot = torch.FloatTensor(self.batch_size, self.action_n).zero_()
        actions_one_hot = actions_one_hot.scatter_(1, torch.LongTensor(actions), 1)
        selected_action_values = torch.sum(self.predict(states) * actions_one_hot, dim=1)
        actual_values = torch.FloatTensor(actual_values)

        self.optimizer.zero_grad()
        loss = self.criterion(selected_action_values, actual_values)
        loss.backward()
        self.optimizer.step()

    # Using Epsilon greedy to
    def get_action(self, state:int, epsilon_greedy:float):
        if np.random.random() < epsilon_greedy:
            return int(np.random.choice([c for c in range(self.action_n) if state["board"][c] == 0]))
        else:
            prediction = self.predict(np.atleast_2d(self.preprocess(state)))[0].detach().numpy()
            for i in range(self.action_n):
                if state["board"][i] != 0:
                    prediction[i] = -1e7
            return int(np.argmax(prediction))

    # Replay_Buffer Controller
    def add_buffer(self, buffer:dict):
        if len(self.replay_buffer['s']) >= self.max_buffer:
            for key in self.replay_buffer.keys():
                self.replay_buffer[key].pop(0)
        for key, value in buffer.items():
            self.replay_buffer[key].append(value)

    # Use these methods if you want to save/load weights
    def copy_weights(self, TNet):
        self.model.load_state_dict(TNet.state_dict())

    def save_weights(self, path):
        torch.save(self.model.state_dict(), path)

    def load_weights(self, path):
        self.model.load_state_dict(torch.load(path))

    # All of the states are recorded as board and those are also should be recorded in the mark
    def preprocess(self, state):
        result = state["board"][:]
        result.append(state.mark)
        return result