from .piece import Piece
class Empty(Piece):
    def __init__(self):
        self.type = "0"

    def __repr__(self):
        return "."