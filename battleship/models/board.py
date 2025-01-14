"""
Module représentant le plateau de jeu.
"""

from typing import List, Tuple, Optional
from .ship import Ship

class Board:
    def __init__(self, size: int = 10):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.ships: List[Ship] = []
        self.shots: List[Tuple[int, int]] = []
    
    def place_ship(self, ship: Ship, x: int, y: int, horizontal: bool) -> bool:
        """Place un navire sur le plateau"""
        if not self.can_place_ship(ship, x, y, horizontal):
            return False
        
        positions = []
        for i in range(ship.size):
            pos_x = x + (i if horizontal else 0)
            pos_y = y + (0 if horizontal else i)
            positions.append((pos_x, pos_y))
            self.grid[pos_y][pos_x] = ship
        
        for pos_x, pos_y in positions:
            ship.add_position(pos_x, pos_y)
        
        self.ships.append(ship)
        return True
    
    def can_place_ship(self, ship: Ship, x: int, y: int, horizontal: bool) -> bool:
        """Vérifie si un navire peut être placé à une position"""
        for i in range(ship.size):
            pos_x = x + (i if horizontal else 0)
            pos_y = y + (0 if horizontal else i)
            
            if not self._is_valid_position(pos_x, pos_y):
                return False
            
            if self.grid[pos_y][pos_x] is not None:
                return False
        
        return True
    
    def receive_shot(self, x: int, y: int) -> Tuple[bool, Optional[Ship]]:
        """Reçoit un tir et retourne si c'est un hit et le navire coulé"""
        self.shots.append((x, y))
        
        if not self._is_valid_position(x, y):
            return False, None
        
        ship = self.grid[y][x]
        if ship is None:
            return False, None
        
        ship.hit(x, y)
        return True, ship if ship.is_sunk() else None
    
    def _is_valid_position(self, x: int, y: int) -> bool:
        """Vérifie si une position est valide sur le plateau"""
        return 0 <= x < self.size and 0 <= y < self.size 