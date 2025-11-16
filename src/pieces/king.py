from .piece import Piece
from board.utils import *

class King(Piece):

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
        

        friendlyPositions = {p.position for p in friendlies}
        enemyPositions = {p.position for p in enemies}

        directions = [(-1, -1), (1, -1), (-1, 1), (1, 1), (1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:

            x, y = self.position
            x += dx
            y += dy

            if not validPos((x, y)):
                continue 

            if (x, y) in friendlyPositions:
                continue

            moves.append((x, y))

        return moves