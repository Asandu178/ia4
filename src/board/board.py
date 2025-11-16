from pieces import *
from board.utils import *

class Board:
    board : list[list[Piece]] = []
    white_pieces : list[Piece] = []
    black_pieces : list[Piece] = []
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
        
    def getPiece(self, pos : tuple[int, int]) -> Piece:
        if (validPos(pos)):
            (i, j) = pos
            return self.board[i][j]
        return Empty()
    
    def movePiece(self, p : Piece, newPos : tuple[int, int]):

        x, y = p.position
        newx, newy = newPos

        if isinstance(p, Pawn):
            p.firstMove = False

        self.board[newx][newy] = p
        self.board[x][y] = Empty()
        p.position = newPos

        self.updateBoard()
    
    def getKingPosition(self, colour : str) -> tuple[int, int]:
        if (colour == 'white'):
            for piece in self.white_pieces:
                if (piece.type == 'K'):
                    return piece.position
        
        for piece in self.black_pieces:
            if (piece.type == 'k'):
                return piece.position
        
    def updateBoard(self):

        self.white_pieces = []
        self.black_pieces = []

        for line in self.board:
            for piece in line:
                if not piece.type == "0":
                    if piece.colour == 'white':
                        self.white_pieces.append(piece)
                    else:
                        self.black_pieces.append(piece)
