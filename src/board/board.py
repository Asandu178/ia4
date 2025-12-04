from pieces import *
from board.utils import *
import copy

class Board:
    board : list[list[Piece]] = []
    white_pieces : list[Piece] = []
    black_pieces : list[Piece] = []
    # last move holds the last piece moved & its original position as well as where it moved to
    last_move : list[tuple[Piece, tuple[int, int], tuple[int, int]]] = None
    PGNname : list[str] = None

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
    
    # def movePiece(self, p : Piece, newPos : tuple[int, int], promoted_piece_type=None):

    #     x, y = p.position
    #     newx, newy = newPos
    #     target = self.getPiece(newPos)

    #     if isinstance(p, Pawn):
    #         p.firstMove = False
    #         # enPassant
    #         if isinstance(target, Empty) and newy != y:
    #             direction = -1 if p.colour == 'white' else 1
    #             self.board[newx - direction][newy] = Empty()
    #         if p.canPromote(newPos):
    #             p = self.promote(p, promoted_piece_type)

    #     if isinstance(p, Rook) or isinstance(p, King):
    #         p.firstMove = False
    #         if isinstance(p, King) and abs(newy - y) == 2:
    #             self.last_move = (p, (x, y))
    #             self.castle(p, newPos)
    #             return


    #     self.board[newx][newy] = p
    #     self.board[x][y] = Empty()
    #     p.position = newPos

    #     self.last_move = (p, (x, y), newPos)

    def movePiece(self, piece : Piece, newPos : tuple[int, int], promoted_piece_type=None) -> dict:
        self.updateBoard()
        currentPiecePos = piece.position
        targetPiece = self.getPiece(newPos)

        originalStates = {
            'currentPiece' : piece,
            'currentPiecePos' : currentPiecePos,
            'targetPiece' : targetPiece,
            'targetPiecePos' : newPos,
            'enPassant' : newPos,
            'firstMove' : getattr(piece, 'firstMove', None),
            'lastMove' : self.last_move,
            'castlingRook' : None,
            'castlingRookInitPos' : None,
            'castlingRookFinalPos' : None,
        }

        if isinstance(piece, Pawn):
            piece.firstMove = False
            # enPassant
            if isinstance(targetPiece, Empty) and newPos[1] != currentPiecePos[1]:
                direction = -1 if piece.colour == 'white' else 1
                # save piece to be captured
                originalStates['targetPiece'] = self.getPiece((newPos[0] - direction, newPos[1]))
                originalStates['targetPiecePos'] = ((newPos[0] - direction), newPos[1])
                originalStates['enPassant'] = newPos
                # capture piece
                self.board[newPos[0] - direction][newPos[1]] = Empty()
            if piece.canPromote(newPos):
                piece = self.promote(piece, newPos, promoted_piece_type)

        if isinstance(piece, Rook) or isinstance(piece, King):
            piece.firstMove = False
            # castling logic
            if isinstance(piece, King) and abs(newPos[1] - currentPiecePos[1]) == 2:
                self.last_move = (piece, currentPiecePos, newPos)
                # determine which rook is involved
                # check left-side first
                rookRow = 0 if piece.colour == 'black' else 7
                if (newPos[1] < currentPiecePos[1]):
                    originalStates['castlingRook'] = self.getPiece((rookRow, 0))
                    originalStates['castlingRookInitPos'] = (rookRow, 0)
                    originalStates['castlingRookFinalPos'] = (rookRow, 3)
                else:
                    originalStates['castlingRook'] = self.getPiece((rookRow, 7))
                    originalStates['castlingRookInitPos'] = (rookRow, 7)
                    originalStates['castlingRookFinalPos'] = (rookRow, 5)                   

                self.castle(piece, newPos)
                return originalStates
            
        self.setPiece(piece, newPos)
        self.setPiece(Empty(), currentPiecePos)
        piece.position = newPos
        self.last_move = (piece, currentPiecePos, newPos)
        self.updateBoard()

        return originalStates
    
    def unMakeMove(self, originalStates : dict):
        piece : Piece = originalStates['currentPiece']
        piecePos : tuple[int, int] = originalStates['currentPiecePos']
        firstMove : bool = originalStates['firstMove']
        lastMove : list[tuple[Piece, tuple[int, int]]] = originalStates['lastMove']
        target : Piece = originalStates['targetPiece']
        targetPos : tuple[int, int] = originalStates['targetPiecePos']
        enPassant : tuple[int, int] = originalStates['enPassant']
        rook : Rook = originalStates['castlingRook']
        rookPos = originalStates['castlingRookInitPos']
        rookFinal = originalStates['castlingRookFinalPos']

        self.setPiece(piece, piecePos)

        if hasattr(piece, 'firstMove'):
            piece.firstMove = firstMove
        
        self.last_move = lastMove

        self.setPiece(Empty(), enPassant)
        self.setPiece(target, targetPos)

        if (rook != None):
            self.setPiece(Empty(), rookFinal)
            self.setPiece(rook, rookPos)

        

    def setPiece(self, piece : Piece, pos : tuple[int, int]):
        self.board[pos[0]][pos[1]] = piece
        piece.position = pos
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
    
    def promote(self, pawn : Pawn, newPos : tuple[int, int], piece_type='q') -> Piece:

        if piece_type is None:
            piece_type = 'q'

        img = f'{pawn.colour}-{piece_type.lower()}.png'
        
        if piece_type == 'q':
            new_piece = Queen(pawn.colour, img, newPos)
        elif piece_type == 'r':
            new_piece = Rook(pawn.colour, img, newPos)
        elif piece_type == 'b':
            new_piece = Bishop(pawn.colour, img, newPos)
        elif piece_type == 'n':
            new_piece = Knight(pawn.colour, img, newPos)
        else:
            new_piece = Queen(pawn.colour, img, newPos)

        new_piece.Board = self

        self.setPiece(new_piece, newPos)
        # print(f"promoted on {newPos} to {piece_type}")
        return new_piece
    
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


        


