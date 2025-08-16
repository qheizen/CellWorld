import CellWorld.Tools.Logger.loggers as lg
import CellWorld.Constant.constants as const
from CellWorld.MainActors.Entities.game_actor_class import GameActor
import hashlib
import pygame
import random
from pygame import Vector2

_logger = lg.get_module_logger("CELLTYPE")

class CellType(GameActor):
    
    def __init__(self) -> None:
        self.name: str = const.NON_VALUE
        self.color: tuple = const.MISSED_COLOR
        self.size: int = const.MISSED_SIZE
        
        self.mass: float = const.BLACK_HOLE_MASS
        self.speed_min: float = 0.
        self.speed_max: float = 0.
        self.strength: float = 0.
        self.is_movable: bool = False
        self.is_gravitate: bool = False
        
        self.metabolism: float = 0.
        self.hunger_trigger_value: float = 0.
        self.eatable_radius: float = 0.
        self.lifetime: float = 0.
        self.is_mortal: bool = False
        self.is_can_be_hungered: bool = False
        self.food: list = []
        
        self.spawn_cell_names: list = []
        self.spawn_start_speed: Vector2 = Vector2(0,0)
        self.spawn_delay: int = 0 
        self.spawn_left_count: int = 0
        self.spawn_directions: list = []
        self.spawn_mutation_rate: float = 0.
        self.spawn_mutation_chance: float = 0.
        
        self.relationship: list = []
        self.attached_offset: list = []
        self.friendship: list = []
        self.actions: list = []
    
        self._float_hunger: float = float(random.randint(1,const.MISSED_HUNGER))
        self._attached_to: CellType = None
        self._hunting_at: CellType = None
        
        self.local_timer: float = 0.
    
    def init(self, transfer_object: dict):
        options_tags: dict = {
            "credentials": self.__safe_init_credentials,
            "physical": self.__safe_init_physic,
            "life": self.__safe_init_life,
            "community": self.__safe_init_community,
            "actions": self.__safe_init_actions,
            "spawner": self.__safe_init_spawner 
        }
        
        for tag, values in transfer_object:
            if init_func := options_tags[tag]:
                init_func(values)
                
        _logger.info(f"CellType - '{self.name}' - was created!")
    
    def __safe_setter(self, link_dict: dict, values_dict: dict):
        for key, value in values_dict:
            if attr := link_dict[key]:
                setattr(self, attr, value)
        
    def __safe_init_credentials(self, credentials: dict) -> None:
        link_dict = {
            "color": "color",
            "size": "size"
        }
        if not (name := credentials.get("name")):
            name = hashlib.md5(str(random.random()).encode()).hexdigest()
            credentials.pop("name")
            
        self.name = name
        self.set_position(credentials.get("start_pos", Vector2(0,0)))
        self.set_velocity(credentials.get("start_vel", self.random_vector()))
        self.__safe_setter(link_dict, credentials)

    def __safe_init_physic(self, physical: dict) -> None:
        link_dict = {
            "cell_mass": "mass",
            "cell_min_speed": "speed_min",
            "cell_max_speed": "speed_max",
            "strength": "strength",
            "is_movable": "is_movable",
            "is_gravitate": "is_gravitate"
        }
        self.__safe_setter(link_dict, physical)
    
    def __safe_init_life(self, life: dict) -> None:
        link_dict = {
            "metabolism_rate": "metabolism",
            "hunger_border": "hunger_trigger_value",
            "eat_radius": "eatable_radius",
            "lifetime": "lifetime",
            "is_mortal": "is_mortal",
            "is_can_be_hungered": "is_can_be_hungered",
            "food": "food"
        }
        self.__safe_setter(link_dict, life)
        
        
    def __safe_init_community(self, community: dict) -> None:
        link_dict = {
            "relationship": "relationship",
            "friendship": "friendship",
            "attached_offsets": "attached_offset"
        }
        self.__safe_setter(link_dict, community)
        
    def __safe_init_actions(self, actions: dict) -> None:
        link_dict = {
            "actions":"actions"
        }
        self.__safe_setter(link_dict, actions)
    
    def __safe_init_spawner(self, spawner: dict) -> None:
        link_dict = {
            "spawn_cell_types":"spawn_cell_names",
            "spawned_start_speed": "spawn_start_speed",
            "spawn_delay": "spawn_delay",
            "spawn_directions":"spawn_directions",
            "max_spawn_number":"spawn_left_count",
            "mutation_rate":"spawn_mutation_rate",
            "crossover_rate":"spawn_mutation_chance"
        }
        self.__safe_setter(link_dict, spawner)
        
    def initiate_spawn(self, global_manager):
        super().initiate_spawn(global_manager)
        self._float_hunger = float(random.randint(1, const.MISSED_HUNGER))
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self._vector_position.x), int(self._vector_position.y)), self.size)
        
    def console_print(self):
        _logger.warning(f"TYPE: {self.name}, HUNG: {self._float_hunger}, TIMER: {self.local_timer}, STATUS: {self._object_state}")
        
    def initiate_update(self, cells):
        
        
    def mutate(self, mutation_rate: float, mutation_chance: float):
        if random.uniform(0, mutation_chance):
            self.name = hashlib.md5(str(random.random()).encode()).hexdigest()
            self.eatable_radius *= 1 - random.uniform(-mutation_rate, mutation_rate)
            self.hunger_trigger_value *= 1 - random.uniform(-mutation_rate, mutation_rate)
            self.metabolism *= 1 - random.uniform(-mutation_rate, mutation_rate)
            self.speed_max *= 1 - random.uniform(-mutation_rate, mutation_rate)
            self.strength *= 1 - random.uniform(-mutation_rate, mutation_rate)