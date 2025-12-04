from .board import Board
from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King, Empty
from .utils import validPos
from game.player import Player
from enum import Enum

startingFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

testFen = "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1"

# map symbol to corresponding class & image

fenMap = {
    'p' : (Pawn, 'black', 'black-pawn.png'),
    'n' : (Knight, 'black', 'black-knight.png'),
    'b' : (Bishop, 'black', 'black-bishop.png'),
    'r' : (Rook, 'black', 'black-rook.png'),
    'q' : (Queen, 'black', 'black-queen.png'),
    'k' : (King, 'black', 'black-king.png'),

    'P' : (Pawn, 'white', 'white-pawn.png'),
    'N' : (Knight, 'white', 'white-knight.png'),
    'B' : (Bishop, 'white', 'white-bishop.png'),
    'R' : (Rook, 'white', 'white-rook.png'),
    'Q' : (Queen, 'white', 'white-queen.png'),
    'K' : (King, 'white', 'white-king.png'),
}

class GameStatus(Enum):
    CHECKMATE = 1
    TIMEOUT = 2
    STALEMATE = 3
    RESIGN = 4
    ONGOING = 5


def _clearBoard(b : Board):
    table = b.board
    for i, line in enumerate(table):
        for j, piece in enumerate(line):
            table[i][j] = Empty()

def fenToBoard(b : Board, fenNotation : str=startingFen):

    _clearBoard(b)
    table = b.board
    i = 0
    j = 0
    
    board_part = fenNotation.split(' ')[0]

    for letter in board_part:
        if letter.isalpha():
            cls, colour, img = fenMap[letter]
            table[i][j] = cls(colour, img, (i, j))
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

def toUCI(board : Board, originalStates : dict) -> str:
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
    team = piece.colour

    notation = f"{CoordsToAlgebraic(piecePos)}{CoordsToAlgebraic(enPassant)}"
    if isinstance(piece, Pawn) and (targetPos[0] == 7 or targetPos[0] == 0):
        notation += (board.getPiece(targetPos)).type.lower()

    return notation

def fromUCI(uci : str) -> tuple[tuple[int, int], tuple[int, int], str]:
    initPos = uci[:2]
    newPos = uci[2:4]
    promotion = None
    if len(uci) > 4:
        promotion = uci[4]
    return (algebraicToCoords(initPos), algebraicToCoords(newPos), promotion)


def algebraicToCoords(square: str) -> tuple[int, int]:
    row = 8 - int(square[1])
    col = ord(square[0].lower()) - ord('a')
    return (row, col)

def CoordsToAlgebraic(coords: tuple[int, int]) -> str:
    (row, col) = coords
    algebraic: str = ""
    algebraic += chr(col + ord('a'))
    algebraic += str(8 - row)
    return algebraic


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

    return isSquareAttacked(b, colour, kingPos)

def isCheckmate(b : Board, colour : str) -> bool:

    if not isCheck(b, colour):
        return False
    
    pieces = b.white_pieces if colour == 'white' else b.black_pieces

    for piece in pieces:
        if getLegalMoves(piece) != []:
            return False
    return True

def isStalemate(b : Board, colour : str) -> bool:
    if isCheck(b, str) or isCheckmate(b, str):
        return False
    
    pieces = b.white_pieces if colour == 'white' else b.black_pieces

    for piece in pieces:
        if getLegalMoves(piece) != []:
            return False
    
    return True


def getLegalMoves(p: Piece) -> list[tuple[int, int]]:
    
    if not p.Board:
        return []
    
    moves = p.moveList()
    
    legalMoves = []
    
    for move in moves:
            
        if not kingInCheckAfterMove(p, move):
            legalMoves.append(move)
    
    return legalMoves

def isCastlingSafe(king: King, move: tuple[int, int]) -> bool:
    board = king.Board
    current_row, current_col = king.position
    target_row, target_col = move
    
    # King cannot castle if it's currently in check
    if isCheck(board, king.colour):
        return False
    
    # Figure out which squares the king passes through
    if target_col > current_col:  
        # Kingside castling - moving right
        squaresKingPassesThrough = [
            (current_row, current_col + 1),
            (current_row, current_col + 2)
        ]
    else:  
        # Queenside castling - moving left
        squaresKingPassesThrough = [
            (current_row, current_col - 1),
            (current_row, current_col - 2)
        ]
    
    # Check if any square along the path is under attack
    for square in squaresKingPassesThrough:
        if isSquareAttacked(board, king.colour, square):
            return False
    
    return True

def isSquareAttacked(board : Board, colour : str, pos : tuple[int, int]) -> bool:
    enemies = board.white_pieces if colour == 'black' else board.black_pieces
    for enemy in enemies:
        if pos in enemy.moveList():
            return True
    return False

def kingInCheckAfterMove(piece: Piece, move: tuple[int, int]) -> bool:
    # Special castling check
    if isinstance(piece, King) and abs(move[1] - piece.position[1]) == 2:
        return not isCastlingSafe(piece, move)
    
    # Normal move check
    board : Board = piece.Board
    originalStates = board.movePiece(piece, move)
    check = isCheck(board, piece.colour)
    board.unMakeMove(originalStates)
    return check



def gameState(board : Board, player : Player) -> GameStatus:

    if  player.timeout():
        return GameStatus.TIMEOUT
    
    if isCheckmate(board, player.colour):
        return GameStatus.CHECKMATE
    
    if isStalemate(board, player.colour):
        return GameStatus.STALEMATE
    
    return GameStatus.ONGOING


        

    




    


