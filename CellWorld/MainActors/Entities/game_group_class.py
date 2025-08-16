from pygame import Vector2
from CellWorld.MainActors.Entities.game_actor_class import GameActor
from CellWorld.MainActors.Entities.game_cell_class import CellType
import random
import hashlib

class CellGroup(GameActor):
    
    def __init__(self):
        self.name = "non-init-value"
        self.cells_names: list = []
        self.cell_count: int = 0
        self.spawn_radius: float = 0.
        
    def init(self, transfer_object: dict):
        options_tags: dict = {
            "credentials": self.__safe_init_credentials,
            "group": self.__safe_init_group,
        }
        
        for tag, values in transfer_object:
            if init_func := options_tags[tag]:
                init_func(values)
    
    def __safe_init_group(self, values):
        link_dict = {
            "cells_type_names": "cells_names",
            "cell_count": "cell_count",
            "spawn_radius": "spawn_radius"
        }
        for key, value in values:
            if attr := link_dict[key]:
                setattr(self, attr, value)
        
    def __safe_init_credentials(self, credentials):
        if not (name := credentials.get("name")):
            name = hashlib.md5(str(random.random()).encode()).hexdigest()
            credentials.pop("name")
        self.name = name
        self.set_position(credentials.get("start_pos", Vector2(0,0)))
    
    def initiate_spawn(self, global_manager):
        super().initiate_spawn(global_manager)
        
    def initiate_spawner_ability(self):
        cells_to_spawn = []
        for i in range(self.cell_count):
            random_cell: CellType = self.get_cell_with_name(random.choice(self.cells_names)).copy()
            random_cell.set_position(self.random_vector(0, self.spawn_radius))
            cells_to_spawn.append(random_cell)
        
        self._world_manager.spawn(cells_to_spawn: list)