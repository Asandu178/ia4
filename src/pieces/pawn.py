from .piece import Piece
from board.utils import *


class Pawn(Piece):

    value = 1

    def __init__(self, colour, image, position = None):
        super().__init__(colour, image, position)
        self.firstMove = True
        self.type = 'P' if self.colour == 'white' else 'p'

        

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

        # treat enPassant case

        # retrieve last piece moved and its old position

        if b.last_move is None:
            return moves
        
        lastPieceMoved : Piece
        lastPieceMoved, (oldi, oldj) = b.last_move

        # if it isnt a pawn there is no need to check for enPassant

        if not isinstance(lastPieceMoved, Pawn):
            return moves

        # determine if this pawn's last move was its first by seeing if it moved two squares
        i, j = lastPieceMoved.position

        dif = abs(i - oldi)
        # as such it is valid for enPassant attacks
        attack = (oldi - direction, oldj)

        if attack in attacks and dif == 2:
            moves.append(attack)

        return moves
    
    def canPromote(self, move : tuple[int, int]) -> bool:
        
        backline = 0 if self.colour == 'white' else 7

        x, _ = move

        if x == backline:
            return True

        return False
