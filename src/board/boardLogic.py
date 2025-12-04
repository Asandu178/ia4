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

def updateEval(board: Board, perspective='white') -> float:
    Eval: float = 0

    if isCheckmate(board, 'white'):
        return -100000 if perspective == 'white' else 100000
    
    if isCheckmate(board, 'black'):
        return 100000 if perspective == 'white' else -100000
    
    # Material count
    for piece in board.white_pieces:
        Eval += piece.value
        # Add positional value
        Eval += getPieceSquareValue(piece, 'white')
    
    for piece in board.black_pieces:
        Eval -= piece.value
        # Subtract positional value (good for black is bad for white)
        Eval -= getPieceSquareValue(piece, 'black')
    
    # Center control bonus
    Eval += evaluateCenterControl(board)
    
    # Development bonus (encourage moving pieces off back rank)
    Eval += evaluateDevelopment(board)
    
    # Flip sign if perspective is black
    if perspective == 'black':
        Eval = -Eval
    
    return Eval

def getPieceSquareValue(piece: Piece, color: str) -> float:
    """Return positional bonus based on piece type and position"""
    if not hasattr(piece, 'position'):
        return 0
    
    row, col = piece.position
    
    # Piece-square tables (simplified)
    if isinstance(piece, Pawn):
        # Pawns better in center and advanced
        if color == 'white':
            return (7 - row) * 0.2  # White moves down (0-7)
        else:
            return row * 0.2  # Black moves up (7-0)
    
    elif isinstance(piece, Knight):
        # Knights better in center
        center_distance = abs(3.5 - row) + abs(3.5 - col)
        return (8 - center_distance) * 0.3  # Closer to center = higher bonus
    
    elif isinstance(piece, Bishop):
        # Bishops like diagonals
        # gets a bonus for how many tiles it can occupy
        return len(getLegalMoves(piece)) * 0.2
    
    elif isinstance(piece, Rook):
        # Rooks like open files and 7th rank
        if row == 6:  # 7th rank for white, 2nd for black
            return 0.3
        return 0
    
    elif isinstance(piece, Queen):
        # Queen is flexible
        return 0
    
    elif isinstance(piece, King):
        # King safety - middle game: prefer castled position
        if col in [2, 3, 4, 5]:  # Near center (not castled)
            return -0.3  # Slightly negative
        elif col in [0, 7]:  # Original position
            return -0.5  # More negative
        else:  # Castled (g or b file)
            return 0.5
    
    return 0

def evaluateCenterControl(board: Board) -> float:
    """Bonus for controlling center squares"""
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    center_score = 0
    
    for row, col in center_squares:
        piece = board.getPiece((row, col))
        if piece and not isinstance(piece, Empty):
            if piece.colour == 'white':
                center_score += 0.8
            else:
                center_score -= 1
    
    return center_score

def evaluateDevelopment(board: Board) -> float:
    """Bonus for developing pieces (not on starting squares)"""
    development_score = 0
    
    # Check knights and bishops on starting squares
    for piece in board.white_pieces:
        if isinstance(piece, (Knight, Bishop)):
            row, col = piece.position
            # Starting positions for white: knights at (7,1),(7,6), bishops at (7,2),(7,5)
            if row == 7 and col in [1, 2, 5, 6]:
                development_score -= 0.4  # Penalty for not developing
    
    for piece in board.black_pieces:
        if isinstance(piece, (Knight, Bishop)):
            row, col = piece.position
            # Starting positions for black: knights at (0,1),(0,6), bishops at (0,2),(0,5)
            if row == 0 and col in [1, 2, 5, 6]:
                development_score += 0.4  # Bonus for white if black hasn't developed
    
    return development_score


        

    




    


