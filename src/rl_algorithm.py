import numpy as np

class QLearningAgent:
    def __init__(self, learning_rate=0.1, gamma=0.9, epsilon=0.1):
        self.learning_rate = learning_rate  # Alpha: Learning rate
        self.gamma = gamma                  # Gamma: Discount factor
        self.epsilon = epsilon              # Epsilon: Exploration rate
        self.q_values = {}                  # Q-values table

    def train(self, routes, episodes=1000):
        # Example of training logic
        for episode in range(episodes):
            route = routes[np.random.choice(len(routes))]
            # Update Q-values based on route (simplified)
            state, action, reward = route  # This is just an example
            self.update_q_values(state, action, reward)

    def update_q_values(self, state, action, reward):
        if (state, action) not in self.q_values:
            self.q_values[(state, action)] = 0
        old_q_value = self.q_values[(state, action)]
        self.q_values[(state, action)] = old_q_value + self.learning_rate * (reward + self.gamma * max(self.q_values.get((state, a), 0) for a in range(4)) - old_q_value)

    def get_q_values(self):
        return self.q_values
