import numpy as np
import random

class QLearningAgent:
    def __init__(self, num_states, num_actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        """
        Initialize the Q-Learning Agent.
        
        Parameters:
        - num_states (int): Total number of states in the environment.
        - num_actions (int): Total number of possible actions.
        - alpha (float): Learning rate.
        - gamma (float): Discount factor for future rewards.
        - epsilon (float): Exploration-exploitation trade-off parameter.
        """
        self.num_states = num_states
        self.num_actions = num_actions
        self.q_table = np.zeros((num_states, num_actions))  # Initialize Q-table
        
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def choose_action(self, state):
        """
        Choose an action based on the epsilon-greedy policy.
        
        Parameters:
        - state (int): Current state.
        
        Returns:
        - action (int): Selected action.
        """
        if random.uniform(0, 1) < self.epsilon:  # Explore
            return random.choice(range(self.num_actions))
        else:  # Exploit
            return np.argmax(self.q_table[state])

    def learn(self, state, action, reward, next_state):
        """
        Update the Q-value using the Q-learning formula.
        
        Parameters:
        - state (int): Current state.
        - action (int): Action taken.
        - reward (float): Immediate reward received.
        - next_state (int): Resulting state after taking the action.
        """
        best_next_action = np.argmax(self.q_table[next_state])
        q_update = reward + self.gamma * self.q_table[next_state, best_next_action]
        self.q_table[state, action] += self.alpha * (q_update - self.q_table[state, action])

    def step(self, state, action, delivery_data):
        """
        Simulate the environment's response to the agent's action.
        
        Parameters:
        - state (int): Current state.
        - action (int): Action taken by the agent.
        - delivery_data: Placeholder for external environment data.
        
        Returns:
        - next_state (int): Resulting state after the action.
        - reward (float): Reward received.
        - done (bool): Whether the episode ends.
        """
        # Example: Simple simulation for demo purposes
        next_state = (state + action) % self.num_states
        reward = -abs(delivery_data.get("state_costs", {}).get(state, 0) - action)  # Customizable reward
        done = random.random() < 0.05  # End with small probability
        return next_state, reward, done

    def train(self, delivery_data, num_episodes=1000, max_steps=100):
        """
        Train the agent using Q-learning over a set number of episodes.
        
        Parameters:
        - delivery_data: Environment data for route simulation.
        - num_episodes (int): Total number of episodes to train.
        - max_steps (int): Maximum steps per episode.
        """
        for episode in range(1, num_episodes + 1):
            state = random.randint(0, self.num_states - 1)
            steps = 0
            done = False

            while not done and steps < max_steps:
                action = self.choose_action(state)
                next_state, reward, done = self.step(state, action, delivery_data)
                self.learn(state, action, reward, next_state)
                state = next_state
                steps += 1

            if episode % 100 == 0:
                print(f"Episode {episode}/{num_episodes} completed.")

    def get_q_values(self):
        """
        Retrieve the learned Q-table.
        
        Returns:
        - q_table (np.ndarray): Learned Q-values for each state-action pair.
        """
        return self.q_table


if __name__ == "__main__":
    # Example usage
    num_states = 10  # Placeholder for the number of delivery states
    num_actions = 5  # Placeholder for delivery routes (actions)

    # Create an agent
    agent = QLearningAgent(num_states=num_states, num_actions=num_actions)

    # Simulated delivery data (replace with a real environment)
    delivery_data = {
        "state_costs": {state: random.randint(1, 10) for state in range(num_states)}
    }

    # Train the agent
    agent.train(delivery_data, num_episodes=500, max_steps=50)

    # Print learned Q-values
    print("Learned Q-table:")
    print(agent.get_q_values())
