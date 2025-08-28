import os
import sys

_this_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_this_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import CellWorld_ref.Actors.GlobalEntities.SimulationManager as simuc
import pygame


sim = simuc.Simulation()
sim.initialize_game("CellWorld/Situations_preconfig.json")
sim.initialize_spawn()
sim.main()
