import hashlib
import random
import copy
from pygame import Vector2
import CellWorld.Constant.constants as const
from CellWorld.Tools.Logger.loggers import get_module_logger
from CellWorld.MainActors.Entities.game_actor_class import GameActor
from CellWorld.MainActors.Entities.game_cell_class import CellType

_logger = get_module_logger("CELLGROUP")

class CellGroup(GameActor):

    def __init__(self):
        super().__init__()
        self.name = const.NON_VALUE
        self.cells_names = []
        self.cell_count = 0
        self.spawn_radius = 0.0

    def init(self, transfer_object: dict):
        options_tags = {
            "credentials": self.__safe_init_credentials,
            "group": self.__safe_init_group
        }

        for tag, values in transfer_object.items():
            init_func = options_tags.get(tag)
            if init_func:
                init_func(values)

    def __safe_init_group(self, values: dict):
        link_dict = {
            "cells_type_names": "cells_names",
            "cell_count": "cell_count",
            "spawn_radius": "spawn_radius"
        }
        for key, value in values.items():
            attr = link_dict.get(key)
            if attr:
                setattr(self, attr, value)

    def __safe_init_credentials(self, credentials: dict):
        name = credentials.pop("name", None)
        if not name:
            name = hashlib.md5(str(random.random()).encode()).hexdigest()
        self.name = name
        self.set_position(credentials.get("start_pos", Vector2(0, 0)))

    def initiate_spawn(self, global_manager):
        super().initiate_spawn(global_manager)
        self.initiate_spawner_ability()
        self.initiate_death()
        
    def initiate_death(self):
        self._object_state = "agent_to_del"

    def initiate_spawner_ability(self):
        cells_to_spawn = []
        for _ in range(self.cell_count):
            prototype = self.get_cell_with_name(random.choice(self.cells_names))
            if not prototype:
                continue

            new_cell = prototype.clone()                
            random_vector = self.random_vector(-self.spawn_radius, self.spawn_radius)
            new_cell.set_position(self._vector_position + random_vector)
            cells_to_spawn.append(new_cell)
        
        self.spawn_to_world(cells_to_spawn)

        

    def initiate_update(self, cells):
        pass 

    def clone(self):
        new = CellGroup()
        new.name = self.name
        new.cells_names = copy.deepcopy(self.cells_names)
        new.cell_count = self.cell_count
        new.spawn_radius = self.spawn_radius
        return new