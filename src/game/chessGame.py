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

    def handleClick(self, pos : tuple[int, int], promoted_piece_type=None) -> bool | str:
        if self.gameOver or not validPos(pos):
            return False
        
        # handle bot movement
        if isinstance(self.currentPlayer, Bot):
            # self.selectedPiece, pos = self.currentPlayer.randomMove()
            if self.moveCnt <= 6:
                self.selectedPiece, pos = self.currentPlayer.randomMove()
            else:
                self.selectedPiece, pos = self.currentPlayer.decideMove(self.board, self.currentPlayer)
            self.selectedPiecePos = self.selectedPiece.position
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
        self.board.movePiece(self.selectedPiece, pos, promoted_piece_type)

        self.moveCnt += 1
        # stop clock only if not first move (since for the first move clock doesnt start)
        if not self.firstMove:
            self.currentPlayer.stopClock()
            self.firstMove = False

        print(f'{self.currentPlayer.colour.capitalize()} time left:{self.currentPlayer.time}')
        print(f'{self.moveCnt}# {self.currentPlayer.colour.capitalize()} moved {self.selectedPiece}{self.selectedPiecePos} to {pos}')
        print(f'{self.board.last_move}')
        print(f'Current eval score {updateEval(self.board)}')

        # switch players
        self.currentPlayer = self.blackPlayer if self.currentPlayer == self.whitePlayer else self.whitePlayer
        # start opponent's clock
        self.currentPlayer.startClock()

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
