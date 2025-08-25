import CellWorld_ref.Constants.Constants as const
import CellWorld_ref.Constants.InGameConst as gconst
import CellWorld_ref.Tools.StaticLib as static
import CellWorld_ref.Tools.Logger.loggers as lg
import CellWorld_ref.Actors.LocalEntities.ActorClass as actor
import CellWorld_ref.Actors.LocalEntities.Cell as cell
import random
import copy
from pygame import Vector2

_logger = lg.get_module_logger("CellGroup")

class Group(actor.Actor):
    
    def __init__(self) -> None:
        super().__init__()
        self._cells_types: list = []
        self._cells_count: int = 0
        self._spawn_radius: float = 0.
        
    def serialize_class(self, transfer_object):
        credentials_link: dict = {
            "name": "_name",
            "color": "_color",
            "size": "_size",
            "draw_text_table": "_draw_text_table",
            "draw_lines": "_draw_lines"
        }
        
        grout_link: dict = {
            "cells_type_names": "_cells_types",
            "cell_count": "_cells_count",
            "spawn_radius": "_spawn_radius"
        }
        
        options_link: dict = {
            "credentials": credentials_link,
            "group": grout_link,
        }
        
        for key, values_dict in transfer_object.items():
            link_dict = options_link.get(key)
            if link_dict:
                self._serialize_attr_from_dict(link_dict, values_dict)
                continue
            _logger.warning(f"Serialization - cant find tag: {key}")
        _logger.info(f"Serialization - group was created with name: {self._name}")
    
    def init_spawn(self, global_manager, spawn_cords=None):
        super().init_spawn(global_manager, spawn_cords)
        self._object_state = gconst.OBJECT_STATES["dormant"]
        self.init_spawner_ability()
        self.init_clearing()
        
    def init_spawner_ability(self):
        for _ in range(self._cells_count):
            random_prototype = random.choice(self._cells_types)
            prototype: cell.Cell = self.get_cell_prototype_with_name(random_prototype)
            if not prototype:
                _logger.warning(f"No cell type with name: {random_prototype}")
                continue
            
            new_cell = prototype.clone()
            random_vector_shift = static.random_vector(-self._spawn_radius, self._spawn_radius)
            new_cell.add_position(random_vector_shift)
            
            self._spawn_to_world(new_cell)
    
    def draw(self, surface):
        if not self._get_option("debug_draw"):
            return
        
        super().draw(surface)
        if self._draw_text_table:
            text_to_draw = f"name: {self._name}\ncell_names: {self._cells_types}\ntimer: {self._local_timer:.2f}"
            static.draw_text_table(surface, text_to_draw, self._vec_position.x, self._vec_position.y, const.COLORS["gray"])
        
    def console_print(self):
        _logger.warning(
            f"TYPE: {self._name}, TYPES: {self._cells_types:.2f}, "
            f"TIMER: {self._local_timer:.2f}, STATUS: {self._object_state},"
            f"VEL: {self._vec_velocity}, POS: {self._vec_position}"
        )
        
    def clone(self):
        new = Group()
        new._name = self._name
        new._cells_types = copy.deepcopy(self._cells_types)
        new._cells_count = self._cells_count
        new._spawn_radius = self._spawn_radius
        return new