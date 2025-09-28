# main.py
import tkinter as tk
from agent import QLearningAgent
import pickle
import numpy as np

# ---------------- TicTacToe class ----------------
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

agent = QLearningAgent()
with open("q_table.pkl", "rb") as f:
    agent.q_table = pickle.load(f)

def play_console():
    env = TicTacToe()
    side = ''
    while side not in ['X','O']:
        side = input("Do you want to play X (first) or O (second)? ").upper()
    human_player = 1 if side == 'X' else 2
    agent_player = 2 if human_player == 1 else 1

    def print_board(board):
        symbols = [' ', 'X', 'O']
        board_2d = board.reshape(3,3)
        print("\nBoard:")
        for row in board_2d:
            print("|".join(symbols[cell] for cell in row))
        print()

    state = env.reset()
    done = False
    print(f"You are {side}, Agent is {'O' if human_player==1 else 'X'}")
    print_board(state)

    while not done:
        if agent_player == 1:
            action = agent.choose_action(state, env.available_actions())
            state, done, winner = env.step(action, agent_player)
            print("Agent plays:")
            print_board(state)
            if done: break

        move = -1
        while move not in env.available_actions():
            try:
                move = int(input(f"Your move {env.available_actions()}: "))
            except ValueError:
                continue
        state, done, winner = env.step(move, human_player)
        print_board(state)
        if done: break

        if agent_player == 2:
            action = agent.choose_action(state, env.available_actions())
            state, done, winner = env.step(action, agent_player)
            print("Agent plays:")
            print_board(state)

    if winner == 0:
        print("Draw!")
    elif winner == human_player:
        print("You win!")
    else:
        print("Agent wins!")

# ---------------- GUI mode ----------------
def play_gui():
    global env, human_player, agent_player, buttons

    env = TicTacToe()
    human_player = None
    agent_player = None
    buttons = []

    root = tk.Tk()
    root.title("Tic-Tac-Toe")

    info_label = tk.Label(root, text="Choose your side", font=("Arial", 16))
    info_label.grid(row=0, column=0, columnspan=3, pady=5)

    def reset_game():
        global env
        env = TicTacToe()
        for b in buttons:
            b.config(text="", state="normal")
        info_label.config(text="Your turn!" if human_player == 1 else "Agent's turn!")
        if agent_player == 1:
            agent_move()

    def choose_side(side):
        global human_player, agent_player
        human_player = 1 if side == 'X' else 2
        agent_player = 2 if human_player == 1 else 1
        side_frame.destroy()
        info_label.config(text="Your turn!" if human_player == 1 else "Agent's turn!")
        if agent_player == 1:
            agent_move()


    def agent_move():
        if env.done:
            return
        action = agent.choose_action(env.board, env.available_actions())
        state, _, _ = env.step(action, agent_player)
        buttons[action].config(text='X' if agent_player == 1 else 'O', state='disabled')
        check_game_over()

    def human_move(i):
        if env.done or env.board[i] != 0:
            return
        state, _, _ = env.step(i, human_player)
        buttons[i].config(text='X' if human_player == 1 else 'O', state='disabled')
        check_game_over()
        if not env.done and agent_player != human_player:
            agent_move()

    def check_game_over():
        if env.done:
            if env.winner == 0:
                info_label.config(text="Draw!")
            elif env.winner == human_player:
                info_label.config(text="You win!")
            else:
                info_label.config(text="Agent wins!")
        else:
            info_label.config(text="Your turn!" if human_player == 1 else "Agent's turn!")

    # Create buttons
    for i in range(9):
        b = tk.Button(root, text="", width=6, height=3, font=("Arial", 24),
                      command=lambda i=i: human_move(i))
        b.grid(row=1 + i // 3, column=i % 3)
        buttons.append(b)

    # Side selection frame
    side_frame = tk.Frame(root)
    side_frame.grid(row=4, column=0, columnspan=3, pady=5)
    tk.Label(side_frame, text="Choose your side:").pack(side='left')
    tk.Button(side_frame, text="X", command=lambda: choose_side('X')).pack(side='left', padx=5)
    tk.Button(side_frame, text="O", command=lambda: choose_side('O')).pack(side='left', padx=5)

    # Reset button
    reset_button = tk.Button(root, text="Reset Game", font=("Arial", 14), command=reset_game)
    reset_button.grid(row=5, column=0, columnspan=3, pady=10)

    root.mainloop()


# ---------------- Choose mode ----------------
if __name__ == "__main__":
    mode = ''
    while mode not in ['1','2']:
        mode = input("Choose mode: 1=Console, 2=GUI: ")
    if mode == '1':
        play_console()
    else:
        play_gui()
