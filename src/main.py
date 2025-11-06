# used for testing as of now
from board import *
from board.boardLogic import *
from pieces import *


b = Board(8, 8)


fenToBoard(b, "rnbqkbnr/pppppppp/8/8/8/2Q6/PPPPPPPP/RNBQKBNR/")

b.printBoard()

# for p in b.board[6]:
#     print(p.moveList())
    

fen  = boardToFen(b)

print(b.getKingPosition('white'))

print(b.board[5][2].moveList())

print(fen)

