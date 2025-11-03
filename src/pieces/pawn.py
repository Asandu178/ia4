from .piece import Piece
from board.utils import validPos


class Pawn(Piece):

    def __init__(self, type, colour, image, position = None):
        super().__init__(type, colour, image, position)
        self.firstMove = True

    def __repr__(self):
        return f"{self.type}"
    
    def moveList(self):
        b = self.Board
        table = b.board
        moves = []
        if self.colour == 'white':
            friendly = b.white_pieces
            enemy = b.black_pieces
            direction = -1
        else:
            friendly = b.black_pieces
            enemy = b.white_pieces
            direction = 1
        
        (i, j) = self.position

        forward1 = (i + direction, j)
        forward2 = (i + 2 * direction, j)

        if (validPos(forward1)):
            moves.append(forward1)
            if (validPos(forward2) and self.firstMove):
                moves.append(forward2)


        # attack moves

        attack1 = (i + direction, j + 1)
        attack2 = (i + direction, j - 1)



        return moves
