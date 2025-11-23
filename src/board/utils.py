def validPos(position : tuple[int, int]):
    if (position[0] < 0 or position[0] >= 8 or position[1] < 0 or position[1] >= 8):
        return False
    return True