# used for testing as of now
from board import *
from board.boardLogic import *
from pieces import *
from board_gui import *


b = Board(8, 8)


fenToBoard(b, "rnbqkbnr/pppprppp/Q7/8/8/8/PPPP1PPP/RNBQKBNR/")

b.printBoard()    

fen  = boardToFen(b)

print(b.getKingPosition('white'))

# b.movePiece(pawn, pawn.moveList()[1])
# b.movePiece(pawn, pawn.moveList()[0])
# b.movePiece(pawn, pawn.moveList()[0])
# b.movePiece(pawn, pawn.moveList()[0])


for piece in b.white_pieces:
    print(f'Miscari valide pentru piesa {piece.type} aflata la {piece.position} : {getLegalMoves(piece)}')

piesa = b.getPiece((2, 0))

print(getLegalMoves(piesa))

b.printBoard()

print(fen)

