import os
import sys

_this_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_this_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import pygame
import random
import CellWorld.SerializableTools.world_serializer as sr
from CellWorld.MainActors.Entities.game_cell_class import CellType
from CellWorld.MainActors.Entities.game_group_class import CellGroup
from CellWorld.MainActors.Entities.game_actor_class import GameActor

class Simulation:

    def __init__(self):
        self.game_manager = None
        pygame.init()
        self.screen = None
        self.clock = None
        self.actual_cells_on_board = []

    def init_game_window(self):
        serializer = sr.WorldSerializer()
        self.game_manager = serializer.serialize_world("CellWorld/ROFL.json")
        self.game_manager.set_simulation_manager(self)

        windows_size = self.game_manager.get_option("size")
        if windows_size and isinstance(windows_size, (list, tuple)) and len(windows_size) >= 2:
            try:
                w, h = int(windows_size[0]), int(windows_size[1])
            except Exception:
                w, h = 800, 600
            self.screen = pygame.display.set_mode((w, h))
        self.clock = pygame.time.Clock()


    def init_spawn(self):
        try:
            namev = self.game_manager.get_cell_type("neutral")
            namev1 = self.game_manager.get_cell_type("agressor")
            namev2 = self.game_manager.get_cell_type("swarm")
            
            if namev is None:
                print("No cell prototype available to spawn (game_manager._cell_types is empty).")
            else:
                for i in range(80):
                    self.spawn(random.choice(self.game_manager._cell_types))
        except Exception as e:
            print(f"Error while spawning initial cells: {e}")
            
            
    def getClock(self):
        return pygame.time.get_ticks()

    def spawn(self, args):
        if isinstance(args, GameActor):
            try:
                new_cell = args.clone()
                new_cell.initiate_spawn(self.game_manager)
                self.actual_cells_on_board.append(new_cell)
            except Exception as e:
                print(f"Failed to spawn single GameActor: {e}")
        elif isinstance(args, (list, tuple)):
            for item in args:
                if isinstance(item, GameActor):
                    try:
                        new_cell = item.clone()
                        new_cell.initiate_spawn(self.game_manager)
                        self.actual_cells_on_board.append(new_cell)
                    except Exception as e:
                        print(f"Failed to spawn GameActor in list: {e}")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for cell in list(self.actual_cells_on_board):
                try:
                    cell.update(self.actual_cells_on_board)
                    if cell._object_state == "agent_to_del":
                        self.actual_cells_on_board.remove(cell)
                except Exception as e:
                    print(f"Error updating cell {cell}: {e}")

            self.screen.fill(self.game_manager.get_option("bgcolor") or (0, 0, 0))
            for cell in self.actual_cells_on_board:
                try:
                    cell.draw(self.screen)
                except Exception as e:
                    print(f"Error drawing cell {cell}: {e}")

            pygame.display.flip()
            self.clock.tick(self.game_manager.get_option("fps") or 60)
        pygame.quit()


if __name__ == "__main__":
    sim = Simulation()
    sim.init_game_window()
    sim.init_spawn()
    sim.run()
