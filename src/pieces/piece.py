class Piece:
    Board = None
    value = -1
    def __init__(self, colour: str, image: str, position: tuple[int, int] = None):
        self.colour = colour
        self.image = image
        self.position = position
    
    def __repr__(self):
        return f"{self.type}"
    
    def moveList(self) -> list[tuple[int, int]]:
        pass
        