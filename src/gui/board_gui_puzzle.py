import pygame
import threading
import queue
import random
import os
import sys

# Add parent folder to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from themes import get_theme
from board.board import Board
from board.boardLogic import *
from board import utils
from pieces.empty import Empty
from game.chessGame import ChessGame
from game.player import Player
from game.human import Human
from game.bot import Bot
from .dialogs import show_promotion_dialog
from menu.Button import Button

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
PUZZLES_FILE = os.path.join(ASSETS_DIR, 'puzzles.txt')

# Load a random fen string from the puzzles file
def load_random_fen():
    try:
        f = open(PUZZLES_FILE, 'r')
        lines = f.readlines()
        f.close()
        
        fens = []
        for line in lines:
            if line.strip() != "":
                fens.append(line.strip())
        
        if len(fens) > 0:
            return random.choice(fens)
        else:
            return startingFen
    except:
        return startingFen

def get_best_move(bot, fen, result_queue):
    try:
        move = bot.decideMove([], fen)
        result_queue.put(move)
    except:
        result_queue.put(None)

def setup_game(fen_string):
    parts = fen_string.split(' ')
    if len(parts) > 1 and parts[1] == 'w':
        turn = 'white'
    else:
        turn = 'black'
        
    game = ChessGame(Human('white','Player',600), Human('black','Player',600), fen_string, turn)
    return game, turn

# Main function for displaying the puzzle board
def boardDisplayPuzzle(theme_name="gold"):
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Chess Puzzle Mode")
    clock = pygame.time.Clock()
    
    square_size = 120
    board_side = 8
    board_width = board_side * square_size
    board_height = board_side * square_size
    
    board_x = 300
    board_y = (1080 - board_height) // 2
    
    theme = get_theme(theme_name)
    light_color = theme["light_square"]
    dark_color = theme["dark_square"]
    background_color = theme["background"]
    
    font_msg = pygame.font.Font(None, 60)
    
    # Use a dictionary to keep the data of the puzzle
    puzzle_data = {}
    puzzle_data['running'] = True
    puzzle_data['fen'] = load_random_fen()
    
    game, turn = setup_game(puzzle_data['fen'])
    puzzle_data['game'] = game
    puzzle_data['turn'] = turn
    
    puzzle_data['target_move'] = None
    puzzle_data['status'] = "CALCULATING" 
    puzzle_data['message'] = "Calculating..."
    puzzle_data['retry_count'] = 0
    puzzle_data['show_hint'] = False
    
    analysis_bot = Bot('white', 'Stockfish', 0, depth=15)
    move_queue = queue.Queue()

    # Start calculating the best move of the puzzle in a separate thread
    def start_calculation():
        calc_thread = threading.Thread(target=get_best_move, args=(analysis_bot, puzzle_data['fen'], move_queue))
        calc_thread.daemon = True
        calc_thread.start()
    
    start_calculation()

    # Functions for the buttons
    def click_next():
        puzzle_data['fen'] = load_random_fen()
        g, t = setup_game(puzzle_data['fen'])
        puzzle_data['game'] = g
        puzzle_data['turn'] = t
        
        puzzle_data['target_move'] = None
        puzzle_data['status'] = "CALCULATING"
        puzzle_data['message'] = "Calculating..."
        puzzle_data['retry_count'] = 0
        puzzle_data['show_hint'] = False
        start_calculation()

    def click_retry():
        g, t = setup_game(puzzle_data['fen'])
        puzzle_data['game'] = g
        puzzle_data['status'] = "PLAYING"
        puzzle_data['retry_count'] = puzzle_data['retry_count'] + 1
        
        if puzzle_data['retry_count'] >= 4:
            puzzle_data['show_hint'] = True
            puzzle_data['message'] = "Hint: Check highlighted piece!"
        else:
            turn_text = puzzle_data['turn'].capitalize()
            puzzle_data['message'] = turn_text + " to move!"

    def click_back():
        puzzle_data['running'] = False

    # Create buttons
    btn_next = Button(1400, 400, 350, 80, 'Next Puzzle', click_next)
    btn_retry = Button(1400, 400, 350, 80, 'Try Again', click_retry)
    btn_back = Button(1400, 520, 350, 80, 'Back to Menu', click_back)
    
    # Game Loop
    while puzzle_data['running']:
        
        # Check if the bot finished calculating
        if puzzle_data['status'] == "CALCULATING":
            try:
                move = move_queue.get_nowait()
                puzzle_data['target_move'] = move
                puzzle_data['status'] = "PLAYING"
                
                turn_text = puzzle_data['turn'].capitalize()
                puzzle_data['message'] = turn_text + " to move!"
            except:
                pass # Still waiting

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                puzzle_data['running'] = False
            
            # Handle Clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if puzzle_data['status'] == "PLAYING":
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    # Check if click is inside board
                    if mouse_x >= board_x and mouse_x < board_x + board_width:
                        if mouse_y >= board_y and mouse_y < board_y + board_height:
                            
                            col = (mouse_x - board_x) // square_size
                            row = (mouse_y - board_y) // square_size
                            
                            current_game = puzzle_data['game']
                            moves_before = current_game.moveCnt
                            
                            # Standard click handling
                            result = current_game.handleClick((row, col))
                            
                            if result == 'PROMOTION_NEEDED':
                                color = current_game.currentPlayer.colour
                                promoted = show_promotion_dialog(screen, color)
                                current_game.handleClick((row, col), promoted)

                            # Check if a move happened
                            if current_game.moveCnt > moves_before:
                                # Get the move that was just made
                                last_move = current_game.board.last_move
                                piece = last_move[0]
                                start_pos = last_move[1]
                                end_pos = last_move[2]
                                
                                # What moves did we want?
                                target = puzzle_data['target_move']
                                target_start = target[0]
                                target_end = target[1]
                                target_promo = target[2]
                                
                                # Check if correct
                                match = False
                                if start_pos == target_start and end_pos == target_end:
                                    match = True
                                    # specific promotion check
                                    if target_promo != None:
                                        p = current_game.board.getPiece(end_pos)
                                        if p.type.lower() != target_promo.lower():
                                            match = False
                                
                                if match:
                                    puzzle_data['status'] = "SOLVED"
                                    puzzle_data['message'] = "Correct!"
                                else:
                                    puzzle_data['status'] = "FAILED"
                                    puzzle_data['message'] = "Incorrect."

        # Draw everything
        screen.fill(background_color)
        
        current_game = puzzle_data['game']
        
        # Draw squares
        for r in range(8):
            for c in range(8):
                x = board_x + c * square_size
                y = board_y + r * square_size
                
                if (r + c) % 2 == 0:
                    color = light_color
                else:
                    color = dark_color
                    
                pygame.draw.rect(screen, color, (x, y, square_size, square_size))
                
                # Draw hint (if needed)
                if puzzle_data['show_hint'] == True:
                    if puzzle_data['target_move'] != None:
                        if puzzle_data['status'] == "PLAYING":
                            hint_pos = puzzle_data['target_move'][0]
                            hint_r = hint_pos[0]
                            hint_c = hint_pos[1]
                            
                            if r == hint_r and c == hint_c:
                                pygame.draw.rect(screen, (0, 255, 255), (x, y, square_size, square_size), 5)

                # Highlight selected piece
                if current_game.selectedPiecePos == (r, c):
                     pygame.draw.rect(screen, (255, 155, 115), (x, y, square_size, square_size), 5)
                
                # Draw piece image
                p = current_game.board.getPiece((r, c))
                if isinstance(p, Empty) == False:
                    # Find Image
                    path = os.path.join(ASSETS_DIR, p.image)
                    try:
                        img = pygame.image.load(path)
                        # Center it
                        img_x = x + (square_size - img.get_width()) // 2
                        img_y = y + (square_size - img.get_height()) // 2
                        screen.blit(img, (img_x, img_y))
                    except:
                        # Fallback Circle
                        center_x = x + 60
                        center_y = y + 60
                        if p.colour == 'white':
                            pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 35)
                        else:
                            pygame.draw.circle(screen, (50, 50, 50), (center_x, center_y), 35)

        # Draw green circles for moves
        for move in current_game.possibleMoves:
            r = move[0]
            c = move[1]
            cx = board_x + c * square_size + 60
            cy = board_y + r * square_size + 60
            pygame.draw.circle(screen, (0, 255, 0), (cx, cy), 15)

        # Draw buttons and text
        text_surf = font_msg.render(puzzle_data['message'], True, (255, 255, 255))
        screen.blit(text_surf, (1400, 250))
        
        btn_back.process()
        btn_back.draw(screen)
        
        if puzzle_data['status'] == "SOLVED":
            btn_next.process()
            btn_next.draw(screen)
        elif puzzle_data['status'] == "FAILED":
            btn_retry.process()
            btn_retry.draw(screen)

        pygame.display.flip()
        clock.tick(60)
