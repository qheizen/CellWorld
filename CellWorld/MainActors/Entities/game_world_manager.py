import CellWorld.Tools.Logger.loggers as lg
from CellWorld.MainActors.Entities.game_cell_class import CellType
from CellWorld.MainActors.Entities.game_group_class import CellGroup
from CellWorld.MainActors.Entities.game_actor_class import GameActor
from CellWorld.MainActors.Entities.game_event_class import Event
import CellWorld.Constant.constants as const

_logger = lg.get_module_logger("WorldManager")

class WorldManager:

    def __init__(self):
        self._global_options = {
            "size": const.WINDOW_SIZE,
            "fps": const.FPS,
            "bgcolor": const.MISSED_COLOR,
            "border_margin": 0,
            "wall_strength": 0.0,
            "constants": {
                "g": 9.8
            }
        }
        self._cell_types = []
        self._cell_groups = []
        self._game_events = []
        self._simulation_manager = None

    def set_simulation_manager(self, simulation):
        self._simulation_manager = simulation

    def change_world_options(self, transfer_object: dict):
        options_tags = {
            "credentials": self.__safe_init_credentials,
            "physical": self.__safe_init_physic
        }

        for tag, values in transfer_object.items():
            init_func = options_tags.get(tag)
            if init_func:
                init_func(values)
        return self

    def __safe_init_credentials(self, credentials: dict):
        link_dict = {
            "fps_lock": "fps",
            "window_size": "size",
            "background_color": "bgcolor"
        }
        for key, value in credentials.items():
            attr = link_dict.get(key)
            if attr:
                self._global_options[attr] = value

    def __safe_init_physic(self, physical: dict):
        link_dict = {
            "wall_margin": "border_margin",
            "wall_strength": "wall_strength"
        }
        for key, value in physical.items():
            attr = link_dict.get(key)
            if attr:
                self._global_options[attr] = value
        self._global_options["constants"]["g"] = physical.get("constant_g", 1)

    def add_cell_type(self, cell_type_data: dict):
        if not cell_type_data:
            _logger.error("Received an empty cell_type")
            return
        cell = CellType()
        cell.init(cell_type_data)
        if cell not in self._cell_types:
            self._cell_types.append(cell)

    def add_cell_group(self, cell_group_data: dict):
        if not cell_group_data:
            _logger.error("Received an empty cell_group")
            return
        cell_group = CellGroup()
        cell_group.init(cell_group_data)
        if cell_group not in self._cell_groups:
            self._cell_groups.append(cell_group)

    def add_event(self, event_data: dict):
        if not event_data:
            _logger.error("Received an empty event")
            return
        event = Event()
        event.init(event_data)
        self._game_events.append(event)

    def spawn(self, args):
        self._simulation_manager.spawn(args)

    def get_actual_clock(self):
        if self._simulation_manager:
            return self._simulation_manager.getClock()
        return None

    def get_option(self, param: str):
        return self._global_options.get(param)

    def get_cell_type(self, name: str):
        for item in self._cell_types:
            if item.name == name:
                return item
        return None
