from .piece import Piece
from board.utils import *

class Bishop(Piece):

    value = 3

    def __init__(self, type, colour, image, position = None):
        super().__init__(type, colour, image, position)


    def __repr__(self):
        return f"{self.type}"
    

    def moveList(self):

        b = self.Board
        
        moves = []
        if self.colour == 'white':
            friendlies = b.white_pieces
            enemies = b.black_pieces
            direction = -1
        else:
            friendlies = b.black_pieces
            enemies = b.white_pieces
            direction = 1
        
        (i, j) = self.position

        allPiecePositions = {p.position for p in enemies + friendlies}
        # for x in range(8):
        #     for y in range(8):

        pass
