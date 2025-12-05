from subprocess import Popen, PIPE, STDOUT
from board.boardLogic import startingFen
import os
import time
class Engine:
    def __init__(self, depth, pathToEngine="./game/stockfish/src/stockfish"):
        self.depth = depth
        self.pathToEngine = pathToEngine
        if not os.path.exists(pathToEngine):
            self.buildEngine()

    def buildEngine(self):
        p = Popen(["cd ./game/stockfish/src && make -j profile-build && sleep 60"], shell=True)
        time.sleep(30)
    
    def evaluatePos(self, moves: list[str]=[], fen: str=startingFen) -> str:
        p = Popen([self.pathToEngine], stdout=PIPE, stdin=PIPE, stderr=PIPE, text=True)

        # use stockfish with uci
        p.stdin.write("uci\n")
        p.stdin.flush()
        # await for stockfish to be ready to use uci
        while True:
            line = p.stdout.readline().strip()
            if line == "uciok":
                break

        # ask if it is ready to assert positions
        p.stdin.write("isready\n")
        p.stdin.flush()

        # wait until ready
        while True:
            line = p.stdout.readline().strip()
            if line == "readyok":
                break

        # introduce all moves made in uci format
        inputMoves = " ".join(moves)
        # send it over
        if moves == []:
            p.stdin.write(f"position fen {fen}\n")
            p.stdin.flush()
        else:
           p.stdin.write(f"position fen {fen} moves {inputMoves}\n")
           p.stdin.flush() 

        # evaluate at given depth
        p.stdin.write(f"go depth {self.depth}\n")
        p.stdin.flush()

        while True:
            line = p.stdout.readline().strip()
            if line.startswith("bestmove"):
                # stop engine
                p.terminate()
                return line.split()[1]


