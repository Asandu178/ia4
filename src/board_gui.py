import pygame
import os
from themes import get_theme
from board.board import Board
from board.boardLogic import *
from board import utils
from pieces.empty import Empty

# pygame setup
def boardDisplay(theme_name="gold", fen=startingFen, turn='white'):
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
    
    # Font pentru piese
    font = pygame.font.Font(None, 80)
    
    # Variabile pentru selecția pieselor
    selected_piece = None
    selected_piece_pos = None
    possible_moves = []
    
    # Variabile pentru ture
    current_turn = turn  # Albul merge primul
    font_small = pygame.font.Font(None, 60)  # Font mai mic pentru litere în cercuri

    # Variabila suplimentare

    move_cnt = 0

    board = Board(8, 8)
    fenToBoard(board, fen)  # Pozitia de start
    

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = (mouse_x - board_x) // square_size
                row = (mouse_y - board_y) // square_size
                
                if utils.validPos((row, col)):
                    print(f"Clicked on square: ({row}, {col})")
                    
                    # If we have a selected piece and click on valid move
                    if selected_piece and (row, col) in possible_moves:

                        board.movePiece(selected_piece, (row, col))
                        # TODO: maybe implement a system that also displays the capture if any happened
                        # currently only a debugging implementation
                        # might have to change it to PGN
                        print(f"#{move_cnt}.{current_turn.capitalize()} moved {selected_piece}{selected_piece_pos} to {(row, col)}")
                        
                        # Switch turns
                        current_turn = 'black' if current_turn == 'white' else 'white'
                        # Increase move count
                        move_cnt = move_cnt + 1

                        status = gameState(board, current_turn)

                        winner = 'black' if current_turn == 'white' else 'white'

                        # TODO : handle winning screen !!!!!!!

                        if status == GameStatus.CHECKMATE:
                            print(f"Winner is {winner} by checkmate after {move_cnt} moves")

                        if status == GameStatus.STALEMATE:
                            print(f"Stalemate after {move_cnt} moves")

                        if status == GameStatus.TIMEOUT:
                            print(f"Winner is {winner} by timeout after {move_cnt} moves")

                        if status == GameStatus.RESIGN:
                            print(f"Winner is {winner} by resignation after {move_cnt} moves")

                        # Reset selection regardless
                        selected_piece = None
                        selected_piece_pos = None
                        possible_moves = []

                    else:
                        # Select new piece
                        piece = board.getPiece((row, col))
                        if not isinstance(piece, Empty) and piece.colour == current_turn:
                            selected_piece = piece
                            selected_piece_pos = (row, col)
                            possible_moves = getLegalMoves(piece)
                            print(f"Selected: {piece}, moves: {possible_moves}")
                        else:
                            # Deselect if clicking empty or opponent piece
                            selected_piece = None
                            selected_piece_pos = None
                            possible_moves = []

            
        


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
        
        # Desenez piesele
        for row in range(Board_side):
            for col in range(Board_side):
                piece = board.getPiece((row, col))
                if not isinstance(piece, Empty):
                    x = board_x + col * square_size + square_size // 2
                    y = board_y + row * square_size + square_size // 2
                    
                    # Alege culoarea in functie de culoarea piesei
                    if piece.colour == 'white':
                        piece_color = (255, 255, 255)
                    else:
                        piece_color = (50, 50, 50) 
                    
                    # Deseneaza cercul pentru piesa
                    pygame.draw.circle(screen, piece_color, (x, y), 35)
                   
        
        # Desenez highlight pe piesa selectata
        if selected_piece_pos:
            row, col = selected_piece_pos
            x = board_x + col * square_size
            y = board_y + row * square_size
            pygame.draw.rect(screen, (255, 155, 115), (x, y, square_size, square_size), 5)
        
        # Desenez mutarile posibile
        for move in possible_moves:
            row, col = move
            x = board_x + col * square_size + square_size // 2
            y = board_y + row * square_size + square_size // 2
            # Cercul verde pentru mutare
            pygame.draw.circle(screen, (0, 255, 0), (x, y), 15)
            
        # Afiseaza tura curenta
        turn_text = f"Turn: {current_turn.capitalize()}"
        turn_surface = font_small.render(turn_text, True, (255, 255, 255))
        screen.blit(turn_surface, (50, 50))
        
        # Updatam display
        pygame.display.flip()
        

    pygame.quit()