from .piece import Piece
from .rook import Rook
from board.utils import *

class King(Piece):

    def __repr__(self):
        return f"{self.type}"
    
    def __init__(self, colour, image, position = None):
        super().__init__(colour, image, position)
        self.firstMove = True
        self.type = 'K' if self.colour == 'white' else 'k'
    
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
        allPositions = friendlyPositions | enemyPositions

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

        if not self.firstMove:
            return moves
        
        # castling moves

        x, y = self.position

        kingside_rook = b.getPiece((x, 7))
        queenside_rook = b.getPiece((x, 0))

        # Kingside castling (O-O)
        if (isinstance(kingside_rook, Rook) and 
            kingside_rook.firstMove and
            (x, y + 1) not in allPositions and
            (x, y + 2) not in allPositions):
            moves.append((x, y + 2))

        # Queenside castling (O-O-O)
        if (isinstance(queenside_rook, Rook) and 
            queenside_rook.firstMove and
            (x, y - 1) not in allPositions and
            (x, y - 2) not in allPositions and
            (x, y - 3) not in allPositions):
            moves.append((x, y - 2))

        return moves