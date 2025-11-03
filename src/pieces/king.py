from .piece import Piece

class King(Piece):
    def __repr__(self):
        return f"{self.type}"