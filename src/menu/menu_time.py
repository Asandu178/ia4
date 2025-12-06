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

    # Generate background
    wall_surface = create_background(screen_width, screen_height)

    # Variables to store selection
    selected_time = None
    
    # Helper to create button callback
    def select_time(seconds):
        nonlocal selected_time
        selected_time = seconds

    def go_back():
        nonlocal selected_time
        selected_time = "BACK"

    # Button dimensions and spacing
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
        ("Unlimited", None)
    ]

    buttons = []
    
    for i, (label, seconds) in enumerate(options):
        btn = Button(btn_x, start_y + i * gap, btn_width, btn_height, label, 
                     lambda s=seconds: select_time(s))
        buttons.append(btn)
        
    # Back button
    buttons.append(Button(btn_x, start_y + len(options) * gap + 20, btn_width, btn_height, "Back", go_back))

    # Prevent immediate click through
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

        if selected_time is not None:
            running = False
            break

        # Draw background
        screen.blit(wall_surface, (0, 0))

        # Draw buttons
        for btn in buttons:
            res = btn.process()
            btn.draw(screen)
            if res is not None:
                pass

        pygame.display.flip()

    return selected_time
