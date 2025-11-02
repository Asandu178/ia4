class Piece:
    def __init__(self, colour: str, type: str, image: str, position: tuple[int, int]):
        self.colour = colour
        self.type = type
        self.image = image
        self.position = position
    
    def __repr__(self):
        return f"hello from pawn {self.colour}"