import CellWorld.Tools.Logger.loggers as lg
from CellWorld.MainActors.Entities.game_cell_class import CellType
from CellWorld.MainActors.Entities.game_group_class import CellGroup
from CellWorld.MainActors.Entities.game_actor_class import GameActor
import CellWorld.Constant.constants as const

_logger = lg.get_module_logger("WorldManager")

class WorldManager:

    def __init__(self):
        self._global_options = {
            "window_size": const.WINDOW_SIZE,
            "fps": const.FPS,
            "bgcolor": const.MISSED_COLOR,
            "border_margin": 0,
            "wall_strength": 0.0,
            "constants": {
                "g": 9.8,
            }
        }
        self._cell_types: list[CellType] = []
        self._cell_groups: list[CellGroup] = []
        self._game_events = []
        
        self._simulation_manager = None
        
        self.actual_cells_on_board = []
        
        
    def set_simulation_manager(self, simulation):
        self._simulation_manager = simulation
         
    def change_world_options(self, transfer_object: dict):
        options_tags: dict = {
            "credentials": self.__safe_init_credentials,
            "physical": self.__safe_init_physic,
        }
        
        for tag, values in transfer_object:
            if init_func := options_tags[tag]:
                init_func(values)

    def __safe_init_credentials(self, credentials):
        link_dict = {
            "fps_lock":"fps",
            "window_size":"window_size",
            "background_color":"bgcolor"
        }
        for key, value in credentials:
            if attr := link_dict[key]:
                self._global_options[attr] = value
        
    def __safe_init_physic(self, physical):
        link_dict = {
            "wall_margin": "border_margin",
            "wall_strength": "wall_strength",
        }
        for key, value in physical:
            if attr := link_dict[key]:
                self._global_options[attr] = value
                
        self._global_options["constants"]["g"] = physical["constant_g"] or 9.8
    
    def add_cell_type(self, cell_type_data: dict):
        if not cell_type_data:
            _logger.error("Was received an empty cell_type")
            return
        cell: CellType = CellType()
        cell.init(cell_type_data)
        if not cell in self._cell_types:
            self._cell_types.append(cell)
        
    def add_cell_group(self, cell_group_data: dict):
        if not cell_group_data:
            _logger.error("Was received an empty cell_group")
            return
        cell_group: CellGroup = CellGroup()
        cell_group.init(cell_group_data)
        if not cell_group in self._cell_groups:
            self._cell_groups.append(cell_group)
            
    def add_event(self, event_data: dict):
        if not event_data:
            _logger.error("Was received an empty event")
            return
        
    def spawn(self, args: list[GameActor]):
        if isinstance(args, GameActor):
            args.initiate_spawn(self)
            self.actual_cells_on_board.append(args)
            
        for item in args:
            item.initiate_spawn(self)
            self.actual_cells_on_board.append(item)
            
    def get_actual_clock(self):
        self._simulation_manager.getClock()
        
    def get_option(self, param: str):
        return self._global_options[param] or None
    
    def get_cell_type(self, param: str):
        for item in self._cell_types:
            if item.name == param:
                return item
    
    