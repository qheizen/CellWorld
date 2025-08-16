from pygame import Vector2
import pygame
from CellWorld.MainActors.Entities.game_world_manager import WorldManager
import CellWorld.Constant.constants as const
import random

class GameActor:
    
    def __init__(self):
        self._vector_position: Vector2 = Vector2(0, 0)
        self._vector_velocity: Vector2 = Vector2(0, 0)
        self._world_manager: WorldManager = None
        self._object_state = "non_initiated"
        
    def init(self):
        pass
        
    def set_position(self, new_pos: Vector2):
        self._vector_position = self.safe_vector2_convert(new_pos)
            
    def set_velocity(self, new_vel: Vector2):
        self._vector_velocity = self.safe_vector2_convert(new_vel)
            
    def add_velocity(self, added_vel:Vector2):
        self._vector_velocity += self.safe_vector2_convert(added_vel)
    
    def add_position(self, added_pos:Vector2):
        self._vector_position += self.safe_vector2_convert(added_pos)
    
    def safe_vector2_convert(self, value) -> Vector2:
        if value is None:
            return Vector2(0, 0)
        
        if isinstance(value, Vector2):
            return value

        try:
            if isinstance(value, (int, float)):
                return Vector2(value, value)
            return Vector2(value)
        except (TypeError, ValueError):
            return Vector2(0, 0)
    
    def random_vector(self, start = const.RAN_START, final = const.RAN_END) -> Vector2:
        start_point = self.safe_vector2_convert(start)
        final_point = self.safe_vector2_convert(final)
        return Vector2(random.uniform(start_point.x, final_point.x), 
                       random.uniform(start_point.y, final_point.y))
    
    def get_random_in_screen_vector(self) -> Vector2:
        if self._world_manager:
            size = self._world_manager.get_option("size", "list")
            return self.random_vector([0, size[0]], [0, size[1]])
        
    def get_fps(self):
        return self._world_manager.get_option("fps", "float")
    
    def get_global_timer(self):
        return self._world_manager.get_actual_clock()
    
    def get_global_margin(self):
        return self._world_manager.get_option("border_margin", "float")

    def get_global_strenth(self):
        return self._world_manager.get_option("wall_strength", "float")
    
    def get_constants(self):
        return self._world_manager.get_option("constants", "dict")
    
    def trigger_action(self, name, args):
        self._world_manager.trigger_action(name, args, self)
        
    def initiate_spawn(self, global_manager):
        self._object_state = "alive"
        self._world_manager = global_manager
        if self._vector_position == Vector2(0,0):
            self.set_position(self.random_vector())
        return
    
    def initiate_death(self):
        self._object_state = "death"
        self.set_velocity(0)
        
    def draw(self, surface):
        pygame.draw.circle(surface, const.MISSED_COLOR, (int(self._vector_position.x), int(self._vector_position.y)), const.MISSED_SIZE)
    
    def get_cell_with_name(self, name: str):
        return self._world_manager.get_cell_type(name)
    
    def initiate_update(self, cells):
        pass
    
    def initiate_spawner_ability(self):
        pass
    
    def spawn_to_world(self, cells: list):
        self._world_manager.spawn(cells)
        
    def console_print(self):
        pass