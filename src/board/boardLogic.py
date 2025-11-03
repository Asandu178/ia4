from .board import Board
from pieces import *

startingFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

testFen = "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1"

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
        if (i == 8 and j == 8):
            break
        if (letter.isalpha()):
            table[i][j] = Piece(letter, "ceva.png", (i,j))
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