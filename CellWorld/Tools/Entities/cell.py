import pygame
from pygame import Vector2


class CellType:

    def __init__(self, global_object):
        self.global_object = global_object

        self.type_name: str = ""
        self.type_color: tuple = (0,0,0)
        self.type_mass: float = 0.0
        self.strength: float = 0.0
        self.hunger: float = 0.0
        self.spawns_left: int = 0

        self.is_movable: bool = True
        self.is_gravitate: bool = True
        self.is_mortal: bool = True
        self.is_can_hunger: bool = True
        self.is_spawner: bool = True

        self.min_speed: float = 0.0
        self.max_speed: float = 0.0
        self.metabolism_rate: float = 0.0
        self.hunger_border: float = 0.0
        self.eat_radius: float = 0.0
        self.lifetime: float = 0.0
        self.spawn_delay: float = 0.0
        self.mutation_rate: float = 0.0
        self.crossover_rate: float = 0.0

        self.food: list = []
        self.spawn_types: list = []
        self.spawn_directions: list = [pygame.Vector2(0,0)]
        self.attached_offsets: list = []
        self.relationships: list = []
        self.friendship: list = []
        self.actions: list = []

        self.spawn_start_speed = pygame.Vector2(0, 0)

        self.velocity = Vector2(0,0)
        self.position = Vector2(0,0)
        self.current_speed = Vector2(0,0)











