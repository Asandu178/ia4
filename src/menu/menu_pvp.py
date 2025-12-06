import sys
import os
import pygame
import threading

# Add parent directory to path to handle imports if run directly (though usually run from main)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from menu.Button import Button
from menu.background import create_background
from gui.board_gui_pvp import boardDisplay as boardDisplayPvP
from network.network import Network
import server

from menu.menu_time import time_selection_menu

def start_local_game():
    time_limit = time_selection_menu()
    if time_limit == "BACK":
        return
        
    boardDisplayPvP(time_limit=time_limit)
    # Reset display mode after game ends
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chess Game - PvP Menu")

def start_host_game():
    time_limit = time_selection_menu()
    if time_limit == "BACK":
        return

    print("Starting server...")
    # Start server in a separate thread
    s = server.Server(time_limit=time_limit)
    t = threading.Thread(target=s.run)
    t.daemon = True
    t.start()
    
    # Host connects as the first client
    network = Network()
    
    # Setup loading screen
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chess Game - Waiting for Opponent")
    
    # Generate background
    wall_surface = create_background(screen_width, screen_height)
    
    font = pygame.font.Font(None, 50)
    
    waiting = True
    player_connected = False
    
    while waiting:
        # Check if we have 2 clients (Host + Opponent)
        # s.clients is updated in the server thread
        if len(s.clients) >= 2:
            player_connected = True
            waiting = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # Draw
        screen.blit(wall_surface, (0, 0))
        
        # Draw status text
        if not player_connected:
            text_str = f"Waiting for opponent... ({len(s.clients)}/2)"
        else:
            text_str = "Opponent connected! Starting..."
            
        text_surf = font.render(text_str, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(screen_width // 2, screen_height // 2))
        
        # Add a loading animation
        shadow_surf = font.render(text_str, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=(screen_width // 2 + 2, screen_height // 2 + 2))
        
        screen.blit(shadow_surf, shadow_rect)
        screen.blit(text_surf, text_rect)
        
        pygame.display.flip()
        pygame.time.wait(100) # Small delay to reduce CPU usage

    # Proceed to game
    player_color = 'white'
    boardDisplayPvP(network=network, player_color=player_color, time_limit=time_limit)
    
    # Reset display mode after game ends
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chess Game - PvP Menu")

def start_join_game():
    # TODO: Create a GUI for IP input. For now, using console as requested.
    pygame.display.quit() # Close window temporarily to focus on console
    ip = input("Enter Host IP (default localhost): ") or 'localhost'
    pygame.display.init() 
    
    network = Network(ip)

    
    player_color = 'black'
    boardDisplayPvP(network=network, player_color=player_color, time_limit=network.time_limit)
    
    # Reset display mode after game ends
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chess Game - PvP Menu")

def back_to_main():
    return "BACK"

def pvp_menu():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chess Game - PvP Menu")

    # Generate background
    wall_surface = create_background(screen_width, screen_height)

    # Button dimensions and spacing
    btn_width = 350
    btn_height = 80 
    btn_x = (screen_width - btn_width) // 2
    start_y = 100
    gap = 90

    buttons = [
        Button(btn_x, start_y, btn_width, btn_height, 'Local Play', start_local_game),
        Button(btn_x, start_y + gap, btn_width, btn_height, 'Host Game', start_host_game),
        Button(btn_x, start_y + gap * 2, btn_width, btn_height, 'Join Game', start_join_game),
        Button(btn_x, start_y + gap * 3, btn_width, btn_height, 'Back', back_to_main)
    ]

    # Prevent immediate click through from previous menu
    # Wait until mouse is released
    while pygame.mouse.get_pressed()[0]:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.wait(10)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Draw background
        screen.blit(wall_surface, (0, 0))

        # Draw buttons
        for btn in buttons:
            action = btn.process()
            btn.draw(screen)
            if action == "BACK":
                running = False 

        pygame.display.flip()

    # Restore main menu caption when returning
    pygame.display.set_caption("Chess Game - Main Menu")

if __name__ == "__main__":
    pvp_menu()
