"""
Constantes utilisées dans le jeu de bataille navale.
"""

# Dimensions
GRID_SIZE = 10
CELL_SIZE = 40

# Couleurs
WATER_COLOR = "#FFFFFF"  # Blanc pour l'eau
SHIP_COLOR = "#808080"   # Gris pour les navires
HIT_COLOR = "#FF0000"    # Rouge pour les touches
MISS_COLOR = "#0000FF"   # Bleu pour les tirs manqués

# Configuration des navires
SHIPS_CONFIG = {
    "Porte-avions": 5,
    "Croiseur": 4,
    "Destroyer 1": 3,
    "Destroyer 2": 3,
    "Sous-marin 1": 2,
    "Sous-marin 2": 2
}

# États du jeu
GAME_PHASES = ["placement", "playing", "game_over"]

# Messages
PLACEMENT_MSG = "Placez votre {} ({} cases)"
TURN_MSG = "À vous de jouer !"
HIT_MSG = "Touché !"
SUNK_MSG = "Coulé !"
MISS_MSG = "Manqué !"

# Symboles
HIT_SYMBOL = "✗"  # Croix pour les touches
MISS_SYMBOL = "○"  # Cercle pour les tirs manqués 