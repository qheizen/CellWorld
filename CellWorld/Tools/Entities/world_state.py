import CellWorld.Tools.Logger.loggers as lg

_logger = lg.get_module_logger("PARSER")

class WorldItem:

    def __init__(self, cell_types:list, game_events:list, groups:list, global_options: dict):
        self._cell_types = cell_types
        self._game_events = game_events
        self._groups = groups

        self._global_options = global_options

    def get_cell_type_info(self, name: str) -> dict:
        for cell_type in self._cell_types:
            if str(cell_type["name"]) == str(name):
                return cell_type
        _logger.warning(f"Cant find cell_type with name: {name}")
        return {}

    def get_all_types(self) -> list:
        return self._cell_types or []

    def get_cell_group_info(self, name:str) -> dict:
        for group_type in self._groups:
            if str(group_type["name"]) == str(name):
                return group_type
        _logger.warning(f"Cant find group with name: {name}")
        return {}

    def get_all_type(self) -> list:
        return self._groups or []

    def get_options(self, name: str):
        return self._global_options.get(name, None)

    def get_event_with_name(self, name):
        for event in self._game_events:
            if str(event["name"]) == str(name):
                return event
        _logger.warning(f"Cant find group with name: {name}")
        return {}