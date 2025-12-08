import pygame
import random

def create_background(width, height):
    """
    Generates a stone wall pattern surface.
    """
    # Create the base surface for the background
    wall_surface = pygame.Surface((width, height))
    wall_surface.fill((40, 40, 40)) 
    
    brick_width = 100
    brick_height = 50
    
    # Iterate through rows and columns to draw bricks
    for row in range(0, height, brick_height):
        # Offset every other row for a brick wall effect
        offset = -(brick_width // 2) if (row // brick_height) % 2 == 1 else 0
        
        for col in range(offset, width, brick_width):
            # Randomize brick color slightly for realism
            shade = random.randint(60, 100)
            brick_color = (shade, shade, shade)
            
            rect_x = col + 2
            rect_y = row + 2
            rect_w = brick_width - 4
            rect_h = brick_height - 4
            
            # Draw the main brick rectangle
            pygame.draw.rect(wall_surface, brick_color, (rect_x, rect_y, rect_w, rect_h))
            
            # Add highlight and shadow lines to give a 3D effect
            pygame.draw.line(wall_surface, (shade + 30, shade + 30, shade + 30), (rect_x, rect_y), (rect_x + rect_w, rect_y))
            pygame.draw.line(wall_surface, (shade + 30, shade + 30, shade + 30), (rect_x, rect_y), (rect_x, rect_y + rect_h))
            pygame.draw.line(wall_surface, (shade - 20, shade - 20, shade - 20), (rect_x, rect_y + rect_h), (rect_x + rect_w, rect_y + rect_h))
            pygame.draw.line(wall_surface, (shade - 20, shade - 20, shade - 20), (rect_x + rect_w, rect_y), (rect_x + rect_w, rect_y + rect_h))
            
    return wall_surface
