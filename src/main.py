# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from route_optimization import OSRMRouteOptimizer  # Adjust import to the correct class name
from rl_algorithm import QLearningAgent
from data_preprocessing import preprocess_data
from visualization import plot_routes
from typing import Optional, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Step 1: Data Preprocessing
def load_and_preprocess_data(data_file: str) -> Optional[pd.DataFrame]:
    """
    Load and preprocess the data from a CSV file.

    Parameters:
        data_file (str): Path to the CSV file containing the data.

    Returns:
        Optional[DataFrame]: Cleaned and preprocessed data, or None if an error occurs.
    """
    try:
        logging.info("Loading data from %s", data_file)
        data = pd.read_csv(data_file)

        if data.empty:
            raise ValueError("The input data file is empty.")
        
        cleaned_data = preprocess_data(data)
        logging.info("Data successfully loaded and preprocessed.")
        return cleaned_data

    except FileNotFoundError:
        logging.error("File '%s' not found. Please provide a valid file path.", data_file)
    except ValueError as e:
        logging.error("Error: %s", e)
    except Exception as e:
        logging.error("An unexpected error occurred while loading data: %s", e)
    
    return None

# Step 2: Route Optimization
def get_optimized_route(delivery_data: pd.DataFrame) -> List[dict]:
    """
    Generate optimized routes from delivery data.

    Parameters:
        delivery_data (DataFrame): Preprocessed delivery data.

    Returns:
        List[dict]: Optimized routes as a list of coordinate dictionaries.
    """
    try:
        logging.info("Optimizing delivery routes...")
        optimized_routes = OSRMRouteOptimizer.optimize_route(delivery_data)
        
        if not optimized_routes:
            raise ValueError("Optimization failed. No routes generated.")
        
        logging.info("Optimized routes successfully generated.")
        return optimized_routes

    except ValueError as e:
        logging.error("Error: %s", e)
    except Exception as e:
        logging.error("An unexpected error occurred during route optimization: %s", e)
    
    return []

# Step 3: Reinforcement Learning
def run_reinforcement_learning(optimized_routes: List[dict], episodes: int = 1000, learning_rate: float = 0.1) -> Optional[QLearningAgent]:
    """
    Train a reinforcement learning agent using optimized routes.

    Parameters:
        optimized_routes (list): List of optimized routes.
        episodes (int): Number of training episodes.
        learning_rate (float): Learning rate for the RL agent.

    Returns:
        Optional[QLearningAgent]: Trained RL agent, or None if an error occurs.
    """
    if not optimized_routes:
        logging.error("Cannot run reinforcement learning with empty routes.")
        return None
    
    try:
        logging.info("Initializing RL agent...")
        agent = QLearningAgent(learning_rate=learning_rate)
        
        logging.info("Training RL agent for %d episodes...", episodes)
        agent.train(optimized_routes, episodes=episodes)
        logging.info("Reinforcement Learning training completed.")
        return agent

    except Exception as e:
        logging.error("An error occurred during RL training: %s", e)
        return None

# Step 4: Visualization
def visualize_results(agent: Optional[QLearningAgent], optimized_routes: List[dict], plot_q_values: bool = True):
    """
    Visualize the optimized routes and RL metrics.

    Parameters:
        agent (Optional[QLearningAgent]): Trained RL agent.
        optimized_routes (list): List of optimized routes.
        plot_q_values (bool): Whether to plot Q-values.
    """
    if not optimized_routes:
        logging.error("No routes to visualize.")
        return

    logging.info("Visualizing optimized routes...")
    plot_routes(optimized_routes)
    
    if plot_q_values and agent:
        try:
            q_values = agent.get_q_values()
            if q_values:
                plt.figure(figsize=(10, 6))
                plt.plot(q_values, label="Q-Values", linewidth=2)
                plt.title("Q-Values Over Training Episodes")
                plt.xlabel("Episodes")
                plt.ylabel("Q-Value")
                plt.grid(True)
                plt.legend()
                plt.show()
            else:
                logging.warning("No Q-values available to plot.")
        except AttributeError:
            logging.warning("The RL agent does not provide Q-values for visualization.")

# Main Execution
if __name__ == "__main__":
    # Configuration
    DATA_FILE = "data/synthetic_data.csv"  # Path to your data file
    EPISODES = 1000                       # Number of training episodes
    LEARNING_RATE = 0.1                   # Learning rate for RL agent

    # Step 1: Load and preprocess data
    delivery_data = load_and_preprocess_data(DATA_FILE)
    if delivery_data is None:
        exit("Terminating program due to data loading error.")
    
    # Step 2: Optimize delivery routes
    optimized_routes = get_optimized_route(delivery_data)
    if not optimized_routes:
        exit("Terminating program due to route optimization failure.")
    
    # Step 3: Run Reinforcement Learning
    agent = run_reinforcement_learning(optimized_routes, episodes=EPISODES, learning_rate=LEARNING_RATE)
    if agent is None:
        exit("Terminating program due to RL training error.")
    
    # Step 4: Visualize results
    visualize_results(agent, optimized_routes, plot_q_values=True)
