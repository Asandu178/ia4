import sys
import os
import pygame
from menu.Button import Button
from menu.background import create_background

def time_selection_menu():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chess Game - Select Time Control")

    # Generate the standard background
    wall_surface = create_background(screen_width, screen_height)

    # Variable to store selected result
    selected_time = None
    
    # Callback to set the time limit
    def select_time(seconds):
        nonlocal selected_time
        selected_time = seconds

    # Callback to cancel selection
    def go_back():
        nonlocal selected_time
        selected_time = "BACK"

    # Button layout configuration
    btn_width = 300
    btn_height = 60 
    btn_x = (screen_width - btn_width) // 2
    start_y = 50
    gap = 70

    # Define time options
    # Label -> Seconds
    options = [
        ("1 Minute", 60),
        ("3 Minutes", 180),
        ("5 Minutes", 300),
        ("10 Minutes", 600),
        ("Unlimited", -1)
    ]

    buttons = []
    
    # Create buttons dynamically based on options
    for i, (label, seconds) in enumerate(options):
        # Use lambda with default argument to capture 'seconds' value
        btn = Button(btn_x, start_y + i * gap, btn_width, btn_height, label, 
                     lambda s=seconds: select_time(s))
        buttons.append(btn)
        
    # Add manual Back button
    buttons.append(Button(btn_x, start_y + len(options) * gap + 20, btn_width, btn_height, "Back", go_back))

    # Prevent immediate click through from previous screen
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
                pygame.quit()
                sys.exit()

        # If a selection was made, exit the loop
        if selected_time is not None:
            running = False
            break

        # Draw background
        screen.blit(wall_surface, (0, 0))

        # Update and draw buttons
        for btn in buttons:
            res = btn.process()
            btn.draw(screen)
            if res is not None:
                pass

        pygame.display.flip()

    
    # Wait for mouse release to prevent double clicking through menus
    while pygame.mouse.get_pressed()[0]:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.wait(10)

    return selected_time
