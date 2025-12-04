import pygame

def show_promotion_dialog(screen, color):
    # Dialog dimensions
    dialog_width = 400
    dialog_height = 150
    screen_width, screen_height = screen.get_size()
    x = (screen_width - dialog_width) // 2
    y = (screen_height - dialog_height) // 2
    
    # Colors
    background_color = (200, 200, 200)
    border_color = (50, 50, 50)
    
    # Pieces to choose from
    pieces = [
        ("Queen", f'{color}-queen.png'),
        ("Rook", f'{color}-rook.png'),
        ("Bishop", f'{color}-bishop.png'),
        ("Knight", f'{color}-knight.png')
    ]
    
    # Draw dialog
    pygame.draw.rect(screen, background_color, (x, y, dialog_width, dialog_height))
    pygame.draw.rect(screen, border_color, (x, y, dialog_width, dialog_height), 2)
    
    # Draw pieces
    piece_size = 80 
    padding = 15
    start_x = x + padding
    
    rects = []
    
    for i, (name, img_name) in enumerate(pieces):
        try:
            img = pygame.image.load(f'./assets/{img_name}')
            img = pygame.transform.scale(img, (piece_size, piece_size))
            
            draw_x = start_x + i * (piece_size + padding)
            draw_y = y + (dialog_height - piece_size) // 2
            
            screen.blit(img, (draw_x, draw_y))
            rects.append((pygame.Rect(draw_x, draw_y, piece_size, piece_size), name))
        except Exception as e:
            print(f"Error loading image {img_name}: {e}")
            # Fallback text
            font = pygame.font.Font(None, 36)
            text = font.render(name[0], True, (0,0,0))
            draw_x = start_x + i * (piece_size + padding)
            draw_y = y + (dialog_height - piece_size) // 2
            screen.blit(text, (draw_x, draw_y))
            rects.append((pygame.Rect(draw_x, draw_y, piece_size, piece_size), name))

    pygame.display.flip()
    
    # Event loop for dialog
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, name in rects:
                    if rect.collidepoint(mouse_pos):
                        return name
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
