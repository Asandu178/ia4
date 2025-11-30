from .player import Player
class Human(Player):
    def __init__(self, colour, name, time, board = None):
        super().__init__(colour, name, time, board)
