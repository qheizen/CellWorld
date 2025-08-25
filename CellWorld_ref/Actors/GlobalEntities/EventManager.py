import CellWorld_ref.Constants.Constants as const
import CellWorld_ref.Actors.LocalEntities.ActorClass as actor
import CellWorld_ref.Actors.LocalEntities.Cell as cell
import CellWorld_ref.Actors.LocalEntities.Group as group
import CellWorld_ref.Actors.LocalEntities.Event as event
import CellWorld_ref.Tools.Logger.loggers as lg

_logger = lg.get_module_logger("GameManager")

class EventManager:
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
    
    def activate_event(self, event_type, args, object):
        pass
    
    