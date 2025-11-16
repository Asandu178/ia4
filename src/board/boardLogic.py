from .board import Board
from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King, Empty
import random

startingFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

testFen = "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1"

# map symbol to corresponding class & image

fenMap = {
    'p' : (Pawn, 'black', 'blackPawn.png'),
    'n' : (Knight, 'black', 'blackKnight.png'),
    'b' : (Bishop, 'black', 'blackBishop.png'),
    'r' : (Rook, 'black', 'blackRook.png'),
    'q' : (Queen, 'black', 'blackQueen.png'),
    'k' : (King, 'black', 'blackKing.png'),

    'P' : (Pawn, 'white', 'whitePawn.png'),
    'N' : (Knight, 'white', 'whiteKnight.png'),
    'B' : (Bishop, 'white', 'whiteBishop.png'),
    'R' : (Rook, 'white', 'whiteRook.png'),
    'Q' : (Queen, 'white', 'whiteQueen.png'),
    'K' : (King, 'white', 'whiteKing.png'),
}


def _clearBoard(b : Board):
    table = b.board
    for i, line in enumerate(table):
        for j, piece in enumerate(line):
            table[i][j] = Empty()

def fenToBoard(b : Board, fenNotation : str):

    _clearBoard(b)
    table = b.board
    i = 0
    j = 0

    for letter in fenNotation:
        if letter.isalpha():
            cls, colour, img = fenMap[letter]
            table[i][j] = cls(letter, colour, img, (i, j))
            table[i][j].Board = b
            if colour == 'white':
                b.white_pieces.append(table[i][j])
            else:
                b.black_pieces.append(table[i][j])
            j += 1

        if letter.isnumeric():
            j += int(letter)

        if letter == '/':
            i += 1
            j = 0


def boardToFen(b : Board) -> str:

    table = b.board
    fen = ""
    i = 0
    offset = 0

    for line in table:
        offset = 0
        for piece in line:
            if piece.type != "0":
                if offset != 0:
                    fen += str(offset)
                fen += piece.type
                offset = 0
            else:
                offset += 1
        if offset:
            fen += str(offset)
        fen += "/"
    return fen


def updateBoard(b : Board):
    table = b.board
    b.white_pieces = []
    b.black_pieces = []
    
    for line in table:
        for piece in line:
            if piece.colour == 'white':
                b.white_pieces.append(piece)
            else:
                b.black_pieces.append(piece)
    return (b.white_pieces, b.black_pieces)


def isCheck(b : Board, colour : str) -> bool:

    kingPos = b.getKingPosition(colour)

    if colour == 'white':
            enemies = b.black_pieces
    else:
            enemies = b.white_pieces

    for enemy in enemies:
        if kingPos in enemy.moveList():
            return True
    
    return False

def getLegalMoves(p : Piece) -> list[tuple[int, int]]:

    b : Board = p.Board
    
    legalMoves = []

    oldPos = p.position

    moves = p.moveList()

    for move in moves:

        pieceAtDest = b.board[move[0]][move[1]]

        b.movePiece(p, move)

        if not isCheck(b, p.colour):
            legalMoves.append(move)

        b.movePiece(p, oldPos)
        b.board[move[0]][move[1]] = pieceAtDest

    return legalMoves


def randomMovePiece(p : Piece):
    b : Board = p.Board
    try:
        newPos = random.choice(getLegalMoves(p))
        b.movePiece(p, newPos)
    except IndexError:
        print("No valid movement")
    
        

    




    


