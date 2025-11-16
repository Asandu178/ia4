from .piece import Piece
from board.utils import *


class Knight(Piece):

    value = 3

    def __repr__(self):
        return f"{self.type}"
        
    def moveList(self) -> list[tuple[int, int]]:

        b = self.Board
        
        moves = []
        if self.colour == 'white':
            friendlies = b.white_pieces
            enemies = b.black_pieces
        else:
            friendlies = b.black_pieces
            enemies = b.white_pieces

        friendyPositions = {p.position for p in friendlies}

        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for dx, dy in directions:
            x, y = self.position
            x += dx
            y += dy

            if not validPos((x, y)):
                continue
            # ensure we dont try to move over an allied piece
            if (x, y) not in friendyPositions:
                moves.append((x, y))

        return moves