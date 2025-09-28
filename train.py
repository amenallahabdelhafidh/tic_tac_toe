# train.py
from agent import QLearningAgent
from main import  TicTacToe

import random
import pickle

def train(agent, episodes=5000):
    env = TicTacToe()

    for episode in range(episodes):
        state = env.reset()
        done = False

        while not done:
            available_actions = env.available_actions()
            action = agent.choose_action(state, available_actions)

            # Agent plays as X (1)
            next_state, done, winner = env.step(action, player=1)

            # Reward system
            if done:
                if winner == 1:      # Agent wins
                    reward = 1
                elif winner == 2:    # Agent loses
                    reward = -1
                else:                # Draw
                    reward = 0
            else:
                reward = 0

            # Random opponent (O=2)
            if not done:
                opp_actions = env.available_actions()
                if opp_actions:
                    opp_action = random.choice(opp_actions)
                    next_state, done, winner = env.step(opp_action, player=2)
                    if done:
                        if winner == 2:
                            reward = -1
                        elif winner == 0:
                            reward = 0

            # Update Q-table
            agent.update(state, action, reward, next_state, done)
            state = next_state

        # Print progress every 500 episodes
        if (episode + 1) % 500 == 0:
            print(f"Episode {episode+1} completed")

    print("Training finished!")

    # Save the trained Q-table
    with open("q_table.pkl", "wb") as f:
        pickle.dump(agent.q_table, f)
    print("Q-table saved as q_table.pkl")

if __name__ == "__main__":
    agent = QLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.2)
    train(agent, episodes=5000)
