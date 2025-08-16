from CellWorld.MainActors.Entities.game_actor_class import GameActor
from CellWorld.MainActors.Entities.game_cell_class import CellType
from CellWorld.MainActors.Entities.game_world_manager import WorldManager
from CellWorld.Tools.JsonSituationParser.json_parser import JsonParser
import CellWorld.Tools.Logger.loggers as lg

_logger = lg.get_module_logger("SERIALIZER")

class WorldSerializer:
    
    def serialize_world(self, path: str) -> WorldManager:
        link_dict = {
            "global_options": self.__serialize_global_options,
            "cell_options": self.__serialize_cell_options,
            "cell_groups": self.__serialize_cell_groups,
            "game_events": self.__serialize_game_events
        }
        result_world_manager: WorldManager = WorldManager()
        
        json_parser: JsonParser = JsonParser()
        data_from_file = json_parser.load_json_from_file(path)
        
        for key, segment_func in link_dict:
            if (segment_data := data_from_file[key]):
                result_world_manager = segment_func(segment_data, result_world_manager)
                continue
            _logger.critical(f"No data segment - {key}")
            
        _logger.critical(f"World serialized!")
    
    def __serialize_global_options(segment: dict, world_manager: WorldManager):
        world_manager.change_world_options(segment)
    
    def __serialize_cell_options(segment: list, world_manager: WorldManager):
        for cell_type in segment:
            world_manager.add_cell_type(cell_type)
    
    def __serialize_cell_groups(segment: list, world_manager: WorldManager):
        for cell_group in segment:
            world_manager.add_cell_group(cell_group)
    
    def __serialize_game_events(segment: list, world_manager: WorldManager):
        for event in segment:
            world_manager.add_event(event)
        