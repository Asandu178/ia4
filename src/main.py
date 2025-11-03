# used for testing as of now
from board import *
from board.boardLogic import *
from pieces import *


b = Board(8, 8)


fenToBoard(b, startingFen)

par = Pawn('p', 'white', 'ce')

b.board[2][0] = par

b.printBoard()

fen  = boardToFen(b)

p = b.board[1][0]

print(p.moveList())

print(p)

print(fen)

