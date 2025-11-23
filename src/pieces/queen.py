from .piece import Piece
from board.utils import *

class Queen(Piece):

    value = 9

    def __repr__(self):
        return f"{self.type}"
    
    def __init__(self, colour, image, position = None):
        super().__init__(colour, image, position)
        self.type = 'Q' if self.colour == 'white' else 'q'
    
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

            while validPos((x, y)):
                # ensure we dont try to move over an allied piece
                if (x, y) in friendlyPositions:
                    break
                moves.append((x, y))
                # when we hit the first enemy we stop looking in this direction, this being the last allowed move
                if (x, y) in enemyPositions:
                    break

                x += dx
                y += dy

        return moves