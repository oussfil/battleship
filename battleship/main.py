"""
Point d'entrée principal du jeu de bataille navale.
"""

import tkinter as tk
from .models.board import Board
from .models.ship import Ship
from .utils.constants import *
from .models.computer_ai import ComputerAI
import time

class GameWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bataille Navale")
        
        # Configuration de la fenêtre
        self.geometry("1000x600")
        
        # Initialisation des plateaux
        self.player_board = Board()
        self.computer_board = Board()
        self.current_ship = None
        self.placement_horizontal = True
        self.game_phase = "placement"  # "placement" ou "playing"
        
        # Initialisation de l'IA
        self.computer_ai = ComputerAI("hard")
        
        # Statistiques
        self.stats = {
            'player_hits': 0,
            'player_misses': 0,
            'computer_hits': 0,
            'computer_misses': 0,
            'start_time': time.time()
        }
        
        self._init_ui()
        self._start_ship_placement()
    
    def _init_ui(self):
        """Initialise l'interface utilisateur"""
        # Frame principale
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill='both')
        
        # Frame de contrôle
        control_frame = tk.Frame(main_frame)
        control_frame.pack(side=tk.TOP, pady=10)
        
        # Bouton de rotation
        self.rotation_btn = tk.Button(
            control_frame,
            text="Rotation (H/V)",
            command=self._toggle_orientation
        )
        self.rotation_btn.pack(side=tk.LEFT, padx=5)
        
        # Label d'état
        self.status_label = tk.Label(control_frame, text="Placez vos navires")
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Frame des grilles
        grids_frame = tk.Frame(main_frame)
        grids_frame.pack(expand=True, fill='both', padx=20)
        
        # Grille du joueur
        player_frame = tk.Frame(grids_frame)
        player_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(player_frame, text="Votre flotte").pack()
        
        self.player_buttons = []
        player_grid = tk.Frame(player_frame)
        player_grid.pack()
        
        for y in range(GRID_SIZE):
            row = []
            for x in range(GRID_SIZE):
                btn = tk.Button(
                    player_grid,
                    width=2,
                    height=1,
                    bg=WATER_COLOR,
                    command=lambda x=x, y=y: self._player_cell_clicked(x, y)
                )
                btn.grid(row=y, column=x)
                row.append(btn)
            self.player_buttons.append(row)
        
        # Grille de l'ordinateur
        computer_frame = tk.Frame(grids_frame)
        computer_frame.pack(side=tk.RIGHT, padx=20)
        tk.Label(computer_frame, text="Flotte ennemie").pack()
        
        self.computer_buttons = []
        computer_grid = tk.Frame(computer_frame)
        computer_grid.pack()
        
        for y in range(GRID_SIZE):
            row = []
            for x in range(GRID_SIZE):
                btn = tk.Button(
                    computer_grid,
                    width=2,
                    height=1,
                    bg=WATER_COLOR,
                    command=lambda x=x, y=y: self._computer_cell_clicked(x, y)
                )
                btn.grid(row=y, column=x)
                row.append(btn)
            self.computer_buttons.append(row)
            
        # Frame des statistiques
        stats_frame = tk.Frame(main_frame)
        stats_frame.pack(side=tk.BOTTOM, pady=10)
        self.stats_label = tk.Label(stats_frame, text="")
        self.stats_label.pack()
        self._update_stats()
        
        # Ajout des listes de navires coulés
        self.sunk_ships_frame = tk.Frame(main_frame)
        self.sunk_ships_frame.pack(side=tk.BOTTOM, pady=5)
        
        # Liste des navires coulés du joueur
        player_sunk_frame = tk.Frame(self.sunk_ships_frame)
        player_sunk_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(player_sunk_frame, text="Vos navires coulés :").pack()
        self.player_sunk_list = tk.Label(player_sunk_frame, text="")
        self.player_sunk_list.pack()
        
        # Liste des navires coulés de l'ordinateur
        computer_sunk_frame = tk.Frame(self.sunk_ships_frame)
        computer_sunk_frame.pack(side=tk.RIGHT, padx=20)
        tk.Label(computer_sunk_frame, text="Navires ennemis coulés :").pack()
        self.computer_sunk_list = tk.Label(computer_sunk_frame, text="")
        self.computer_sunk_list.pack()
    
    def _update_stats(self):
        """Met à jour l'affichage des statistiques"""
        player_total = self.stats['player_hits'] + self.stats['player_misses']
        computer_total = self.stats['computer_hits'] + self.stats['computer_misses']
        
        player_accuracy = (self.stats['player_hits'] / player_total * 100 
                         if player_total > 0 else 0)
        computer_accuracy = (self.stats['computer_hits'] / computer_total * 100 
                           if computer_total > 0 else 0)
        
        game_time = int(time.time() - self.stats['start_time'])
        minutes = game_time // 60
        seconds = game_time % 60
        
        stats_text = (
            f"Joueur - Touches: {self.stats['player_hits']}, "
            f"Manqués: {self.stats['player_misses']}, "
            f"Précision: {player_accuracy:.1f}%\n"
            f"Ordinateur - Touches: {self.stats['computer_hits']}, "
            f"Manqués: {self.stats['computer_misses']}, "
            f"Précision: {computer_accuracy:.1f}%\n"
            f"Temps de jeu: {minutes}m {seconds}s"
        )
        self.stats_label.config(text=stats_text)
        
        # Mise à jour toutes les secondes
        self.after(1000, self._update_stats)
    
    def _player_cell_clicked(self, x: int, y: int):
        """Gère le clic sur la grille du joueur"""
        if self.game_phase == "placement":
            self._handle_placement(x, y)
    
    def _computer_cell_clicked(self, x: int, y: int):
        """Gère le clic sur la grille de l'ordinateur"""
        if self.game_phase == "playing":
            self._handle_shot(x, y)
    
    def _handle_placement(self, x: int, y: int):
        """Gère le placement d'un navire"""
        if not self.current_ship:
            return
            
        # Vérifier si le placement est possible
        if self.player_board.can_place_ship(
            self.current_ship, x, y, self.placement_horizontal
        ):
            # Placer le navire
            if self.player_board.place_ship(
                self.current_ship, x, y, self.placement_horizontal
            ):
                # Mettre à jour l'affichage
                positions = self.current_ship.positions
                for px, py in positions:
                    self.player_buttons[py][px].config(bg=SHIP_COLOR)
                
                # Passer au navire suivant
                self._start_ship_placement()
    
    def _handle_shot(self, x: int, y: int):
        """Gère un tir du joueur"""
        if (x, y) in self.computer_board.shots:
            return
        
        hit, sunk = self.computer_board.receive_shot(x, y)
        if hit:
            self.stats['player_hits'] += 1
            self.computer_buttons[y][x].config(bg=HIT_COLOR, text=HIT_SYMBOL)
            if sunk:
                self.status_label.config(text=f"{sunk.name} coulé !")
                self._update_sunk_ships()
                # Afficher le navire coulé
                for sx, sy in sunk.positions:
                    self.computer_buttons[sy][sx].config(bg=SHIP_COLOR, text=HIT_SYMBOL)
                if all(ship.is_sunk() for ship in self.computer_board.ships):
                    self._end_game(True)
                    return
            else:
                self.status_label.config(text="Touché !")
        else:
            self.stats['player_misses'] += 1
            self.computer_buttons[y][x].config(bg=MISS_COLOR, text=MISS_SYMBOL)
            self.status_label.config(text="Manqué !")
        
        self.after(500, self._computer_turn)
    
    def _computer_turn(self):
        """Tour de l'ordinateur"""
        x, y = self.computer_ai.get_shot(self.player_board)
        hit, sunk = self.player_board.receive_shot(x, y)
        
        self.computer_ai.notify_hit(x, y, sunk is not None)
        
        if hit:
            self.stats['computer_hits'] += 1
            self.player_buttons[y][x].config(bg=HIT_COLOR, text=HIT_SYMBOL)
            if sunk:
                self.status_label.config(text=f"L'ordinateur a coulé votre {sunk.name} !")
                self._update_sunk_ships()
                if all(ship.is_sunk() for ship in self.player_board.ships):
                    self._end_game(False)
            else:
                self.status_label.config(text="L'ordinateur vous a touché !")
        else:
            self.stats['computer_misses'] += 1
            self.player_buttons[y][x].config(bg=MISS_COLOR, text=MISS_SYMBOL)
            self.status_label.config(text="L'ordinateur a manqué !")
    
    def _toggle_orientation(self):
        """Change l'orientation du placement des navires"""
        self.placement_horizontal = not self.placement_horizontal
    
    def _update_player_grid(self):
        """Met à jour l'affichage de la grille du joueur"""
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.player_board.grid[y][x]:
                    self.player_buttons[y][x].config(bg=SHIP_COLOR)
    
    def _start_ship_placement(self):
        """Commence le placement des navires"""
        # Vérifie s'il reste des navires à placer
        for name, size in SHIPS_CONFIG.items():
            if not any(ship.name == name for ship in self.player_board.ships):
                self.current_ship = Ship(name, size)
                self.status_label.config(text=f"Placez votre {name} ({size} cases)")
                return
        
        # Si tous les navires sont placés, commence la partie
        self.game_phase = "playing"
        self.rotation_btn.config(state=tk.DISABLED)
        self.status_label.config(text="À vous de jouer !")
        self._place_computer_ships()
    
    def _place_computer_ships(self):
        """Place aléatoirement les navires de l'ordinateur"""
        import random
        for name, size in SHIPS_CONFIG.items():
            ship = Ship(name, size)
            placed = False
            while not placed:
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                horizontal = random.choice([True, False])
                if self.computer_board.place_ship(ship, x, y, horizontal):
                    placed = True
    
    def _end_game(self, player_won: bool):
        """Termine la partie"""
        self.game_phase = "game_over"
        message = "Félicitations ! Vous avez gagné !" if player_won else "Game Over ! L'ordinateur a gagné !"
        
        # Afficher tous les navires de l'ordinateur
        if player_won:
            for ship in self.computer_board.ships:
                for x, y in ship.positions:
                    self.computer_buttons[y][x].config(bg=SHIP_COLOR)
        
        # Afficher la boîte de dialogue de fin
        dialog = tk.Toplevel(self)
        dialog.title("Fin de partie")
        
        tk.Label(dialog, text=message, pady=10).pack()
        
        stats_text = (
            f"Statistiques finales :\n"
            f"Joueur - Touches: {self.stats['player_hits']}, "
            f"Manqués: {self.stats['player_misses']}\n"
            f"Ordinateur - Touches: {self.stats['computer_hits']}, "
            f"Manqués: {self.stats['computer_misses']}"
        )
        tk.Label(dialog, text=stats_text, pady=10).pack()
        
        tk.Button(
            dialog,
            text="Nouvelle partie",
            command=lambda: [dialog.destroy(), self._reset_game()]
        ).pack(pady=5)
        
        tk.Button(
            dialog,
            text="Quitter",
            command=self.quit
        ).pack(pady=5)
    
    def _reset_game(self):
        """Réinitialise la partie"""
        # Réinitialiser les plateaux
        self.player_board = Board()
        self.computer_board = Board()
        
        # Réinitialiser l'IA
        self.computer_ai = ComputerAI("hard")
        
        # Réinitialiser les statistiques
        self.stats = {
            'player_hits': 0,
            'player_misses': 0,
            'computer_hits': 0,
            'computer_misses': 0,
            'start_time': time.time()
        }
        
        # Réinitialiser l'interface
        self.game_phase = "placement"
        self.current_ship = None
        self.placement_horizontal = True
        
        # Réinitialiser les boutons
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                self.player_buttons[y][x].config(bg=WATER_COLOR)
                self.computer_buttons[y][x].config(bg=WATER_COLOR)
        
        # Réactiver le bouton de rotation
        self.rotation_btn.config(state=tk.NORMAL)
        
        # Commencer le placement
        self._start_ship_placement()
    
    def _update_sunk_ships(self):
        """Met à jour l'affichage des navires coulés"""
        # Navires du joueur
        player_sunk = [ship.name for ship in self.player_board.ships if ship.is_sunk()]
        self.player_sunk_list.config(text="\n".join(player_sunk) if player_sunk else "Aucun")
        
        # Navires de l'ordinateur
        computer_sunk = [ship.name for ship in self.computer_board.ships if ship.is_sunk()]
        self.computer_sunk_list.config(text="\n".join(computer_sunk) if computer_sunk else "Aucun")

def main():
    """Lance le jeu"""
    app = GameWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
