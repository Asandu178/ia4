from .player import Player
from board import Board
from pieces import Piece
from board.boardLogic import getLegalMoves
import random

class Bot(Player):
    def __init__(self, colour, name, time, board : Board = None):
        super().__init__(colour, name, time, board)

    def randomMove(self) -> tuple[Piece, tuple[int, int]]:
        pieces = self.board.white_pieces if self.colour == 'white' else self.board.black_pieces
        all_moves = []
    
        for piece in pieces:
            moves = getLegalMoves(piece)
            for move in moves:
                all_moves.append((piece, move))  # Add each move individually
    
        if all_moves:
            return random.choice(all_moves)
        else:
            return None  # No legal moves (checkmate/stalemate)
    
    def decideMove(self, board : Board, currentPlayer : str) -> tuple[Piece, tuple[int, int]]:

        pass
        
        


