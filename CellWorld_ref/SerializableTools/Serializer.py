from CellWorld_ref.Actors.GlobalEntities.GameManager import WorldManager
from CellWorld_ref.Tools.JsonSituationParser.JsonParser import JsonParser
import CellWorld_ref.Tools.Logger.loggers as lg

_logger = lg.get_module_logger("SERIALIZER")

class WorldSerializer:
    
    def serialize_world(self, path: str) -> WorldManager:
        segment_funcs = {
            "global_options": self.__serialize_global_options,
            "cell_options": self.__serialize_cell_options,
            "cell_groups": self.__serialize_cell_groups,
            "game_events": self.__serialize_game_events
        }
        world_manager = WorldManager()

        json_parser = JsonParser()
        data_from_file:list = json_parser.load_json_from_file(path)

        for key, func in segment_funcs.items():
            segment_data = data_from_file.get(key)
            if segment_data is not None:
                world_manager = func(segment_data, world_manager)
                _logger.info(f"Segment loaded (name: {key})")
            else:
                _logger.critical(f"No data segment (name: {key})")

        _logger.info("World serialized!")
        data_from_file.clear()
        json_parser = None
        return world_manager

    def __serialize_global_options(self, segment: dict, world_manager: WorldManager):
        world_manager.serialize_class(segment)
        return world_manager

    def __serialize_cell_options(self, segment: list, world_manager: WorldManager):
        for cell_type_data in segment:
            world_manager.add_cell_type(cell_type_data)
        return world_manager

    def __serialize_cell_groups(self, segment: list, world_manager: WorldManager):
        for cell_group_data in segment:
            world_manager.add_group_type(cell_group_data)
        return world_manager

    def __serialize_game_events(self, segment: list, world_manager: WorldManager):
        for event_data in segment:
            world_manager.add_event_type(event_data)
        return world_manager
        