class Piece:
    Board = None
    value = -1
    def __init__(self, type: str, colour: str, image: str, position: tuple[int, int] = None):
        self.type = type
        self.colour = colour
        self.image = image
        self.position = position
    
    def __repr__(self):
        return f"{self.type}"
    
    def moveList(self):
        pass
        