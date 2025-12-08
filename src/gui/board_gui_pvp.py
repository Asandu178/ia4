import pygame
import time
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

# Mapping for theme filenames (e.g. white-pawn.png -> wp.png)
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

# Main function for displaying the PvP board
def boardDisplay(player1=None, player2=None, theme_name="gold", fen=startingFen, turn='white', network=None, player_color=None, time_limit=None):
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

    
    # Fonts
    font_small = pygame.font.Font(None, 60)  # Font for turn text
    font_timer = pygame.font.Font(None, 80) # Font for timers

    if not player1:
        player1 = Human('white', 'Marius', 600)
        # Check if time_limit is provided, otherwise default to 600 or player default
        if time_limit is not None:
             if time_limit == -1:
                 player1.time = None
             else:
                 player1.time = time_limit
    if not player2:
        player2 = Human('black', 'Andrei', 600)
        if time_limit is not None:
             if time_limit == -1:
                 player2.time = None
             else:
                 player2.time = time_limit

    Player1 = player1
    Player2 = player2
    Game = ChessGame(Player1, Player2, fen, turn)
    Player1.board = Game.board
    Player2.board = Game.board
    
    if time_limit is not None:
        if time_limit == -1:
            Player1.time = None
            Player2.time = None
        else:
            Player1.time = time_limit
            Player2.time = time_limit
        
    start_ticks = pygame.time.get_ticks()

    while running:
        current_time = pygame.time.get_ticks()
        
        
        # Determine orientation
        if network:
             orientation = player_color # Fixed for network play
        else:
             orientation = Game.currentPlayer.colour # Dynamic for local play

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if Game.winner != None or Game.gameOver:
                 # TODO : handle gameover screen using
                print(f'{(f"Winner is {Game.winner.upper()}" if GameStatus.STALEMATE != Game.status else "Stalemate")} after {Game.moveCnt} moves by {Game.status.name}')

                
            if not Game.gameOver:
                # Update current player time check for timeout
                if Game.currentPlayer.time is not None:
                    # Calculate elapsed since start of turn
                     elapsed = time.time() - Game.currentPlayer.start
                     if Game.currentPlayer.time - elapsed <= 0:
                         Game.status = GameStatus.TIMEOUT
                         Game._updateGameState() # Trigger timeout logic

                if network and Game.currentPlayer.colour != player_color:
                    move = network.receive()
                    if move:
                        Game.applyExternalMove(move['start'], move['end'], move['promotion'])
                
                elif event.type == pygame.MOUSEBUTTONDOWN or isinstance(Game.currentPlayer, Bot):
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    # Transform mouse click to logical board coordinates
                    clicked_col = (mouse_x - board_x) // square_size
                    clicked_row = (mouse_y - board_y) // square_size
                    
                    if orientation == 'black':
                        row = 7 - clicked_row
                        col = 7 - clicked_col
                    else:
                        row = clicked_row
                        col = clicked_col
            
                
                    pos = (row, col)

                    result = Game.handleClick(pos)

                    if result == 'PROMOTION_NEEDED':
                        # Determine color of the current player
                        color = Game.currentPlayer.colour
                        promoted_piece_name = show_promotion_dialog(screen, color)
                        if Game.handleClick(pos, promoted_piece_name):
                            if network:
                                _, start, end = Game.board.last_move
                                network.send({"start": start, "end": end, "promotion": promoted_piece_name})
                    
                    elif result == True:
                        if network:
                            _, start, end = Game.board.last_move
                            network.send({"start": start, "end": end, "promotion": None})

                    # Update Game state
                    gameState(Game.board, Game.currentPlayer)


        # Fill background
        screen.fill(background)
        
        # Draw Chess Board
        if board_image:
            if orientation == 'black':
                 rotated_board = pygame.transform.rotate(board_image, 180)
                 screen.blit(rotated_board, (board_x, board_y))
            else:
                 screen.blit(board_image, (board_x, board_y))
        else:
            for row in range(Board_side):
                for col in range(Board_side):
                    # Visual coordinates calculation
                    if orientation == 'black':
                        draw_row = 7 - row
                        draw_col = 7 - col
                    else:
                         draw_row = row
                         draw_col = col
                    
                    # Calculate position
                    x = board_x + draw_col * square_size
                    y = board_y + draw_row * square_size
                    
                    # Choose color (white if sum is even, black if odd)
                    if (row + col) % 2 == 0:
                        color = white
                    else:
                        color = black
                    
                    # Draw the square
                    pygame.draw.rect(screen, color, (x, y, square_size, square_size))
        
        # Draw Pieces
        for row in range(Board_side):
            for col in range(Board_side):
                piece = Game.board.getPiece((row, col))
                if not isinstance(piece, Empty):
                    
                    # Calculate visual position
                    if orientation == 'black':
                         draw_row = 7 - row
                         draw_col = 7 - col
                    else:
                         draw_row = row
                         draw_col = col
                    
                    # Calculate top-left corner of square
                    x = board_x + draw_col * square_size
                    y = board_y + draw_row * square_size
                    
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
                   
        
        # Draw highlight on selected piece
        if Game.selectedPiecePos:
            row, col = Game.selectedPiecePos
            
            if orientation == 'black':
                 draw_row = 7 - row
                 draw_col = 7 - col
            else:
                 draw_row = row
                 draw_col = col

            x = board_x + draw_col * square_size
            y = board_y + draw_row * square_size
            pygame.draw.rect(screen, (255, 155, 115), (x, y, square_size, square_size), 5)
        
        # Draw possible moves
        for move in Game.possibleMoves:
            row, col = move
            
            if orientation == 'black':
                 draw_row = 7 - row
                 draw_col = 7 - col
            else:
                 draw_row = row
                 draw_col = col
                 
            x = board_x + draw_col * square_size + square_size // 2
            y = board_y + draw_row * square_size + square_size // 2
            # Green circle for possible move
            pygame.draw.circle(screen, (0, 255, 0), (x, y), 15)
        
        # Highlight last move
        if Game.moveCnt > 0 and Game.board.last_move:
            # Assuming Game.last_move is (piece, original_position)
            moved_piece, from_pos, _ = Game.board.last_move
            
            # Highlight FROM square (where piece came from)
            if from_pos:
                row, col = from_pos
                
                if orientation == 'black':
                     draw_row = 7 - row
                     draw_col = 7 - col
                else:
                     draw_row = row
                     draw_col = col

                x = board_x + draw_col * square_size
                y = board_y + draw_row * square_size
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
                
                if orientation == 'black':
                     draw_row = 7 - row
                     draw_col = 7 - col
                else:
                     draw_row = row
                     draw_col = col

                x = board_x + draw_col * square_size
                y = board_y + draw_row * square_size
                # Draw semi-transparent overlay
                highlight_surf = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                highlight_surf.fill((50, 255, 50, 64))
                screen.blit(highlight_surf, (x, y))
                pygame.draw.rect(screen, ((50, 255, 50, 64)), (x, y, square_size, square_size), 3)
                
        # Display current turn
        turn_text = f"Turn: {Game.currentPlayer.colour.capitalize()}"
        turn_surface = font_small.render(turn_text, True, (255, 255, 255))
        screen.blit(turn_surface, (50, 50))
        
        # Display Timers
        if time_limit is not None and time_limit != -1:
             def format_time(seconds):
                 mins = int(seconds) // 60
                 secs = int(seconds) % 60
                 return f"{mins:02}:{secs:02}"
             
             # Calculate real-time value for current player
             p1_time = Player1.time
             if Game.currentPlayer == Player1 and not Game.firstMove and not Game.gameOver:
                 p1_time -= (time.time() - Player1.start)
             
             p2_time = Player2.time
             if Game.currentPlayer == Player2 and not Game.firstMove and not Game.gameOver:
                 p2_time -= (time.time() - Player2.start)
                 
             # Clamp to 0
             p1_time = max(0, p1_time)
             p2_time = max(0, p2_time)
             
             p1_timer_surf = font_timer.render(format_time(p1_time), True, (255, 255, 255) if Game.currentPlayer == Player1 else (150, 150, 150))
             p2_timer_surf = font_timer.render(format_time(p2_time), True, (255, 255, 255) if Game.currentPlayer == Player2 else (150, 150, 150))
             
             # Position timers
             screen.blit(p1_timer_surf, (50, 150)) # Player 1 (White)
             screen.blit(p2_timer_surf, (50, 250)) # Player 2 (Black) - maybe improve positioning later
             
             pygame.draw.circle(screen, (255, 255, 255), (30, 175), 10) # White indicator
             pygame.draw.circle(screen, (0, 0, 0), (30, 275), 10) # Black indicator
            
        # Update display and handle game over
        if Game.gameOver:
            msg = "Game Over"
            if Game.winner:
                msg = f"Game Over, {Game.winner.capitalize()} wins!"
            elif Game.status == GameStatus.STALEMATE:
                msg = "Game Over, Stalemate!"
            
            draw_game_over(screen, msg)

        pygame.display.flip()