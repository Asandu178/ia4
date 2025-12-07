import pygame

class TextInputBox:
    def __init__(self, x, y, width, height, font_size=40, placeholder="Enter IP"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = ''
        self.font = pygame.font.Font(None, font_size)
        self.active = True 
        self.placeholder = placeholder
        self.done = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.done = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        # Draw background
        pygame.draw.rect(screen, (30, 30, 30), self.rect)
        
        # Render the text
        txt_surface = self.font.render(self.text, True, self.color)
        
        # Calculate width relative to box
        width = self.rect.width - 10 
        
        # Clip area to the input box so text doesn't spill out
        original_clip = screen.get_clip()
        screen.set_clip(self.rect)
        
        if not self.text:
            # Render placeholder if text is empty
            placeholder_surface = self.font.render(self.placeholder, True, (100, 100, 100))
            screen.blit(placeholder_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - placeholder_surface.get_height()) // 2))
        else:
            # Check if text is wider than the box
            if txt_surface.get_width() > width:
                # Align right (scrolling effect)
                screen.blit(txt_surface, (self.rect.x + width - txt_surface.get_width() + 5, self.rect.y + (self.rect.height - txt_surface.get_height()) // 2))
            else:
                # Align left (normal)
                screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - txt_surface.get_height()) // 2))
        
        # Restore original clip
        screen.set_clip(original_clip)
            
        # Blit the rect border
        pygame.draw.rect(screen, self.color, self.rect, 2)
