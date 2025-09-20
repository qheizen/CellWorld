import CellWorld.Constants.Constants as const
import CellWorld.Constants.InGameConst as gconst
import CellWorld.Tools.StaticLib as static
from pygame import Vector2
import pygame

 
class Actor:
    
    def __init__(self):
        self._name: str = static.get_random_hash()
        self._color: tuple = const.TEMPLATE_COL
        self._size: int = const.TEMPLATE_SIZE
        self._draw_text_table: bool = False
        self._draw_lines: bool = False
        
        self._object_state: str = gconst.TEMPLATE_STATE
        self._vec_position = Vector2(0, 0)
        self._vec_velocity = Vector2(0, 0)
        
        self._world_manager = None
        self._local_timer = 0.
        
    
    def draw(self, surface):
        pygame.draw.circle(
            surface, self._color,
            (int(self._vec_position.x), int(self._vec_position.y)),
            self._size
        )
        
        
    def set_position(self, new_pos: Vector2):
        self._vec_position = static.convert_to_vec(new_pos)
        
        
    def set_velocity(self, new_vel: Vector2):
        self._vec_velocity = static.convert_to_vec(new_vel)
        
        
    def add_velocity(self, add_vel: Vector2):
        self._vec_velocity += static.convert_to_vec(add_vel)
        
        
    def add_position(self, add_pos: Vector2):
        self._vec_position += static.convert_to_vec(add_pos)
        
        
    def trigger_self_action(self, name: str, args: list):
        if self._world_manager:
            self._world_manager.trigger_action(name, args, self)
    
    
    def serialize_class(self, transfer_object: dict):
        pass
    

    def get_cell_prototype_with_name(self, name):
        if self._world_manager:
            return self._world_manager.get_cell_prototype_with_name(name)
        return None
    
    
    def init_spawn(self, global_manager, spawn_cords = None):
        self._world_manager = global_manager
        
        if spawn_cords:
            self.set_position(static.convert_to_vec(spawn_cords))
            
        if self._vec_position == Vector2(0, 0):
            self.set_position(self._get_random_in_screen_vector())
            
    
    def init_death(self):
        self._object_state = gconst.OBJECT_STATES["dead"]
        self._vec_velocity *= 0.3 
        
        
    def init_clearing(self):
        self._object_state = gconst.OBJECT_STATES["disposed"]
    
    
    def init_spawner_ability(self):
        pass
    
    
    def console_print(self):
        pass
    
    
    def update(self, other_cells: list):
        pass
   
   
    def clone(self) -> "Actor":
        pass
        
        
    def _spawn_to_world(self, cells: list):
        if self._world_manager:
            self._world_manager.spawn_to_world(cells)
        
        
    def _serialize_attr_from_dict(self, link_dict: dict, values_dict: dict) -> None:
        for key, value in values_dict.items():
            attribute = link_dict.get(key)
            if attribute is not None:
                setattr(self, attribute, value)
        return 
                
                
    def _get_option(self, option: str):
        if self._world_manager:
            return self._world_manager.get_option(option)
        return None
    
    
    def _get_fps(self):
        return self._get_option("fps")
        
        
    def _get_random_in_screen_vector(self) -> Vector2:
        if self._world_manager:
            win_size = self._get_option("window_size")
            return static.random_vector(0, win_size)
        return Vector2(0, 0)
    
    def activate_event(self, event_type:str, args: list, object = None):
        if self._world_manager:
            self._world_manager.trigger_action(event_type, args, object)
            
    def control(self, keys):
        speed = 30/60
        if keys[pygame.K_w]:
            self.add_velocity((0, -speed))
        if keys[pygame.K_s]:
            self.add_velocity((0, speed))
        if keys[pygame.K_a]:
            self.add_velocity((-speed, 0))
        if keys[pygame.K_d]:
            self.add_velocity((speed, 0))
        
    