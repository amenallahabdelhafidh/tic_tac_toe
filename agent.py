import numpy as np
import random

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.q_table = {}  # dictionary: state -> action values
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # exploration probability

    def get_state_key(self, state):
        """Convert board numpy array into a string to use as dict key"""
        return tuple(state.tolist())

    def choose_action(self, state, available_actions):
        """Epsilon-greedy strategy to pick an action"""
        state_key = self.get_state_key(state)

        # Initialize if unseen
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(9)

        # Exploration vs Exploitation
        if random.random() < self.epsilon:
            return random.choice(available_actions)  # explore
        else:
            q_values = self.q_table[state_key]
            return max(available_actions, key=lambda a: q_values[a])  # exploit best

    def update(self, state, action, reward, next_state, done):
        """Update Q-values based on the reward received"""
        state_key = self.get_state_key(state)
        next_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(9)
        if next_key not in self.q_table:
            self.q_table[next_key] = np.zeros(9)

        q_values = self.q_table[state_key]

        if done:
            target = reward
        else:
            target = reward + self.gamma * np.max(self.q_table[next_key])

        q_values[action] += self.alpha * (target - q_values[action])
