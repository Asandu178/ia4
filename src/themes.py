

# Tema clasică - clasic chess style
CLASSIC = {
    "light_square": (240, 217, 181),  # Bej
    "dark_square": (181, 136, 99),    # Maro
    "background": (30, 30, 30),
    "border": (100, 100, 100),
    "name": "Classic"
}

# Tema moderna - dark mode
MODERN_DARK = {
    "light_square": (120, 150, 200),  # Albastru deschis
    "dark_square": (40, 60, 100),     # Albastru inchis
    "background": (20, 20, 25),
    "border": (200, 200, 200),
    "name": "Modern Dark"
}

# Tema verde
GREEN = {
    "light_square": (180, 220, 150),  # Verde deschis
    "dark_square": (100, 150, 80),    # Verde inchis
    "background": (25, 25, 20),
    "border": (150, 200, 100),
    "name": "Green"
}

# Tema purpurie
PURPLE = {
    "light_square": (220, 180, 240),  # Violet deschis
    "dark_square": (140, 80, 180),    # Violet inchis
    "background": (20, 15, 30),
    "border": (200, 150, 255),
    "name": "Purple"
}

# Tema rosie
RED = {
    "light_square": (255, 200, 180),  # Rosu deschis
    "dark_square": (200, 60, 60),     # Rosu inchis
    "background": (30, 15, 15),
    "border": (255, 100, 100),
    "name": "Red"
}

# Tema gri
GRAYSCALE = {
    "light_square": (220, 220, 220),  # Gri deschis
    "dark_square": (80, 80, 80),      # Gri inchis
    "background": (40, 40, 40),
    "border": (150, 150, 150),
    "name": "Grayscale"
}

# Tema oceanul
OCEAN = {
    "light_square": (100, 200, 255),  # Albastru deschis
    "dark_square": (20, 100, 180),    # Albastru inchis
    "background": (10, 30, 50),
    "border": (150, 220, 255),
    "name": "Ocean"
}

# Tema auriu
GOLD = {
    "light_square": (255, 245, 200),  # Auriu deschis
    "dark_square": (180, 140, 50),    # Auriu inchis
    "background": (30, 25, 10),
    "border": (255, 215, 0),
    "name": "Gold"
}

# Dictionar cu toate temele
THEMES = {
    "classic": CLASSIC,
    "modern_dark": MODERN_DARK,
    "green": GREEN,
    "purple": PURPLE,
    "red": RED,
    "grayscale": GRAYSCALE,
    "ocean": OCEAN,
    "gold": GOLD,
}

def get_theme(theme_name):
    return THEMES.get(theme_name.lower(), theme_name)
