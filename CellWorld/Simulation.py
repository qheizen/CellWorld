import os
import sys

# Добавляем в sys.path родительскую директорию, чтобы абсолютные импорты типа "CellWorld." работали при запуске изнутри пакета
_this_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_this_dir)  # <- теперь в sys.path окажется ".../CellWorld"
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import pygame
import random
# убрал import copy; теперь клонирование делается через prototype.clone()
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

    def init(self):
        serializer = sr.WorldSerializer()
        self.game_manager = serializer.serialize_world("CellWorld/Situations_preconfig.json")
        self.game_manager.set_simulation_manager(self)

        windows_size = self.game_manager.get_option("size")
        if windows_size and isinstance(windows_size, (list, tuple)) and len(windows_size) >= 2:
            try:
                w, h = int(windows_size[0]), int(windows_size[1])
            except Exception:
                w, h = 800, 600
            self.screen = pygame.display.set_mode((w, h))

        self.clock = pygame.time.Clock()

        try:
            prototype = None
            if hasattr(self.game_manager, "_cell_types") and self.game_manager._cell_types:
                prototype = self.game_manager._cell_types[0]

            if prototype is None:
                print("No cell prototype available to spawn (game_manager._cell_types is empty).")
            else:
                new_cells = []
                for i in range(15):
                    self.spawn(prototype)
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
    sim.init()
    sim.run()
