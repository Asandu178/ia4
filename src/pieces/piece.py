class Piece:
    def __init__(self, type: str, image: str, position: tuple[int, int]):
        self.type = type
        self.image = image
        self.position = position
    
    def __repr__(self):
        return f"{self.type}"