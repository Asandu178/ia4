from .board import Board
from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King, Empty
from .utils import validPos
from game.player import Player
from game.human import Human
#from game.bot import Bot
from enum import Enum
import copy

startingFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

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

def fenToBoard(b : Board, fenNotation : str):

    _clearBoard(b)
    table = b.board
    i = 0
    j = 0

    for letter in fenNotation:
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

    return isSquareAttacked(b, colour, kingPos)

def getLegalMoves(p: Piece) -> list[tuple[int, int]]:
    
    if not p.Board:
        return []
    
    moves = p.moveList()

    x, y = p.position
    
    legal_moves = []
    
    for move in moves:
            
        if not kingInCheckAfterMove(p, move):
            legal_moves.append(move)
    
    return legal_moves

def is_castling_safe(king: King, move: tuple[int, int]) -> bool:
    board = king.Board
    current_row, current_col = king.position
    target_row, target_col = move
    
    # King cannot castle if it's currently in check
    if isCheck(board, king.colour):
        return False
    
    # Figure out which squares the king passes through
    if target_col > current_col:  
        # Kingside castling - moving right
        squares_king_passes_through = [
            (current_row, current_col + 1),
            (current_row, current_col + 2)
        ]
    else:  
        # Queenside castling - moving left
        squares_king_passes_through = [
            (current_row, current_col - 1),
            (current_row, current_col - 2)
        ]
    
    # Check if any square along the path is under attack
    for square in squares_king_passes_through:
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
        return not is_castling_safe(piece, move)
    
    # Normal move check
    board_copy = copy.deepcopy(piece.Board)
    copy_piece = board_copy.getPiece(piece.position)
    board_copy.movePiece(copy_piece, move)
    return isCheck(board_copy, piece.colour)


def gameState(board : Board, player : Player) -> GameStatus:

    validMoves = []
    moves = []

    if player.timeout():
        return GameStatus.TIMEOUT

    pieces = board.white_pieces if player.colour == 'white' else board.black_pieces

    for piece in pieces:
        moves = getLegalMoves(piece)
        if moves != []:
            validMoves.append(moves)
    
    if isCheck(board, player.colour) and validMoves == []:
        return GameStatus.CHECKMATE
    
    if validMoves == []:
        return GameStatus.STALEMATE
    
    return GameStatus.ONGOING

def updateEval(board : Board) -> float:
    Eval : float = 0

    for piece in board.white_pieces:
        Eval += piece.value
    
    for piece in board.black_pieces:
        Eval -= piece.value

    return Eval


        

    




    


