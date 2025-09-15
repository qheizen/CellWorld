import pygame
import CellWorld.Tools.StaticLib as static
import CellWorld.Constants.Constants as const
import CellWorld.SerializableTools.Serializer as sr
from CellWorld.Actors.LocalEntities.Cell import Cell
from CellWorld.Actors.LocalEntities.Group import Group
from CellWorld.Actors.LocalEntities.Event import Event
from CellWorld.Actors.LocalEntities.ActorClass import Actor
from CellWorld.Actors.GlobalEntities.EventManager import EventManager
import CellWorld.InterfaceTemplates.SituationInputTemplate as sit 
from CellWorld.Actors.GlobalEntities.GuiManager import GUIManager
import CellWorld.Tools.Logger.loggers as lg

_logger = lg.get_module_logger("GameManager")

class Simulation:
    
    def __init__(self):
        self._game_manager = None
        pygame.init()
        self._screen_layer = None
        self._clock = None
        
        self._event_manager = None
        self._actual_entities_on_board = []
        self._gui = None
        
        self._windows = []
        
    def initialize_game(self, path: str):
        serializer = sr.WorldSerializer()
        self.game_manager = serializer.serialize_world(path)
        self.game_manager.set_simulation_manager(self)
        self._gui = GUIManager()
        
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
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                
                self._gui.handle_event(event)
                    
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
                    
            self._gui.draw(self._screen_layer)
            
            if self.game_manager.get_option("debug_draw"):
                self.draw_debug_info(self._screen_layer)
            pygame.display.flip()
            self._clock.tick(self.game_manager.get_option("fps") or 60)
        pygame.quit()
            
    def initialize_spawn(self):
        pass
    
    def initialize_gui(self):
        self._gui = sit.create_window(self._gui)
        return
            
    def draw_debug_info(self, screen):
        text_to_draw = f"FPS: {self._clock.get_fps()}"
        static.draw_text_table(screen, text_to_draw, 0, 0, const.COLORS["gray"])