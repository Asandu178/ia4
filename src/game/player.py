from board import Board
import time
class Player:
    def __init__(self, colour : str, name : str, time : int, board : Board = None):
        self.colour = colour
        self.name = name
        self.time = time
        self.start = 0
        self.end = 0
        self.board = None

    def timeout(self) -> bool:
        return self.time <= 0

    def startClock(self):
        # if current player has no time left, he lost by timeout
        if not self.timeout():
            self.start = time.time()

    def stopClock(self):
        # stop counting
        self.end = time.time()
        # subtract the difference
        self.time -= (self.end - self.start)
        


