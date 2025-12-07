import pygame

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.buttonText = buttonText
        self.image = None
        
        # Colors for Stone/Diamond theme (Grey Nuances)
        self.fillColors = {
            'normal': '#707070',     
            'hover': '#909090',      
            'pressed': '#505050',    
            'border_light': '#B0B0B0', 
            'border_dark': '#404040'   
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.Font(None, 40) 
        
        # Text - Auto-scale font size to fit in diamond width
        usable_width = self.width * 0.7 
        
        font_size = 40
        self.textSurf = self.font.render(self.buttonText, True, (255, 255, 255))
        
        while self.textSurf.get_width() > usable_width and font_size > 20:
            font_size -= 2
            self.font = pygame.font.Font(None, font_size)
            self.textSurf = self.font.render(self.buttonText, True, (255, 255, 255))
            
        self.textRect = self.textSurf.get_rect(center=self.rect.center) 

    def set_text(self, text):
        self.buttonText = text
        usable_width = self.width * 0.7 
        font_size = 40
        self.font = pygame.font.Font(None, font_size)
        self.textSurf = self.font.render(self.buttonText, True, (255, 255, 255))
        
        while self.textSurf.get_width() > usable_width and font_size > 20:
            font_size -= 2
            self.font = pygame.font.Font(None, font_size)
            self.textSurf = self.font.render(self.buttonText, True, (255, 255, 255))
            
        self.textRect = self.textSurf.get_rect(center=self.rect.center) 

    def process(self):
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0]:
                if self.onePress:
                    return self.onclickFunction()
                elif not self.alreadyPressed:
                    self.alreadyPressed = True
                    return self.onclickFunction()
            else:
                self.alreadyPressed = False

    def draw(self, screen):
        mousePos = pygame.mouse.get_pos()
        
        current_color = self.fillColors['normal']
        is_hovered = self.rect.collidepoint(mousePos)
        is_pressed = pygame.mouse.get_pressed()[0] and is_hovered

        if is_pressed:
            current_color = self.fillColors['pressed']
            if self.onclickFunction and not self.alreadyPressed:
                 self.alreadyPressed = True
                 return self.onclickFunction()
        elif is_hovered:
            current_color = self.fillColors['hover']
            self.alreadyPressed = False
        else:
            self.alreadyPressed = False

        # Diamond Points
        # Top, Right, Bottom, Left
        points = [
            (self.x + self.width // 2, self.y),
            (self.x + self.width, self.y + self.height // 2),
            (self.x + self.width // 2, self.y + self.height),
            (self.x, self.y + self.height // 2)
        ]

        # Draw Main Diamond Body
        pygame.draw.polygon(screen, current_color, points)
        
        
        
        # Upper Left Edge
        pygame.draw.line(screen, self.fillColors['border_light'], points[3], points[0], 3)
        # Upper Right Edge
        pygame.draw.line(screen, self.fillColors['border_light'], points[0], points[1], 3)
        
        # Bottom Right Edge
        pygame.draw.line(screen, self.fillColors['border_dark'], points[1], points[2], 3)
        # Bottom Left Edge
        pygame.draw.line(screen, self.fillColors['border_dark'], points[2], points[3], 3)

        # Text
        screen.blit(self.textSurf, self.textRect)
