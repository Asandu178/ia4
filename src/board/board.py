from pieces import *
from board.utils import *

class Board:
    board : list[list[Piece]] = []
    white_pieces : list[Piece] = []
    black_pieces : list[Piece] = []
    # last move holds the last piece moved & its original position
    last_move : list[tuple[Piece, tuple[int, int]]] = None

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[Empty() for _ in range(cols)] for _ in range(rows)]
        # 0 for white, 1 for black
        self.turn = 0
        print(self)
    
    def __repr__(self):
        return f"Hello from chess board"
    
    def printBoard(self):
        for i in range(self.rows):
            print(self.board[i])
        
    def getPiece(self, pos : tuple[int, int]) -> Piece:
        if (validPos(pos)):
            (i, j) = pos
            return self.board[i][j]
        return Empty()
    
    def movePiece(self, p : Piece, newPos : tuple[int, int]):

        x, y = p.position
        newx, newy = newPos
        target = self.getPiece(newPos)

        if isinstance(p, Pawn):
            p.firstMove = False
            # enPassant
            if isinstance(target, Empty) and newy != y:
                direction = -1 if p.colour == 'white' else 1
                self.board[newx - direction][newy] = Empty()
            if p.canPromote(newPos):
                p = self.promote(p)

        if isinstance(p, Rook) or isinstance(p, King):
            p.firstMove = False
            if isinstance(p, King) and abs(newy - y) == 2:
                self.last_move = (p, (x, y))
                self.castle(p, newPos)
                return


        self.board[newx][newy] = p
        self.board[x][y] = Empty()
        p.position = newPos

        self.last_move = (p, (x, y))

        self.updateBoard()

    def setPiece(self, piece : Piece, pos : tuple[int, int]):
        self.board[pos[0]][pos[1]] = piece
        self.updateBoard()
    
    def getKingPosition(self, colour : str) -> tuple[int, int]:
        if (colour == 'white'):
            for piece in self.white_pieces:
                if (piece.type == 'K'):
                    return piece.position
        
        for piece in self.black_pieces:
            if (piece.type == 'k'):
                return piece.position
        
    def updateBoard(self):

        self.white_pieces = []
        self.black_pieces = []

        for line in self.board:
            for piece in line:
                if not piece.type == "0":
                    if piece.colour == 'white':
                        self.white_pieces.append(piece)
                    else:
                        self.black_pieces.append(piece)
    
    def promote(self, pawn : Pawn) -> Piece:

        # TODO : make the interface for promotion
        # currently just make a queen
        img = "placeholder"
        queen = Queen(pawn.colour, img, pawn.position)
        queen.Board = self

        self.setPiece(queen, pawn.position)
        print(f"promoted on {pawn.position}")
        return queen
    
    def castle(self, king : King, newPos : tuple[int, int]):
        newx , newy = newPos
        x , y = king.position

        # kingside castling
        if newy > y:
            rook : Rook = self.getPiece((x, 7))
            newRookPos = (x, y + 1)
        # queenside castling
        else:
            rook : Rook = self.getPiece((x, 0))
            newRookPos = (x, y - 1)

        # move king
        self.board[newx][newy] = king
        self.board[x][y] = Empty()
        king.position = newPos

        # move rook
        self.board[newRookPos[0]][newRookPos[1]] = rook
        self.board[rook.position[0]][rook.position[1]] = Empty()
        rook.position = newRookPos

        self.updateBoard()


        


