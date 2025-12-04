from board.board import Board
from board.boardLogic import *
from board.utils import validPos
from pieces import *
from .player import Player
from .human import Human
from .bot import Bot

class ChessGame:
    def __init__(self, whitePlayer : Player, blackPlayer : Player, fen=startingFen, initialTurn='white'):
        self.board : Board = Board(8, 8)
        fenToBoard(self.board, fen)
        self.currentPlayer = whitePlayer if initialTurn == 'white' else blackPlayer
        self.selectedPiece = None
        self.selectedPiecePos = None
        self.possibleMoves = []
        self.whitePlayer = whitePlayer
        self.blackPlayer = blackPlayer
        self.moveCnt = 0
        self.winner = None
        self.gameOver = False
        self.firstMove = True
        self.score = 0
        self.status = GameStatus.ONGOING
        self.uciMoves : list[str]= []

    def handleClick(self, pos : tuple[int, int], promoted_piece_type=None) -> bool | str:

        if self.gameOver or not validPos(pos):
            return False
        
        # handle bot movement
        if isinstance(self.currentPlayer, Bot):
            self.selectedPiecePos, pos, promoted_piece_type = self.currentPlayer.decideMove([], self.boardToFen())
            self.selectedPiece = self.board.getPiece(self.selectedPiecePos)
            self.possibleMoves = getLegalMoves(self.selectedPiece)

        if self.selectedPiece and pos in self.possibleMoves:
            # Check for promotion
            if isinstance(self.selectedPiece, Pawn) and self.selectedPiece.canPromote(pos):
                if promoted_piece_type is None:
                    return 'PROMOTION_NEEDED'
            
            self._handleMove(pos, promoted_piece_type)
            return True
        
        else:
            self._handleSelect(pos)
            return False
        
    def _handleMove(self, pos : tuple[int, int], promoted_piece_type=None):
        # make move

        originalState = self.board.movePiece(self.selectedPiece, pos, promoted_piece_type)

        self.moveCnt += 1
        # stop clock only if not first move (since for the first move clock doesnt start)
        if not self.firstMove:
            self.currentPlayer.stopClock()
            self.firstMove = False
        
        moveUCI = toUCI(self.board, originalState)
        self.uciMoves.append(moveUCI)
        print(f'{self.currentPlayer.colour.capitalize()} time left:{self.currentPlayer.time}')
        print(f'{self.moveCnt}# {self.currentPlayer.colour.capitalize()} {moveUCI}')
        print(f'Current eval score {updateEval(self.board)}')

        # switch players
        self.currentPlayer = self.blackPlayer if self.currentPlayer == self.whitePlayer else self.whitePlayer
        # start opponent's clock
        self.currentPlayer.startClock()

        print(self.boardToFen())

        # no longer first move
        if self.firstMove:
            self.firstMove = False
        
        # update gameState
        self._updateGameState()

        # Reset selection
        self.selectedPiece = None
        self.selectedPiecePos = None
        self.possibleMoves = []

    def _handleSelect(self, pos : tuple[int, int]):
        piece = self.board.getPiece(pos)

        if not isinstance(piece, Empty) and piece.colour == self.currentPlayer.colour:
            self.selectedPiece = piece
            self.selectedPiecePos = pos
            self.possibleMoves = getLegalMoves(self.selectedPiece)
        else:
            self.selectedPiece = None
            self.selectedPiecePos = None
            self.possibleMoves = []

    def _updateGameState(self):
        self.status = gameState(self.board, self.currentPlayer)

        if self.status == GameStatus.CHECKMATE:
            self.winner = self.winner = 'black' if self.currentPlayer == self.whitePlayer else 'white'
            self.gameOver = True
        elif self.status == GameStatus.STALEMATE:
            self.winner = None
            self.gameOver = True
        elif self.status == GameStatus.TIMEOUT:
            self.winner = self.winner = 'black' if self.currentPlayer == self.whitePlayer else 'white'
            self.gameOver = True
        elif self.status == GameStatus.RESIGN:
            self.winner = self.winner = 'black' if self.currentPlayer == self.whitePlayer else 'white'
            self.gameOver = True

    def castleRight(self, colour : str) -> str:

        rights : str = ""
        kingPos = self.board.getKingPosition(colour)
        king : King = self.board.getPiece(kingPos)
        row = 0 if colour == 'black' else 7
        queenSide = 'q' if colour == 'black' else 'Q'
        if not king.firstMove:
            return rights
        
        rookQueenSide : Piece = self.board.getPiece((row, 0))
        rookKingSide : Piece = self.board.getPiece((row, 7))

        if isinstance(rookKingSide, Rook):
            if rookKingSide.firstMove:
                rights += f"{king.type}"
        if isinstance(rookQueenSide, Rook):
            if rookQueenSide.firstMove:
                rights += f"{queenSide}"       

        return rights
    
    def recordEnPassantTarget(self) -> str:
        # check if last move was a pawn move and if it was an EnPassant valid target
        if self.board.last_move == None:
            return "-"
        piece, initPos, newPos =  self.board.last_move
        x, y = newPos
        direction = -1 if piece.colour == 'white' else 1
        print(self.board.last_move)

        # if it wasnt a pawn or it didnt move 2 squares
        if not isinstance(piece, Pawn) or abs(initPos[0] - newPos[0]) != 2:
            return "-"
        
        return f"{CoordsToAlgebraic((x - direction, y))}"

    def boardToFen(self) -> str:

        # piece placement data
        table = self.board.board
        fen = ""
        i = 0
        offset = 0

        for line in table:
            i += 1
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
            if i != 8:
                fen += "/"
        fen += f" {self.currentPlayer.colour[0]} "
        rights = self.castleRight('white')
        rights += self.castleRight('black')
        if rights == "":
            rights = '-'
        fen += rights
        fen += " "
        fen += self.recordEnPassantTarget()
        fen += f" 0 {int(self.moveCnt / 2)}"

        print(self.uciMoves)
        return fen
