from .piece import Piece

class Bishop(Piece):
    def __repr__(self):
        return f"{self.type}"