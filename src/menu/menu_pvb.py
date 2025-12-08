import pygame
import sys
import os

# Ensure src is in path to allow imports from other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from menu.Button import Button
from gui.board_gui_pvb import boardDisplayPvB
from themes import get_theme
from menu.background import create_background

def pvb_menu():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Player vs Bot - Select Difficulty")
    
    # Generate background using the common background utility
    wall_surface = create_background(screen_width, screen_height)
    
    # Fonts
    font_title = pygame.font.Font(None, 60)
    font_desc = pygame.font.Font(None, 40)
    
    running = True

    # Callbacks for difficulty selection
    def start_easy():
        # Depth 1: Very easy, makes mistakes
        boardDisplayPvB(bot_depth=1)
        # return to menu after game
        reset_display()

    def start_medium():
        # Depth 5: Intermediate challenge
        boardDisplayPvB(bot_depth=5)
        reset_display()

    def start_hard():
        # Depth 10: Strong bot
        boardDisplayPvB(bot_depth=10)
        reset_display()

    def start_demon():
        # Depth 30: Very strong, near grandmaster level
        boardDisplayPvB(bot_depth=30)
        reset_display()

    def back_to_main():
        nonlocal running
        running = False
        
    def reset_display():
        # Reset display after returning from game to ensure menu sizing is correct
        nonlocal screen
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Player vs Bot - Select Difficulty")

    # Button layout configuration
    btn_width = 350
    btn_height = 80
    
    # Center X
    center_x = (screen_width - btn_width) // 2
    
    start_y = 100
    gap = 90
    
    btn_easy = Button(center_x, start_y, btn_width, btn_height, 'Easy', start_easy)
    btn_medium = Button(center_x, start_y + gap, btn_width, btn_height, 'Medium', start_medium)
    btn_hard = Button(center_x, start_y + gap * 2, btn_width, btn_height, 'Hard', start_hard)
    btn_demon = Button(center_x, start_y + gap * 3, btn_width, btn_height, 'Demon', start_demon)
    
    btn_back = Button(center_x, start_y + gap * 4, btn_width, btn_height, 'Back', back_to_main)
    
    buttons = [btn_easy, btn_medium, btn_hard, btn_demon, btn_back]

    # Prevent immediate click through from previous menu
    # Wait until mouse is released before accepting input
    while pygame.mouse.get_pressed()[0]:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.wait(10)

    while running:
        screen.blit(wall_surface, (0, 0))
        
        # Draw Title
        title_surf = font_title.render("Select Bot Difficulty", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen_width // 2, 50))
        screen.blit(title_surf, title_rect)
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Draw and process Buttons
        for btn in buttons:
            btn.process()
            btn.draw(screen)
            
        pygame.display.flip()

    # Wait for mouse release to prevent double clicking through menus when returning
    while pygame.mouse.get_pressed()[0]:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.wait(10)
