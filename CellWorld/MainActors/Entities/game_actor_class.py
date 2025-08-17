import pygame
from pygame import Vector2
import random
import CellWorld.Constant.constants as const

class GameActor:
    def __init__(self):
        self._vector_position = Vector2(0, 0)
        self._vector_velocity = Vector2(0, 0)
        self._world_manager = None
        self._object_state = const.NON_VALUE
        self._local_timer = pygame.time.Clock()

    def init(self, transfer_object: dict):
        pass

    def set_position(self, new_pos: Vector2):
        self._vector_position = self.safe_vector2_convert(new_pos)

    def set_velocity(self, new_vel: Vector2):
        self._vector_velocity = self.safe_vector2_convert(new_vel)

    def add_velocity(self, added_vel: Vector2):
        self._vector_velocity += self.safe_vector2_convert(added_vel)

    def add_position(self, added_pos: Vector2):
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

    def random_vector(self, start=const.RAN_START, final=const.RAN_END) -> Vector2:
        start_point = self.safe_vector2_convert(start)
        final_point = self.safe_vector2_convert(final)
        return Vector2(
            random.uniform(start_point.x, final_point.x),
            random.uniform(start_point.y, final_point.y)
        )

    def get_random_in_screen_vector(self) -> Vector2:
        if self._world_manager:
            size = self._world_manager.get_option("size")
            return self.random_vector((0, 0), (size[0], size[1]))
        return Vector2(0, 0)

    def get_fps(self):
        if self._world_manager:
            return self._world_manager.get_option("fps")
        return None

    def get_global_timer(self):
        if self._world_manager:
            return self._world_manager.get_actual_clock()
        return None

    def get_global_margin(self):
        if self._world_manager:
            return self._world_manager.get_option("border_margin")
        return None
    
    def get_global_screen_size(self):
        if self._world_manager:
            return self._world_manager.get_option("size")
        return None

    def get_global_strength(self):
        if self._world_manager:
            return self._world_manager.get_option("wall_strength")
        return None

    def get_constants(self):
        if self._world_manager:
            return self._world_manager.get_option("constants")
        return {}

    def trigger_action(self, name, args):
        if self._world_manager:
            self._world_manager.trigger_action(name, args, self)

    def initiate_spawn(self, global_manager):
        self._object_state = "alive"
        self._world_manager = global_manager
        if self._vector_position == Vector2(0, 0):
            self.set_position(self.get_random_in_screen_vector())

    def initiate_death(self):
        self._object_state = "death"
        self.set_velocity(0)

    def draw(self, surface):
        pygame.draw.circle(
            surface, const.MISSED_COLOR,
            (int(self._vector_position.x), int(self._vector_position.y)),
            const.MISSED_SIZE
        )

    def get_cell_with_name(self, name: str):
        if self._world_manager:
            return self._world_manager.get_cell_type(name)
        return None

    def initiate_update(self, cells):
        pass

    def initiate_spawner_ability(self):
        pass

    def spawn_to_world(self, cells: list):
        if self._world_manager:
            self._world_manager.spawn(cells)

    def console_print(self):
        print(f"ACTOR - pos: {self._vector_position}, vel: {self._vector_velocity}")

    def update(self, cells: list):
        self.initiate_update(cells)
