from .player import Player
from board import Board
from pieces import Piece
from board.boardLogic import getLegalMoves, gameState, GameStatus, updateEval
import random
import copy
import math

class Bot(Player):
    def __init__(self, colour, name, time, depth : int = 3, board : Board = None):
        super().__init__(colour, name, time, board)
        self.depth = depth

    def randomMove(self) -> tuple[Piece, tuple[int, int]]:
        allMoves = self.getAllMoves(self.colour, self.board)
    
        if allMoves:
            return random.choice(allMoves)
        else:
            return None  # No legal moves (checkmate/stalemate)
    
    def decideMove(self, board : Board, currentPlayer : Player) -> tuple[Piece, tuple[int, int]]:
        bestMove = None
        alpha = -math.inf
        beta = math.inf
        allMoves = self.getAllMoves(currentPlayer.colour, board)

        if not allMoves:
            return None
        
        isMaximizing = (currentPlayer.colour == self.colour)

        # is bots turn to play ?
        if isMaximizing:
            bestValue = -math.inf
            # try all moves
            for piece, move in allMoves:
                # make move
                prevState = board.movePiece(piece, move)
                # evaluate score
                value = self.alphaBeta(board, self.depth - 1, False, alpha, beta)
                # unmake move
                board.unMakeMove(prevState)
                # store best response
                if value > bestValue:
                    bestValue = value
                    bestMove = (piece, move)
                
                alpha = max(alpha, bestValue)
                if beta <= alpha:
                    break
        
        else:
            bestValue = math.inf
            for piece, move in allMoves:
                prevState = board.movePiece(piece, move)
                value = self.alphaBeta(board, self.depth - 1, True, alpha, beta)
                board.unMakeMove(prevState)
                if value < bestValue:
                    bestValue = value
                    bestMove = (piece, move)

                beta = min(beta, bestValue)
                if beta <= alpha:
                    break

        return bestMove

    def alphaBeta(self, board: Board, depth: int, maximizingPlayer: bool, alpha: float, beta: float) -> float:
        # Check whose turn it is for gameState
        current_color = self.colour if maximizingPlayer else ('black' if self.colour == 'white' else 'white')
        current_player = Player(current_color, "temp", 60, board)
        
        # Get the game status
        status = gameState(board, current_player)
        
        if depth == 0 or status != GameStatus.ONGOING:
            eval_score = updateEval(board)
            
            # Adjust for perspective
            if self.colour == 'black':
                eval_score = -eval_score  # Flip evaluation for black
            
            return eval_score
        
        # Get moves for the current board state
        if maximizingPlayer:
            color = self.colour
        else:
            color = 'black' if self.colour == 'white' else 'white'
            
        allMoves = self.getAllMoves(color, board)
        
        if maximizingPlayer:
            value = -math.inf
            for piece, move in allMoves:
                # newBoard = copy.deepcopy(board)
                # copyPiece = newBoard.getPiece(piece.position)
                # newBoard.movePiece(copyPiece, move)
                prevState = board.movePiece(piece, move)
                
                value = max(value, self.alphaBeta(board, depth - 1, False, alpha, beta))
                alpha = max(alpha, value)
                board.unMakeMove(prevState)
                
                if beta <= alpha:
                    break  # Beta cutoff
            return value
        else:
            value = math.inf
            for piece, move in allMoves:
                # newBoard = copy.deepcopy(board)
                # copyPiece = newBoard.getPiece(piece.position)
                # newBoard.movePiece(copyPiece, move)
                prevState = board.movePiece(piece, move)
                
                value = min(value, self.alphaBeta(board, depth - 1, True, alpha, beta))
                beta = min(beta, value)
                board.unMakeMove(prevState)
                
                if beta <= alpha:
                    break  # Alpha cutoff
            return value
        

    def getAllMoves(self, colour, board : Board) -> tuple[(Piece, tuple[int, int])]:

        pieces = board.white_pieces if colour == 'white' else board.black_pieces
        allMoves = []
        for piece in pieces:
            moves = getLegalMoves(piece)
            for move in moves:
                allMoves.append((piece, move))
            
        return allMoves


                
        
        


