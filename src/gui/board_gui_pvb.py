import pygame
import threading
import time
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
from .dialogs import show_promotion_dialog, draw_game_over
from settings import SettingsManager
import os

PIECE_MAPPING = {
    'white-pawn.png': 'wp.png',
    'white-rook.png': 'wr.png',
    'white-knight.png': 'wn.png',
    'white-bishop.png': 'wb.png',
    'white-queen.png': 'wq.png',
    'white-king.png': 'wk.png',
    'black-pawn.png': 'bp.png',
    'black-rook.png': 'br.png',
    'black-knight.png': 'bn.png',
    'black-bishop.png': 'bb.png',
    'black-queen.png': 'bq.png',
    'black-king.png': 'bk.png'
}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets') 
BOARDS_DIR = os.path.join(ASSETS_DIR, 'boards')
PIECES_DIR = os.path.join(ASSETS_DIR, 'pieces')  

# Helper function for threaded bot move calculation
def get_bot_move(game, move_queue):
    # This runs in a separate thread
    try:
        move = game.currentPlayer.decideMove([], game.boardToFen())
        move_queue.put(move)
    except Exception as e:
        print(f"Error in bot thread: {e}")

# pygame setup
def boardDisplayPvB(player1=None, player2=None, theme_name="gold", fen=startingFen, turn='white', bot_depth=5):
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    running = True
    dt = 0
    
    # Board parameters
    Board_side = 8
    square_size = 120
    board_width = Board_side * square_size
    board_height = Board_side * square_size

    # Position the board on the screen (centered)
    board_x = (1920 - board_width) // 2
    board_y = (1080 - board_height) // 2
    
    # Import themes from SettingsManager
    theme_board_name = SettingsManager.get_theme_board()
    theme_piece_name = SettingsManager.get_theme_pieces()
    
    # Board Background handling
    board_image = None
    if theme_board_name != "Classic":
        board_img_path = os.path.join(BOARDS_DIR, theme_board_name)
        if os.path.exists(board_img_path):
             try:
                 loaded_img = pygame.image.load(board_img_path)
                 board_image = pygame.transform.scale(loaded_img, (board_width, board_height))
             except:
                 pass
    
    # Set default colors if board image is not available
    if not board_image:
        theme = get_theme("classic") 
        theme_data = get_theme(theme_board_name.replace(".png","").lower()) 
        
        white = theme_data.get("light_square", (240, 217, 181))
        black = theme_data.get("dark_square", (181, 136, 99))
        background = theme_data.get("background", (30, 30, 30))
    else:
        background = (30, 30, 30)

    
    # Turn variables
    font_small = pygame.font.Font(None, 60)  # Smaller font for turn text
    if not player1:
        player1 = Human('white', 'Marius', 600)
    if not player2:
        player2 = Bot('black', 'Andrei', 600, depth=bot_depth)
        
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
                # Log game result
                print(f'{(f"Winner is {Game.winner.upper()}" if GameStatus.STALEMATE != Game.status else "Stalemate")} after {Game.moveCnt} moves by {Game.status.name}')
                
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

                    # Update game state
                    gameState(Game.board, Game.currentPlayer)

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
                Game.applyExternalMove(start_pos, end_pos, promotion_type)
                
                gameState(Game.board, Game.currentPlayer)
                is_thinking = False
                
            except queue.Empty:
                pass # Still thinking

        # Fill screen with background
        screen.fill(background)
        
        # Draw Chess Board
        if board_image:
             screen.blit(board_image, (board_x, board_y))
        else:
            for row in range(Board_side):
                for col in range(Board_side):
                    # Calculate position
                    x = board_x + col * square_size
                    y = board_y + row * square_size
                    
                    # Choose color (white if sum is even, black if odd)
                    if (row + col) % 2 == 0:
                        color = white
                    else:
                        color = black
                    
                    # Draw the square
                    pygame.draw.rect(screen, color, (x, y, square_size, square_size))
        
    
        for row in range(Board_side):
            for col in range(Board_side):
                piece = Game.board.getPiece((row, col))
                if not isinstance(piece, Empty):
                    # Calculate top-left corner of square
                    x = board_x + col * square_size
                    y = board_y + row * square_size
                    
                    # Get the PNG image for this piece
                    image_path = None
                    theme_specific_path = os.path.join(PIECES_DIR, theme_piece_name, piece.image)
                    default_path = os.path.join(ASSETS_DIR, piece.image)
                    
                    if piece.image in PIECE_MAPPING:
                        mapped_name = PIECE_MAPPING[piece.image]
                        mapped_path = os.path.join(PIECES_DIR, theme_piece_name, mapped_name)
                        if os.path.exists(mapped_path):
                            image_path = mapped_path
                        else:
                            image_path = default_path
                    else:
                         image_path = default_path

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
                   
        
        # Highlight selected piece
        if Game.selectedPiecePos:
            row, col = Game.selectedPiecePos
            x = board_x + col * square_size
            y = board_y + row * square_size
            pygame.draw.rect(screen, (255, 155, 115), (x, y, square_size, square_size), 5)
        
        # Draw possible moves
        for move in Game.possibleMoves:
            row, col = move
            x = board_x + col * square_size + square_size // 2
            y = board_y + row * square_size + square_size // 2
            # Green circle for possible move
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
                
        # Display current turn
        turn_text = f"Turn: {Game.currentPlayer.colour.capitalize()}"
        turn_surface = font_small.render(turn_text, True, (255, 255, 255))
        screen.blit(turn_surface, (50, 50))
            
        # Update display and handle game over
        if Game.gameOver:
            msg = "Game Over"
            if Game.winner:
                 msg = f"Game Over, {Game.winner.capitalize()} wins!"
            elif Game.status == GameStatus.STALEMATE:
                 msg = "Game Over, Stalemate!"
            
            draw_game_over(screen, msg)

        pygame.display.flip()