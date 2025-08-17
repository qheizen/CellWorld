import hashlib
import random
import CellWorld.Tools.Logger.loggers as lg
import CellWorld.Constant.constants as const
from CellWorld.MainActors.Entities.game_actor_class import GameActor

_logger = lg.get_module_logger("EVENT")

class Event(GameActor):

    def __init__(self):
        super().__init__()
        self.name = const.NON_VALUE
        self.description = const.NON_VALUE
        self.event_type = const.NON_VALUE
        self.args = []
        self.activation_time = 0.0

    def init(self, transfer_object: dict):
        options_tags = {
            "credentials": self.__safe_init_credentials
        }

        for tag, values in transfer_object.items():
            init_func = options_tags.get(tag)
            if init_func:
                init_func(values)

        self.args = transfer_object.get("args", [])
        self.activation_time = transfer_object.get("activation_time", 0.0)

    def __safe_init_credentials(self, credentials: dict):
        name = credentials.pop("name", None)
        if not name:
            name = hashlib.md5(str(random.random()).encode()).hexdigest()
        self.name = name

        link_dict = {
            "description": "description",
            "event_type": "event_type"
        }

        for key, value in credentials.items():
            attr = link_dict.get(key)
            if attr:
                setattr(self, attr, value)

    def activate_outgoing(self, event_type: str, args: list):
        event_dict = {
            "spawn_entity_to_scene": self._spawn_to_scene
        }
        func = event_dict.get(event_type)
        if func:
            func(args)

    def activate_incoming(self):
        current_time = self.get_global_timer()
        if current_time is not None and current_time > self.activation_time:
            self.activation_time = 0.0
            self.activate_outgoing(self.event_type, self.args)

    def initiate_spawn(self, global_manager):
        super().initiate_spawn(global_manager)

    def _spawn_to_scene(self, args):
        self.spawn_to_world(args)
