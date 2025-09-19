import CellWorld.Constants.Constants as const
import CellWorld.Actors.LocalEntities.ActorClass as actor
import CellWorld.Actors.LocalEntities.Cell as cell
import CellWorld.Actors.LocalEntities.Group as group
import CellWorld.Actors.LocalEntities.Event as event
import CellWorld.Tools.Logger.loggers as lg

_logger = lg.get_module_logger("GameManager")

class WorldManager:
    
    def __init__(self):
        self._global_options = {
            "window_size": const.WINSIZE,
            "bg_color": const.TEMPLATE_COL,
            "board_strength": 0.0,
            "board_margin": 0,
            "debug_draw": False,
            "fps": const.FPS,
            "constants": {
                "g": 9.8
            }
        }
        self._cell_types: list = []
        self._group_types: list = []
        self._events_types: list = []
        
        self._simulation_manager = None
        
    def set_simulation_manager(self, simulator):
        self._simulation_manager = simulator
        
    def serialize_class(self, transfer_object: dict):
        credentials_link: dict = {
            "fps_lock": "fps",
            "window_size": "window_size",
            "background_color": "bg_color",
            "debug_draw": "debug_draw"
        }
        
        physical_link: dict = {
            "wall_margin": "board_margin",
            "wall_strength": "board_strength",
            "constants": "constants",
        }
        
        options_link: dict = {
            "credentials": credentials_link,
            "physical": physical_link
        }
        
        for key, values_dict in transfer_object.items():
            link_dict = options_link.get(key)
            if link_dict:
                self._serialize_attr_from_dict(link_dict, values_dict)
                continue
            _logger.warning(f"Serialization - cant find tag: {key}")
        _logger.info(f"Serialization - world serialized")
    
    def _serialize_attr_from_dict(self, link_dict: dict, values_dict: dict):
        for key, value in values_dict.items():
            attribute = link_dict.get(key)
            if attribute is not None:
                self._global_options[attribute] = value
        return
    
    def get_option(self, option: str):
        return self._global_options.get(option, None)
    
    def trigger_action(self, event_type: str, args: list, object = None):
        if self._simulation_manager:
            self._simulation_manager.activate_event(event_type, args, object)
        
    def add_cell_type(self, cell_type_data: dict):
        if not cell_type_data:
            _logger.error("Received an empty cell_type")
            return
        new_cell = cell.Cell()
        new_cell.serialize_class(cell_type_data)
        if new_cell not in self._cell_types:
            self._cell_types.append(new_cell)
            
    def add_group_type(self, cell_group_data: dict):
        if not cell_group_data:
            _logger.error("Received an empty cell_group")
            return
        new_group = group.Group()
        new_group.serialize_class(cell_group_data)
        if new_group not in self._group_types:
            self._group_types.append(new_group)
            
    def add_event_type(self, cell_event_data: dict):
        if not cell_event_data:
            _logger.error("Received an empty event")
        new_event = event.Event()
        new_event.serialize_class(cell_event_data)
        if new_event not in self._events_types:
            self._events_types.append(new_event)
            
    def spawn_to_world(self, cells: list):
        if self._simulation_manager:
            self._simulation_manager.spawn_to_world(cells)
        
    def get_cell_prototype_with_name(self, name: str):
        for item in self._cell_types:
            if item._name == name:
                _logger.info(f"Trying to take cell_type example (name: {name})")
                return item
        return None
    
    def get_group_prototype_with_name(self, name: str):
        for item in self._group_types:
            if item._name == name:
                _logger.info(f"Trying to take cell_group example (name: {name})")
                return item
        return None
    
    def get_event_prototype_with_name(self, name: str):
        for item in self._events_types:
            if item._name == name:
                _logger.info(f"Trying to take cell_group example (name: {name})")
                return item
        return None
    
    
    def on_button_click(self, *args):
        print("GameManager: Button clicked with args:", args)

    def on_text_submit(self, text: str):
        print("GameManager: Text submitted:", text)

    def on_form_submit(self, form_data):
        print("GameManager: Form submitted:", form_data)
        
    def get_cell_types_names(self):
        result: str = ""
        for type in self._cell_types:
            result += f" {type._name}"
        return result
    
    def set_attribute(self, name, value):
        self._global_options[name] = value
        
    def set_special_attribute(self, name, value):
        self._global_options["constants"][name] = value