import pygame
import sys
import os

# Add parent directory to path to import 'src' modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from menu.Button import Button
from menu.background import create_background
from settings import SettingsManager

# Asset paths definitions
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARDS_DIR = os.path.join(BASE_DIR, 'assets', 'boards')
PIECES_DIR = os.path.join(BASE_DIR, 'assets', 'pieces')

def get_available_boards():
    # Scan the assets directory for available board themes
    boards = ["Classic"]  # Default option for color-based board
    if os.path.exists(BOARDS_DIR):
        for f in os.listdir(BOARDS_DIR):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                boards.append(f)
    return boards

def get_available_piece_themes():
    # Scan the assets directory for available piece themes
    themes = ["classic"] # Default
    if os.path.exists(PIECES_DIR):
        for d in os.listdir(PIECES_DIR):
            if os.path.isdir(os.path.join(PIECES_DIR, d)):
                themes.append(d)
    return themes

def preferences_menu():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chess Game - Preferences")

    # Generate background
    wall_surface = create_background(screen_width, screen_height)

    # Load available options from filesystem
    board_options = get_available_boards()
    piece_options = get_available_piece_themes()

    # Helper functions to cycle through options when buttons are clicked
    def next_board():
        current = SettingsManager.get_theme_board()
        try:
            current_idx = board_options.index(current)
            next_idx = (current_idx + 1) % len(board_options)
        except ValueError:
            next_idx = 0
        SettingsManager.set_theme_board(board_options[next_idx])

    def next_pieces():
        current = SettingsManager.get_theme_pieces()
        try:
            current_idx = piece_options.index(current)
            next_idx = (current_idx + 1) % len(piece_options)
        except ValueError:
            next_idx = 0
        SettingsManager.set_theme_pieces(piece_options[next_idx])
    
    def back_to_menu():
        return "back" 
        # Signal to break loop

    btn_width = 400
    btn_height = 80
    btn_x = (screen_width - btn_width) // 2
    start_y = 100
    gap = 100

    # Create buttons with callbacks
    btn_board = Button(btn_x, start_y, btn_width, btn_height, f'Board Theme: ...', next_board)
    btn_pieces = Button(btn_x, start_y + gap, btn_width, btn_height, f'Piece Theme: ...', next_pieces)
    btn_back = Button(btn_x, start_y + gap * 2, btn_width, btn_height, 'Back', back_to_menu)
    
    buttons = [btn_board, btn_pieces, btn_back]

    running = True
    while running:
        # Get current settings to update button labels
        current_board = SettingsManager.get_theme_board()
        current_pieces = SettingsManager.get_theme_pieces()

        # Update button text to show current selection
        btn_board.set_text(f'Board Theme: {current_board}')
        btn_pieces.set_text(f'Piece Theme: {current_pieces}')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        screen.blit(wall_surface, (0, 0))

        for btn in buttons:
            action = btn.process()
            if action == "back":
                running = False
            btn.draw(screen)

        pygame.display.flip()
    
    # Wait for mouse release to avoid click-through to next screen
    while pygame.mouse.get_pressed()[0]:
        pygame.event.pump()

