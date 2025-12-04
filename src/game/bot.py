from .player import Player
from board import Board
from pieces import Piece
from .engine import Engine
from board.boardLogic import fromUCI, startingFen

class Bot(Player):
    def __init__(self, colour, name, time, depth : int = 30):
        super().__init__(colour, name, time, None)
        self.depth = depth
        self.engine = Engine(self.depth)

    def decideMove(self, moves : list[str], fen : str=startingFen) -> tuple[tuple[int, int], tuple[int, int], str]:
        bestMoveUci = self.engine.evaluatePos(moves, fen)
        bestmove = fromUCI(bestMoveUci)
        return bestmove



                
        
        


