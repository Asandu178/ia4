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
    try:
        s = server.Server(time_limit=time_limit)
    except OSError as e:
        print(f"Error starting server: {e}")
        return

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
    
    
    # Back button
    btn_back = Button(20, 20, 150, 50, 'Back', back_to_main)

    while waiting:
        events = pygame.event.get()
        # Check if we have 2 clients (Host + Opponent)
        # s.clients is updated in the server thread
        if len(s.clients) >= 2:
            player_connected = True
            waiting = False
            
        for event in events:
            if event.type == pygame.QUIT:
                s.stop()
                t.join(timeout=1.0)
                pygame.quit()
                sys.exit()
        
        # Process Back button
        action = btn_back.process()
        if action == "BACK":
            s.stop()
            # Wait for thread to finish to ensure port is released
            t.join(timeout=1.0) 
            return

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
        
        btn_back.draw(screen)
        
        pygame.display.flip()
        pygame.time.wait(100) # Small delay to reduce CPU usage

    # Proceed to game
    player_color = 'white'
    boardDisplayPvP(network=network, player_color=player_color, time_limit=time_limit)
    
    # Reset display mode after game ends
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chess Game - PvP Menu")

from menu.TextInput import TextInputBox

def start_join_game():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chess Game - Join Game")

    # Generate background
    wall_surface = create_background(screen_width, screen_height)
    
    # Create Text Input Box
    input_box_width = 400
    input_box_height = 60
    input_box_x = (screen_width - input_box_width) // 2
    input_box_y = (screen_height - input_box_height) // 2
    
    input_box = TextInputBox(input_box_x, input_box_y, input_box_width, input_box_height, placeholder="Enter IP (default: localhost)")
    
    font_instr = pygame.font.Font(None, 40)
    instruction_text = font_instr.render("Enter Host IP:", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(screen_width // 2, input_box_y - 50))
    
    # Back Button
    btn_back = Button(20, 20, 150, 50, 'Back', back_to_main)

    ip = None
    running = True
    
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            input_box.handle_event(event)
            
            
        action = btn_back.process()
        if action == "BACK":
            return # Return to PvP menu

        if input_box.done:
            ip = input_box.text
            if not ip:
                ip = 'localhost'
            running = False

        # Draw
        screen.blit(wall_surface, (0, 0))
        
        screen.blit(instruction_text, instruction_rect)
        input_box.draw(screen)
        btn_back.draw(screen)
        
        pygame.display.flip()
        pygame.time.wait(30)

    if ip:
        print(f"Connecting to {ip}...")
        try:
            network = None
            # Draw the "Connecting..." screen
            screen.blit(wall_surface, (0, 0))
            connect_text = font_instr.render(f"Connecting to {ip}...", True, (255, 255, 255))
            connect_rect = connect_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(connect_text, connect_rect)
            pygame.display.flip()
            
            # Attempt connection
            network = Network(ip)
            
            player_color = 'black'
            boardDisplayPvP(network=network, player_color=player_color, time_limit=network.time_limit)
        except Exception as e:
            print(f"Connection failed: {e}")
    
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
    
    # Wait for mouse release to prevent double clicking through menus
    while pygame.mouse.get_pressed()[0]:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.wait(10)

    # Restore main menu caption when returning
    pygame.display.set_caption("Chess Game - Main Menu")

if __name__ == "__main__":
    pvp_menu()
