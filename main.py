from agent import QLearningAgent
import pickle
import numpy as np

# TicTacToe class (from your main.py)
class TicTacToe:
    def __init__(self):
        self.reset()
    def reset(self):
        self.board = np.zeros(9, dtype=int)
        self.done = False
        self.winner = None
        return self.board.copy()
    def available_actions(self):
        return [i for i in range(9) if self.board[i] == 0]
    def step(self, action, player):
        if self.done:
            raise ValueError("Game finished!")
        if self.board[action] != 0:
            raise ValueError("Invalid move!")
        self.board[action] = player
        self.check_winner()
        return self.board.copy(), self.done, self.winner
    def check_winner(self):
        b = self.board
        lines = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for line in lines:
            if b[line[0]] != 0 and b[line[0]] == b[line[1]] == b[line[2]]:
                self.done = True
                self.winner = b[line[0]]
                return
        if 0 not in b:
            self.done = True
            self.winner = 0

# Print the board
def print_board(board):
    symbols = [' ', 'X', 'O']
    board_2d = board.reshape(3,3)
    print("\nBoard:")
    for row in board_2d:
        print("|".join(symbols[cell] for cell in row))
    print()

# Play function
def play():
    # Load trained agent
    agent = QLearningAgent()
    with open("q_table.pkl", "rb") as f:
        agent.q_table = pickle.load(f)

    # Choose sides
    side = ''
    while side not in ['X','O']:
        side = input("Do you want to play X (first) or O (second)? ").upper()
    human_player = 1 if side == 'X' else 2
    agent_player = 2 if human_player == 1 else 1

    env = TicTacToe()
    state = env.reset()
    done = False
    print(f"You are {side}, Agent is {'O' if human_player==1 else 'X'}")
    print_board(state)

    while not done:
        # Agent move
        if agent_player == 1:
            available = env.available_actions()
            action = agent.choose_action(state, available)
            state, done, winner = env.step(action, agent_player)
            print("Agent plays:")
            print_board(state)
            if done: break

        # Human move
        available = env.available_actions()
        move = -1
        while move not in available:
            try:
                move = int(input(f"Your move {available}: "))
            except ValueError:
                continue
        state, done, winner = env.step(move, human_player)
        print_board(state)
        if done: break

        # Agent move
        if agent_player == 2:
            available = env.available_actions()
            action = agent.choose_action(state, available)
            state, done, winner = env.step(action, agent_player)
            print("Agent plays:")
            print_board(state)

    # Show result
    if winner == 0:
        print("Draw!")
    elif winner == human_player:
        print("You win!")
    else:
        print("Agent wins!")

if __name__ == "__main__":
    play()

