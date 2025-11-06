from pieces import *
from board.utils import *

class Board:
    board = []
    white_pieces = []
    black_pieces = []
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[Empty() for _ in range(cols)] for _ in range(rows)]
        print(self)
    
    def __repr__(self):
        return f"Hello from chess board"
    
    def printBoard(self):
        for i in range(self.rows):
            print(self.board[i])
        
    def getPiece(self, pos):
        if (validPos(pos)):
            (i, j) = pos
            return self.board[i][j]
        return 0