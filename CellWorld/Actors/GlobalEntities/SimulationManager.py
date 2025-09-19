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
from CellWorld.Actors.GlobalEntities.SaverManager import SaveManager
from CellWorld.Actors.GUI.DebugConsole import DebugConsoleObject
import CellWorld.Tools.Logger.loggers as lg

_logger = lg.get_module_logger("GameManager")

class Simulation:
    
    def __init__(self):
        self._game_manager = None
        pygame.init()
        self._screen_layer = None
        self._clock = None
        
        self._event_manager = None
        self._console_manager = None
        self._actual_entities_on_board = []
        self._gui = None
        
        self._windows = []
        
        self.control_cell = None
        self.is_change_cell = False
        
        self.pointer_is_busy: bool = False
        
        self.cell_type_name = None
        self.is_window_spawn: bool = False
        
    def initialize_game(self, path: str):
        serializer = sr.WorldSerializer()
        self.game_manager = serializer.serialize_world(path)
        self.game_manager.set_simulation_manager(self)
        self.save_manager = SaveManager(path)
        self._gui = GUIManager()
        
        windows_size = self.game_manager.get_option("window_size")
        self._console_manager = DebugConsoleObject((10, windows_size[1] - 75), (300, 100), const.COLORS["blue"], 15,2)
        if windows_size and isinstance(windows_size, (list, tuple)):
            try:
                w, h = int(windows_size[0]), int(windows_size[1])
            except Exception:
                w, h = 800, 600
            self._event_manager = EventManager(self.game_manager)
            self._screen_layer = pygame.display.set_mode((w, h))
        self._clock = pygame.time.Clock()
        self._console_manager.console_print("Info - Init -> Main window initialized")
    
    def spawn_to_world(self, entities):
        if isinstance(entities, Actor):
            try:
                actor = entities.clone()
                actor.init_spawn(self.game_manager)
                self._console_manager.console_print(f"Info - Trying to spawn entity. (name: {actor._name}), (pos: {actor._vec_position}))")
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
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.spawn_cell_to_world_from_mouse()
                    
                self._gui.handle_event(event)
                
            if not self.is_change_cell and self.control_cell:
                self.control_cell.control(pygame.key.get_pressed())
            
            self._gui.update(1/60)  
                  
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
                    
            if self.is_change_cell:
                self.draw_from_mouse_to_cell(self._screen_layer, self.control_cell)
            
            
            if self.game_manager.get_option("debug_draw"):
                self._console_manager.draw(self._screen_layer)       
                self.draw_debug_info(self._screen_layer)
                
            self._gui.draw(self._screen_layer)
            pygame.display.flip()
            self._clock.tick(self.game_manager.get_option("fps") or 60)
        pygame.quit()
            
    def initialize_spawn(self):
        pass
    
    def initialize_gui(self):
        self._gui = sit.main_interface(self._gui, self.save_manager, self.game_manager, self, self._console_manager)
        return
            
    def draw_debug_info(self, screen):
        text_to_draw = f"FPS: {self._clock.get_fps()}"
        static.draw_text_table(screen, text_to_draw, 0, 0, const.COLORS["gray"])
        
    def draw_from_mouse_to_cell(self, surface, cell):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        if cell and cell in self._actual_entities_on_board:
            pygame.draw.aaline(surface, const.COLORS["white"], (mouse_x, mouse_y), cell._vec_position, 2)
            
            pygame.draw.circle(
                surface, const.COLORS["white"],
                (int(cell._vec_position.x), int(cell._vec_position.y)),
                cell._size + 10, 2
            )
        
    def change_control_cell(self, shift_idx:int):
        self._console_manager.console_print(f"Info - Change selected cell")
        if not self.is_change_cell:
            return
        
        if not self.control_cell and self._actual_entities_on_board:
            self.control_cell = self._actual_entities_on_board[0]
            return
        
        actual_idx = self._actual_entities_on_board.index(self.control_cell)
        
        if shift_idx > 0:
            if actual_idx != len(self._actual_entities_on_board):
                self.control_cell = self._actual_entities_on_board[actual_idx+1]
        elif shift_idx < 0:
            if actual_idx != len(self._actual_entities_on_board):
                self.control_cell = self._actual_entities_on_board[actual_idx-1]
    
    def open_control_cell_tab(self):
        self._console_manager.console_print(f"Info - Cell control window was opened")
        self.is_change_cell = True
        
    def select_current_cell(self):
        if not self.control_cell:
            self._console_manager.console_print(f"Warning - Cell is not selected")
            _logger.warning("Cell is not selected")
        self._console_manager.console_print(f"Info - Cell was selected")
        self.is_change_cell = False    
    
    def spawn_cell_to_world_from_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.pointer_is_busy and self.is_window_spawn and (cell_type := self.game_manager.get_cell_prototype_with_name(self.cell_type_name)):
            cell = cell_type.clone()
            cell.set_position((mouse_x, mouse_y))
            self.spawn_to_world(cell)
        elif self.pointer_is_busy and self.is_window_spawn:
            self._console_manager.console_print(f"Error - Cant spawn cell. (name: {self.cell_type_name}). Usable types names - {self.game_manager.get_cell_types_names()} ")