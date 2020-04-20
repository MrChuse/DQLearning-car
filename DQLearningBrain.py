import numpy as np


class Brain:

    def __init__(self, approximator, loss_f, num_actions, capacity=100000, discount_rate=0.99):
        self.net = approximator
        self.loss_f = loss_f
        self.num_actions = num_actions
        self.discount_rate = discount_rate
        self.capacity = capacity
        self.replay_memory = [(0,)] * capacity
        self.counter = 0
        self.eps_start = 1
        self.eps_end = 0.01
        self.eps_decay = 0.01
        self.eps = 1
        self.memory_usage = 0

    def add_replay_memory(self, current_state, taken_action, reward_for_that_action, following_state):
        self.replay_memory[self.counter] = (current_state, taken_action, reward_for_that_action, following_state)
        self.counter = (self.counter + 1) % self.capacity
        if self.memory_usage < self.capacity:
            self.memory_usage += 1

    def learn_from_replay_memory(self):
        random_number = np.random.randint(0, self.memory_usage)
        random_sample = self.replay_memory[random_number]
        #print(random_sample)
        q_values = self.net.forward(random_sample[0])
        q_values_next = self.net.forward(random_sample[3])
        max_q = np.max(q_values_next)
        target_q_value = max_q * self.discount_rate + random_sample[2]

        loss = self.loss_f.forward(q_values[0][random_sample[1]], target_q_value)
        dz = np.zeros(self.num_actions)
        dz[random_sample[1]] = self.loss_f.backward()
        self.net.backward(dz)
        return loss

    def get_action(self, state, greedy=False):
        if not greedy and np.random.random() < self.eps:
            return np.random.randint(0, self.num_actions)
        q_values = self.net.forward(state)
        best_action = np.argmax(q_values)
        return best_action

    def decrease_eps(self):
        if self.eps > self.eps_end:
            self.eps *= 1-self.eps_decay
