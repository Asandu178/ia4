from .piece import Piece
from board.utils import *


class Pawn(Piece):

    value = 1

    def __init__(self, type, colour, image, position = None):
        super().__init__(type, colour, image, position)
        self.firstMove = True
        self.enPassant = False

        

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

        friendlyPositions = {p.position for p in friendlies}

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

        # treat en passant case
        # release meeeeeee
        # TODO implement the logic ffs
        # maybe use a last move logic like if enemy last movement was a pawn check if he moved 2 tiles and if adjacent to this one -> can capture

        for attack in attacks:
            if validPos(attack) and attack not in friendlyPositions:
                left : Piece = b.getPiece((i, j - 1))
                right : Piece = b.getPiece((i, j + 1))

                if isinstance(left, Pawn):
                    if left.enPassant:
                        moves.append(attack)
                if isinstance(right, Pawn):
                    if right.enPassant:
                        moves.append(attack)



        return moves
