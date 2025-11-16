# Example file showing a circle moving on screen
import pygame
from themes import get_theme

# pygame setup
def boardDisplay(theme_name="gold"):
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

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
      
        
        # Updatam display
        pygame.display.flip()
        

    pygame.quit()
