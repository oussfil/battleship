"""
Module représentant un navire dans le jeu.
"""

from typing import List, Tuple

class Ship:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.positions: List[Tuple[int, int]] = []
        self.hits: List[Tuple[int, int]] = []
    
    def add_position(self, x: int, y: int):
        """Ajoute une position au navire"""
        self.positions.append((x, y))
    
    def hit(self, x: int, y: int) -> bool:
        """Enregistre un tir sur le navire"""
        if (x, y) in self.positions and (x, y) not in self.hits:
            self.hits.append((x, y))
            return True
        return False
    
    def is_sunk(self) -> bool:
        """Vérifie si le navire est coulé"""
        return len(self.hits) == self.size
