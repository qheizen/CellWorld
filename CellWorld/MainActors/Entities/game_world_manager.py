import CellWorld.Tools.Logger.loggers as lg
from CellWorld.MainActors.Entities.game_cell_class import CellType

_logger = lg.get_module_logger("WorldManager")

class WorldManager:

    def __init__(self):
        self._global_options = {}
        self._cell_types = []
        self._cell_groups = []
        self._game_events = []
         
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
            "constant_g": "constant_g"
        }
        for key, value in physical:
            if attr := link_dict[key]:
                self._global_options[attr] = value
    
    def add_cell_type(self, cell_type_data: dict):
        if not cell_type_data:
            _logger.error("Was received an empty cell_type")
            return
        cell: CellType = CellType()
        cell.init(cell_type_data)
        if not cell in self._cell_types:
            self._cell_types.append(cell)
        
    def add_cell_group(self, cell_group: dict):
        