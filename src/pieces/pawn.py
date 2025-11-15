from .piece import Piece
from board.utils import *


class Pawn(Piece):

    value = 1

    def __init__(self, type, colour, image, position = None):
        super().__init__(type, colour, image, position)
        self.firstMove = True

        

    def __repr__(self):
        return f"{self.type}"
    
    def moveList(self) -> list[tuple[int, int]]:

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

        # normal moves

        forward1 = (i + direction, j)
        forward2 = (i + 2 * direction, j)

        # make a set of all piece positions

        allPiecePositions = {p.position for p in enemies + friendlies}

        if validPos(forward1) and forward1 not in allPiecePositions:
                moves.append(forward1)
                if validPos(forward2) and self.firstMove and forward2 not in allPiecePositions:
                    moves.append(forward2)


        # attack moves

        attacks = [(i + direction, j + 1), (i + direction, j - 1)]

        for attack in attacks:
            if validPos(attack):
                for enemy in enemies:
                    if enemy.position == attack:
                        moves.append(attack)
            else:
                continue

        return moves
