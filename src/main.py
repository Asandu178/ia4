# used for testing as of now
from board import *
from board.boardLogic import *
from pieces import *


b = Board(8, 8)


fenToBoard(b, "rnbqkbnr/pppppppp/8/8/8/1p6/PPPPPPPP/RNBQKBNR/")

b.printBoard()

for p in b.board[6]:
    print(p.moveList())
    

fen  = boardToFen(b)

print(fen)

