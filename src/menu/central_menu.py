import sys
import os
import pygame

# Add parent directory to path so we can import from 'src' packages
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from menu.Button import Button
from menu.background import create_background
from menu.menu_pvp import pvp_menu
from menu.menu_pvb import pvb_menu
from gui.board_gui_puzzle import boardDisplayPuzzle

from menu.preferences import preferences_menu

def start_pvp():
    pvp_menu()

def start_pvb():
    pvb_menu()
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chess Game - Main Menu")

def start_puzzle():
    boardDisplayPuzzle()
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chess Game - Main Menu")

def start_preferences():
    preferences_menu()
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chess Game - Main Menu")

def quit_game():
    pygame.quit()
    sys.exit()

def main_menu():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chess Game - Main Menu")

    # Generate background using the shared utility
    wall_surface = create_background(screen_width, screen_height)

    # Button dimensions and spacing
    btn_width = 350
    btn_height = 80 
    btn_x = (screen_width - btn_width) // 2
    start_y = 100
    gap = 90

    buttons = [
        Button(btn_x, start_y, btn_width, btn_height, 'Player vs Player', start_pvp),
        Button(btn_x, start_y + gap, btn_width, btn_height, 'Player vs Bot', start_pvb),
        Button(btn_x, start_y + gap * 2, btn_width, btn_height, 'Puzzle', start_puzzle),
        Button(btn_x, start_y + gap * 3, btn_width, btn_height, 'Preferences', start_preferences),
        Button(btn_x, start_y + gap * 4, btn_width, btn_height, 'Quit', quit_game)
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_game()

        # Draw pre-generated wall background
        screen.blit(wall_surface, (0, 0))

        for btn in buttons:
            btn.process()
            btn.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()

