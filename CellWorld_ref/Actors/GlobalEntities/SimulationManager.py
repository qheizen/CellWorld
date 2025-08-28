
    
import pygame
import CellWorld_ref.SerializableTools.Serializer as sr
from CellWorld_ref.Actors.LocalEntities.Cell import Cell
from CellWorld_ref.Actors.LocalEntities.Group import Group
from CellWorld_ref.Actors.LocalEntities.Event import Event
from CellWorld_ref.Actors.LocalEntities.ActorClass import Actor
from CellWorld_ref.Actors.GlobalEntities.EventManager import EventManager
import CellWorld_ref.Tools.Logger.loggers as lg

_logger = lg.get_module_logger("GameManager")

class Simulation:
    
    def __init__(self):
        self._game_manager = None
        pygame.init()
        self._screen_layer = None
        self._clock = None
        
        self._event_manager = None
        self._actual_entities_on_board = []
        
    def initialize_game(self, path: str):
        serializer = sr.WorldSerializer()
        self.game_manager = serializer.serialize_world(path)
        self.game_manager.set_simulation_manager(self)
        
        windows_size = self.game_manager.get_option("window_size")
        if windows_size and isinstance(windows_size, (list, tuple)):
            try:
                w, h = int(windows_size[0]), int(windows_size[1])
            except Exception:
                w, h = 800, 600
            self._event_manager = EventManager(self.game_manager)
            self._screen_layer = pygame.display.set_mode((w, h))
        self._clock = pygame.time.Clock()
    
    def spawn_to_world(self, entities):
        if isinstance(entities, Actor):
            try:
                actor = entities.clone()
                actor.init_spawn(self.game_manager)
                self._actual_entities_on_board.append(actor)
            except Exception as e:
                _logger.critical(f"Error while spawning initial cells: {e}")
        else:
            for actor in entities:
                self.spawn_to_world(actor)
    
    def activate_event(self, event_type, args, object):
        self._event_manager.activate_event(event_type, args, object)
        
    def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            for actor in list(self._actual_entities_on_board):
                try:
                    actor.update(self._actual_entities_on_board)
                    if actor._object_state == "disposed":
                        self._actual_entities_on_board.remove(actor)
                except Exception as e:
                    _logger.critical(f"Error updating actor {actor}, {e}")
                
            self._screen_layer.fill(self.game_manager.get_option("bg_color"))
            for actor in self._actual_entities_on_board:
                try:
                    actor.draw(self._screen_layer)
                except Exception as e:
                    _logger.critical(f"Error drawing cell {actor}: {e}")
            pygame.display.flip()
            self._clock.tick(self.game_manager.get_option("fps") or 60)
        
        pygame.quit()
            
    def initialize_spawn(self):
        try:
            planet = self.game_manager.get_cell_prototype_with_name("namev")
            for i in range(20):
                self.spawn_to_world(planet)
        except Exception as e:
            print(f"Error while spawning initial cells: {e}")