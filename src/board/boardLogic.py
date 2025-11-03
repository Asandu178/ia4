from .board import Board
from pieces import Pawn, Knight, Bishop, Rook, Queen, King, Empty

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
        if (letter.isalpha()):
            cls, colour, img = fenMap[letter]
            table[i][j] = cls(letter, colour, img, (i, j))
            table[i][j].Board = b
            if (colour == 'white'):
                b.white_pieces.append(table[i][j])
            else:
                b.black_pieces.append(table[i][j])
            j += 1

        if (letter.isnumeric()):
            j += int(letter)

        if (letter == '/'):
            i += 1
            j = 0


def boardToFen(b : Board):

    table = b.board
    fen = ""
    i = 0
    offset = 0

    for line in table:
        offset = 0
        for piece in line:
            if (piece.type != "0"):
                if (offset != 0):
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
    white = []
    black = []
    
    for line in table:
        for piece in line:
            if (piece.colour == 'white'):
                white.append(piece)
            else:
                black.append(piece)
    return (white, black)



