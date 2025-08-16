import CellWorld.Tools.Logger.loggers as lg
from CellWorld.MainActors.Entities.game_cell_class import CellType

_logger = lg.get_module_logger("PARSER")

class WorldManager:

    def __init__(self):
        self._cell_types = []
        self._game_events = []
        self._groups = []

        self._global_options = {}
        
        