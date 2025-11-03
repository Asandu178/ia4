from .piece import Piece

class Rook(Piece):
    def __repr__(self):
        return f"{self.type}"