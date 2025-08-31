import os
import sys

_this_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_this_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import CellWorld.Actors.GlobalEntities.SimulationManager as simuc

class GameScene(simuc.Simulation):
    
    def __init__(self):
        super().__init__()
        self.selected_cell = None
        self.gui_manager = None
        
    def initialize_game(self, path, gui_manager):
        super().initialize_game(path)
        self.gui_manager = gui_manager
        gui_manager.simulation_manager = self
    
    def initialize_spawn(self):
        try:
            planet = self.game_manager.get_cell_prototype_with_name("namev")
            for i in range(10):
                self.spawn_to_world(planet)
        except Exception as e:
            print(f"Error while spawning initial cells: {e}")

sim = GameScene()
sim.initialize_game("CellWorld/Situations_preconfig.json")
sim.initialize_spawn()
sim.main()
