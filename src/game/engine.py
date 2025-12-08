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

    @staticmethod
    def buildEngine(pathToEngine="./game/stockfish/src/stockfish"):
        if not os.path.exists(pathToEngine):
            p = Popen([f"wget -P ./game https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-ubuntu-x86-64-avx2.tar"], shell=True)
            time.sleep(5)
            p = Popen([f"cd ./game &&  tar -xvf stockfish-ubuntu-x86-64-avx2.tar && rm stockfish-ubuntu-x86-64-avx2.tar"], shell=True)
            time.sleep(5)
            p = Popen(["cd ./game/stockfish/src && make -j profile-build"], shell=True)
            time.sleep(60)
    
    def evaluatePos(self, moves: list[str]=[], fen: str=startingFen, threads=6) -> str:
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
        
        p.stdin.write(f"setoption name Threads value {threads}\n")
        p.stdin.flush()

        # wait until ready
        while True:
            line = p.stdout.readline().strip()
            if line == f"info string Using {threads} threads":
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


