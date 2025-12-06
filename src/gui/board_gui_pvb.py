import pygame
import threading
import queue
from themes import get_theme
from board.board import Board
from board.boardLogic import *
from board import utils
from pieces.empty import Empty
from game.chessGame import ChessGame
from game.player import Player
from game.human import Human
from game.bot import Bot
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from .dialogs import show_promotion_dialog
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')   

# Helper function for threaded bot move calculation
def get_bot_move(game, move_queue):
    # This runs in a separate thread
    try:
        move = game.currentPlayer.decideMove([], game.boardToFen())
        move_queue.put(move)
    except Exception as e:
        print(f"Error in bot thread: {e}")

# pygame setup
def boardDisplayPvB(player1=None, player2=None, theme_name="gold", fen=startingFen, turn='white'):
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    running = True
    dt = 0
    
    # Parametri tabla
    Board_side = 8
    square_size = 120
    board_width = Board_side * square_size
    board_height = Board_side * square_size

    # Pozitia tablei pe ecran (centrata)
    board_x = (1920 - board_width) // 2
    board_y = (1080 - board_height) // 2
    
    # Importez tema aleasa
    theme = get_theme(theme_name)
    white = theme["light_square"]
    black = theme["dark_square"]
    background = theme["background"]
    border_color = theme["border"]
    
    # Variabile pentru ture
    # current_turn is now dynamic based on Game.currentPlayer
    font_small = pygame.font.Font(None, 60)  # Font mai mic pentru litere în cercuri

    if not player1:
        player1 = Human('white', 'Marius', 600)
    if not player2:
        player2 = Bot('black', 'Andrei', 600)
        
    Player1 = player1
    Player2 = player2
    Game = ChessGame(Player1, Player2, fen, turn)
    Player1.board = Game.board
    Player2.board = Game.board

    # Threading setup
    move_queue = queue.Queue()
    is_thinking = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if Game.winner != None or Game.gameOver:
                # TODO : handle gameover screen using
                print(f'{(f'Winner is {Game.winner.upper()}' if GameStatus.STALEMATE != Game.status else 'Stalemate')} after {Game.moveCnt} moves by {Game.status.name}')
                
            if not Game.gameOver:
                # Handle Human Input
                if not isinstance(Game.currentPlayer, Bot) and event.type == pygame.MOUSEBUTTONDOWN and not is_thinking:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    col = (mouse_x - board_x) // square_size
                    row = (mouse_y - board_y) // square_size
            
                
                    pos = (row, col)

                    result = Game.handleClick(pos)

                    if result == 'PROMOTION_NEEDED':
                        # Determine color of the current player
                        color = Game.currentPlayer.colour
                        promoted_piece_name = show_promotion_dialog(screen, color)
                        Game.handleClick(pos, promoted_piece_name)

                    # maybe use this ?
                    gameState(Game.board, Game.currentPlayer)

                    # TODO : handle states using _updateGameState perhaps

        # Bot Move Logic (Threaded)
        if not Game.gameOver and isinstance(Game.currentPlayer, Bot):
            if not is_thinking:
                is_thinking = True
                bot_thread = threading.Thread(target=get_bot_move, args=(Game, move_queue))
                bot_thread.daemon = True # Daemon thread dies if main program exits
                bot_thread.start()
            
            # Check if bot has found a move
            try:
                # Non-blocking get
                move = move_queue.get_nowait()
                start_pos, end_pos, promotion_type = move
                
                # Apply the move
                # We use applyExternalMove because it handles selection and move logic cleanly
                # even though it's technically "internal" to the bot logic here
                Game.applyExternalMove(start_pos, end_pos, promotion_type)
                
                gameState(Game.board, Game.currentPlayer)
                is_thinking = False
                
            except queue.Empty:
                pass # Still thinking

        # Umplu ecranul cu culoarea din temă
        screen.fill(background)
        
        # Desenez tabla de șah
        for row in range(Board_side):
            for col in range(Board_side):
                # Calcul pozitie
                x = board_x + col * square_size
                y = board_y + row * square_size
                
                # Aleg culoare (alb daca suma e para, negru daca e impara)
                if (row + col) % 2 == 0:
                    color = white
                else:
                    color = black
                
                # Desenez patratul
                pygame.draw.rect(screen, color, (x, y, square_size, square_size))
        
   

        for row in range(Board_side):
            for col in range(Board_side):
                piece = Game.board.getPiece((row, col))
                if not isinstance(piece, Empty):
                    # Calculate top-left corner of square
                    x = board_x + col * square_size
                    y = board_y + row * square_size
                    
                    # Get the PNG image for this piece
                    image_path = os.path.join(ASSETS_DIR, piece.image)
                    try:
                        image = pygame.image.load(image_path)
                    except FileNotFoundError:
                        image = None
                    
                    if image:
                        # Center the image in the square
                        img_x = x + (square_size - image.get_width()) // 2
                        img_y = y + (square_size - image.get_height()) // 2
                        screen.blit(image, (img_x, img_y))
                    else:
                        # Fallback: draw circle if image not found
                        center_x = x + square_size // 2
                        center_y = y + square_size // 2
                        if piece.colour == 'white':
                            piece_color = (255, 255, 255)
                        else:
                            piece_color = (50, 50, 50)
                        pygame.draw.circle(screen, piece_color, (center_x, center_y), 35)
                   
        
        # Desenez highlight pe piesa selectata
        if Game.selectedPiecePos:
            row, col = Game.selectedPiecePos
            x = board_x + col * square_size
            y = board_y + row * square_size
            pygame.draw.rect(screen, (255, 155, 115), (x, y, square_size, square_size), 5)
        
        # Desenez mutarile posibile
        for move in Game.possibleMoves:
            row, col = move
            x = board_x + col * square_size + square_size // 2
            y = board_y + row * square_size + square_size // 2
            # Cercul verde pentru mutare
            pygame.draw.circle(screen, (0, 255, 0), (x, y), 15)
        
        # Highlight last move
        if Game.moveCnt > 0 and Game.board.last_move:
            # Assuming Game.last_move is (piece, original_position)
            moved_piece, from_pos, _ = Game.board.last_move
            
            # Highlight FROM square (where piece came from)
            if from_pos:
                row, col = from_pos
                x = board_x + col * square_size
                y = board_y + row * square_size
                # Draw semi-transparent overlay
                highlight_surf = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                highlight_surf.fill((50, 255, 50, 64))
                screen.blit(highlight_surf, (x, y))
                # Optional: Add border
                pygame.draw.rect(screen, ((50, 255, 50, 64)), (x, y, square_size, square_size), 3)
            
            # Highlight TO square (where piece is now)
            if moved_piece and hasattr(moved_piece, 'position'):
                to_pos = moved_piece.position
                row, col = to_pos
                x = board_x + col * square_size
                y = board_y + row * square_size
                # Draw semi-transparent overlay
                highlight_surf = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                highlight_surf.fill((50, 255, 50, 64))
                screen.blit(highlight_surf, (x, y))
                # Optional: Add border
                pygame.draw.rect(screen, ((50, 255, 50, 64)), (x, y, square_size, square_size), 3)
                
        # Afiseaza tura curenta
        turn_text = f"Turn: {Game.currentPlayer.colour.capitalize()}"
        turn_surface = font_small.render(turn_text, True, (255, 255, 255))
        screen.blit(turn_surface, (50, 50))
        # TODO : afiseaza si timpul curent al jucatorilor preferabil sa scada constant, citeste fct din Player pt asta
            
        # Updatam display
        pygame.display.flip()
        

    