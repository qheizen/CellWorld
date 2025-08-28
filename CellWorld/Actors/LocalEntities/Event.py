import CellWorld.Constants.Constants as const
import CellWorld.Constants.InGameConst as gconst
import CellWorld.Tools.StaticLib as static
import CellWorld.Tools.Logger.loggers as lg
import CellWorld.Actors.LocalEntities.ActorClass as actor
import CellWorld.Actors.LocalEntities.Cell as cell
import random
import copy
from pygame import Vector2

_logger = lg.get_module_logger("CellGroup")

class Event(actor.Actor):
    
    def __init__(self) -> None:
        super().__init__()
        self._description = const.TEMPLATE_STR
        self._event_type = const.TEMPLATE_STR
        self._args = []
        
        self._status: bool = False
        self._activation_time: float = 0.0
        
    def serialize_class(self, transfer_object: dict):
        credentials_link: dict = {
            "name": "_name",
            "description": "_description",
        }
        
        event_link: dict = {
            "event_type": "_event_type",
            "args": "_args"
        }
        
        options_link: dict = {
            "credentials": credentials_link,
            "event_type": event_link
        }
        
        for key, values_dict in transfer_object.items():
            link_dict = options_link.get(key)
            if link_dict:
                self._serialize_attr_from_dict(link_dict, values_dict)
                continue
            _logger.warning(f"Serialization - cant find tag: {key}")
        _logger.info(f"Serialization - event was created with name: {self._name}")
        
    def init_spawn(self, global_manager, spawn_cords=None):
        super().init_spawn(global_manager, spawn_cords)
        self._object_state = gconst.OBJECT_STATES["dormant"]
        
    def update(self, other_cells):
        self._local_timer += 1 / self._get_fps()
        
        if self._activation_time <= self._local_timer and not self._status:
            _logger.info(f"Event {self._name} activated")
            self.activate_event(self._event_type, self._args, other_cells)
        self._local_timer += 1 / self._get_fps()
    
    def console_print(self):
        _logger.warning(
            f"TYPE: {self._name}, EVENT: {self._event_type}",
            f"DESC: {self._description}"
            f"VEL: {self._vec_velocity}, POS: {self._vec_position}"
        )

    def clone(self):
        new = Event()
        new._name = self._name
        new._activation_time = self._activation_time
        new._description = self._description
        new._event_type = self._event_type
        new._args = copy.deepcopy(self._args)
        return new