import os
import sys

_this_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_this_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import CellWorld.Actors.GlobalEntities.SimulationManager as simuc
from CellWorld.Actors.GlobalEntities.GameManager import WorldManager
import pygame

class GameScene(simuc.Simulation):
    
    def __init__(self):
        super().__init__()
        self.selected_cell = None
        self.gui_manager = None
        
    def initialize_game(self, path):
        super().initialize_game(path)
    
    def initialize_spawn(self):
        try:
            planet = self.game_manager.get_cell_prototype_with_name("namev")
            planet1 = self.game_manager.get_cell_prototype_with_name("namev1")
            for i in range(30):
                self.spawn_to_world(planet)
                self.spawn_to_world(planet1)
        except Exception as e:
            print(f"Error while spawning initial cells: {e}")

sim = GameScene()
sim.initialize_game("CellWorld/Situations_preconfig.json")
sim.initialize_spawn()
sim.initialize_gui()
sim.main()
