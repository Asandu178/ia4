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

    def handleClick(self, pos : tuple[int, int]) -> bool:
        if self.gameOver or not validPos(pos):
            return False
        
        # handle bot movement
        if isinstance(self.currentPlayer, Bot):
            self.selectedPiece, pos = self.currentPlayer.randomMove()
            self.selectedPiecePos = self.selectedPiece.position
            self.possibleMoves = getLegalMoves(self.selectedPiece)

        if self.selectedPiece and pos in self.possibleMoves:
            self._handleMove(pos)
            return True
        
        else:
            self._handleSelect(pos)
            return False
        
    def _handleMove(self, pos : tuple[int, int]):
        # make move
        self.board.movePiece(self.selectedPiece, pos)

        self.moveCnt += 1
        # stop clock only if not first move (since for the first move clock doesnt start)
        if not self.firstMove:
            self.currentPlayer.stopClock()
            self.firstMove = False

        print(f'{self.currentPlayer.colour.capitalize()} time left:{self.currentPlayer.time}')
        print(f'{self.moveCnt}# {self.currentPlayer.colour.capitalize()} moved {self.selectedPiece}{self.selectedPiecePos} to {pos}')

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
        status = gameState(self.board, self.currentPlayer)

        if status == GameStatus.CHECKMATE:
            self.winner = self.winner = 'black' if self.currentPlayer == self.whitePlayer else 'white'
            self.gameOver = True
        elif status == GameStatus.STALEMATE:
            self.winner = None
            self.gameOver = True
        elif status == GameStatus.TIMEOUT:
            self.winner = self.winner = 'black' if self.currentPlayer == self.whitePlayer else 'white'
            self.gameOver = True
        elif status == GameStatus.RESIGN:
            self.winner = self.winner = 'black' if self.currentPlayer == self.whitePlayer else 'white'
            self.gameOver = True
