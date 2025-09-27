import numpy as np

class TicTacToe:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset the board to empty state"""
        self.board = np.zeros(9, dtype=int)  # 0=empty, 1=X, 2=O
        self.done = False
        self.winner = None
        return self.board.copy()

    def available_actions(self):
        available = []
        for i in range(9):
            if self.board[i] == 0:
                available.append(i)
        return available
    def step(self, action, player):
        """Make a move for player (1=X, 2=O)"""
        if self.done:
            raise ValueError("Game is already finished!")
        if self.board[action] != 0:
            raise ValueError("Invalid move,already taken!")

        self.board[action] = player

        self.check_winner()

        return self.board.copy(), self.done, self.winner

    def check_winner(self):
        
        b = self.board 
        lines = [
            [0,1,2], [3,4,5], [6,7,8],  
            [0,3,6], [1,4,7], [2,5,8],  
            [0,4,8], [2,4,6]          
        ]
        for line in lines:
            if b[line[0]] != 0 and b[line[0]] == b[line[1]] == b[line[2]]:
                self.done = True
                self.winner = b[line[0]]
                return

        if 0 not in b:
            self.done = True
            self.winner = 0  

