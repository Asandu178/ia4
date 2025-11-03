# used for testing as of now
from pieces import *
from board import *

ceva = Piece("p", "ceva.png", (3,5))
p = Pawn("p", "mar.png", (4,5))

b = Board(8, 8)

k = Knight("k", "wow.png", (3,5))

b.board[0][0] = ceva


funfen = "4k2r/6r1/8/8/8/8/3R4/R3K3"

fenToBoard(b, startingFen)

b.printBoard()

fen  = boardToFen(b)

print(fen)

