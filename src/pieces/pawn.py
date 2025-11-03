from .piece import Piece


class Pawn(Piece):
    def __repr__(self):
        return f"Hello from pawn {self.type}"
