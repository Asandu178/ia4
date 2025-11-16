# used for testing as of now
from board import *
from board.boardLogic import *
from pieces import *
from board_gui import *


b = Board(8, 8)


fenToBoard(b, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/")

b.printBoard()    

fen  = boardToFen(b)

print(b.getKingPosition('white'))

# b.movePiece(pawn, pawn.moveList()[1])
# b.movePiece(pawn, pawn.moveList()[0])
# b.movePiece(pawn, pawn.moveList()[0])
# b.movePiece(pawn, pawn.moveList()[0])


for piece in b.white_pieces:
    print(f'Miscari valide pentru piesa {piece.type} aflata la {piece.position} : {getLegalMoves(piece)}')

r = b.getPiece((0, 0))
R = b.getPiece((7, 0))

b.movePiece(r, (1, 0))
b.movePiece(R, (2, 0))

b.printBoard()

print(fen)

