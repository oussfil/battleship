"""
Module d'intelligence artificielle pour l'ordinateur.
"""

import random
from typing import List, Tuple, Optional
from .board import Board

class ComputerAI:
    """
    Intelligence artificielle pour l'ordinateur.
    
    Attributes:
        difficulty (str): Niveau de difficulté ('easy' ou 'hard')
        last_hit (Optional[Tuple[int, int]]): Dernière position touchée
        potential_targets (List[Tuple[int, int]]): Cibles potentielles après un hit
    """
    
    def __init__(self, difficulty: str = "hard"):
        self.difficulty = difficulty
        self.last_hit: Optional[Tuple[int, int]] = None
        self.potential_targets: List[Tuple[int, int]] = []
        self.successful_hits: List[Tuple[int, int]] = []
    
    def get_shot(self, board: Board) -> Tuple[int, int]:
        """
        Détermine la prochaine case à cibler.
        
        Args:
            board (Board): Plateau du joueur
            
        Returns:
            Tuple[int, int]: Coordonnées (x, y) du tir
        """
        if self.difficulty == "easy" or not self.last_hit:
            return self._random_shot(board)
        
        # Mode difficile : cible les cases adjacentes après un hit
        if not self.potential_targets:
            self._update_potential_targets(board, self.last_hit)
        
        if self.potential_targets:
            target = self.potential_targets.pop(0)
            if self._is_valid_target(board, target):
                return target
        
        return self._random_shot(board)
    
    def notify_hit(self, x: int, y: int, sunk: bool):
        """
        Notifie l'IA du résultat d'un tir.
        
        Args:
            x (int): Coordonnée X du tir
            y (int): Coordonnée Y du tir
            sunk (bool): True si un navire a été coulé
        """
        if sunk:
            self.last_hit = None
            self.potential_targets.clear()
            self.successful_hits.clear()
        else:
            self.last_hit = (x, y)
            self.successful_hits.append((x, y))
    
    def _random_shot(self, board: Board) -> Tuple[int, int]:
        """Choisit une case aléatoire non ciblée."""
        available_shots = [
            (x, y) for x in range(board.size) 
            for y in range(board.size) 
            if (x, y) not in board.shots
        ]
        return random.choice(available_shots)
    
    def _update_potential_targets(self, board: Board, pos: Tuple[int, int]):
        """Met à jour la liste des cibles potentielles."""
        x, y = pos
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # Si plusieurs hits consécutifs, détermine la direction
        if len(self.successful_hits) > 1:
            dx = self.successful_hits[-1][0] - self.successful_hits[-2][0]
            dy = self.successful_hits[-1][1] - self.successful_hits[-2][1]
            if (dx, dy) != (0, 0):
                directions = [(dx, dy), (-dx, -dy)]
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if self._is_valid_target(board, (new_x, new_y)):
                self.potential_targets.append((new_x, new_y))
    
    def _is_valid_target(self, board: Board, pos: Tuple[int, int]) -> bool:
        """Vérifie si une position est une cible valide."""
        x, y = pos
        return (board._is_valid_position(x, y) and 
                (x, y) not in board.shots) 