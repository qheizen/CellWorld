import CellWorld.Tools.Logger.loggers as lg
import CellWorld.Constant.constants as const
from CellWorld.MainActors.Entities.game_actor_class import GameActor
import hashlib
import random


class Event(GameActor):
    
    def __init__(self):
        self.name = const.NON_VALUE
        self.description = const.NON_VALUE
        self.event_type = const.NON_VALUE
        
        self.args = []
        self.activation_time = 0.
        
    def init(self, transfer_object: dict):
        options_tags: dict = {
            "credentials": self.__safe_init_credentials,
        }
        
        for tag, values in transfer_object:
            if init_func := options_tags[tag]:
                init_func(values)
                
        self.args = transfer_object.get("args", [])
        self.activation_time = transfer_object.get("activation_time", [])
    
    def __safe_init_credentials(self, credentials: dict):
        if not (name := credentials.get("name")):
            name = hashlib.md5(str(random.random()).encode()).hexdigest()
            credentials.pop("name")
        self.name = name
        
        link_dict = {
            "description": "description",
            "event_type": "event_type",
        }
        
        for key, value in credentials:
            if attr := link_dict[key]:
                setattr(self, attr, value)
        
    
    def activate_outcoming(self, type: str, args: list):
        event_dict = {
            "spawn_entity_to_scene": self._spawn_to_scene
        }
        if func := event_dict[type]:
            func(args)
    
    def activate_incoming(self):
        if self.get_global_timer() > self.activation_time:
            self.activation_time = 0
            self.activate_outcoming(self.event_type, self.args)
    
    def initiate_spawn(self, global_manager):
        return super().initiate_spawn(global_manager)
    
    def _spawn_to_scene(self, args): 
        self.spawn_to_world(args)
        
        