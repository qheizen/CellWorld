from __future__ import annotations
import hashlib
import random
import copy
import pygame
from pygame import Vector2
import CellWorld.Constant.constants as const
import CellWorld.Tools.Logger.loggers as lg
from CellWorld.MainActors.Entities.game_actor_class import GameActor

_logger = lg.get_module_logger("CELLTYPE")

class CellType(GameActor):

    def __init__(self) -> None:
        super().__init__() 
        self.name: str = const.NON_VALUE
        self.color: tuple = const.MISSED_COLOR
        self.size: int = const.MISSED_SIZE
        self.visual_distance: float = const.VISIBLE_RADIUS
        
        self.mass: float = const.BLACK_HOLE_MASS
        self.speed_min: float = 0.
        self.speed_max: float = 0.
        self.strength: float = 0.
        self.is_movable: bool = False
        self.is_gravitate: bool = False
        self.drag: float = 0.12
        
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
        self._attached_to: list = []
        self._hunting_at: CellType = None
        self._hungerred: bool = False
        
        self._friendly_cells = []
        
        self.local_timer: float = 0.
    
    def init(self, transfer_object: dict):
        options_tags = {
            "credentials": self.__safe_init_credentials,
            "physical": self.__safe_init_physic,
            "life": self.__safe_init_life,
            "community": self.__safe_init_community,
            "actions": self.__safe_init_actions,
        }

        for tag, values in transfer_object.items():
            init_func = options_tags.get(tag)
            if init_func:
                try:
                    init_func(values)
                except Exception as e:
                    _logger.critical(f"CellType (funcname: init): {e}")
                continue
            _logger.warning(f"CellType (funcname: init) cant find cell (name: '{tag}')")

        _logger.info(f"CellType (funcname: init) - cell_type was created (name: '{self.name}')")

    def __safe_setter(self, link_dict: dict, values_dict: dict):
        for key, value in values_dict.items():
            attr = link_dict.get(key)
            if attr is not None:
                setattr(self, attr, value)

    def __safe_init_credentials(self, credentials: dict) -> None:
        link_dict = {
            "color": "color",
            "size": "size",
            "visual_distance": "visual_distance"
        }
        name = credentials.pop("name", None)
        if not name:
            name = hashlib.md5(str(random.random()).encode()).hexdigest()
        self.name = name
        self.set_position(Vector2(0,0))
        self.set_velocity(credentials.get("start_vel", self.random_vector()))
        self.__safe_setter(link_dict, credentials)

    def __safe_init_physic(self, physical: dict) -> None:
        link_dict = {
            "cell_mass": "mass",
            "cell_min_speed": "speed_min",
            "cell_max_speed": "speed_max",
            "strength": "strength",
            "is_movable": "is_movable",
            "is_gravitate": "is_gravitate",
            "drag":"drag"
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
        if spawner := life["spawner"]:
            self.__safe_init_spawner(spawner)

    def __safe_init_community(self, community: dict) -> None:
        link_dict = {
            "relationship": "relationship",
            "friendship": "friendship",
            "attached_offsets": "attached_offset"
        }
        self.__safe_setter(link_dict, community)

    def __safe_init_actions(self, actions_list) -> None:
        if isinstance(actions_list, list):
            self.actions = actions_list

    def __safe_init_spawner(self, spawner: dict) -> None:
        link_dict = {
            "spawn_cell_types": "spawn_cell_names",
            "spawned_start_speed": "spawn_start_speed",
            "spawn_delay": "spawn_delay",
            "spawn_directions": "spawn_directions",
            "max_spawn_number": "spawn_left_count",
            "mutation_rate": "spawn_mutation_rate",
            "crossover_rate": "spawn_mutation_chance"
        }
        self.__safe_setter(link_dict, spawner)

    def initiate_spawn(self, global_manager):
        super().initiate_spawn(global_manager)
        self._float_hunger = float(random.randint(1, const.MISSED_HUNGER))
        self._last_spawn_time = 0.0
    
    def initiate_spawn_at_point(self, global_manager, cords):
        self._vector_position = self.safe_vector2_convert(cords)
        super().initiate_spawn(global_manager)
        self._float_hunger = float(random.randint(1, const.MISSED_HUNGER))
        self._last_spawn_time = 0.0

    def draw(self, surface):
        pygame.draw.circle(
            surface, self.color,
            (int(self._vector_position.x), int(self._vector_position.y)),
            self.size
        )
        for friend in self._friendly_cells:
            if friend != self._hunting_at:
                pygame.draw.line(surface, const.WHITE, (int(self._vector_position.x), int(self._vector_position.y)), (int(friend.x), int(friend.y)))
        self._friendly_cells = []
        
        if self._hunting_at:
            pygame.draw.line(surface, const.RED, (int(self._vector_position.x), int(self._vector_position.y)), 
                             (int(self._hunting_at._vector_position.x), int(self._hunting_at._vector_position.y)))


    def console_print(self):
        _logger.warning(
            f"TYPE: {self.name}, HUNG: {self._float_hunger:.2f}, "
            f"TIMER: {self.local_timer:.2f}, STATUS: {self._object_state},"
            f"VEL: {self._vector_velocity}, POS: {self._vector_velocity}"
        )

    def update(self, current_cells: list):
        result_force = Vector2(0, 0)
        for other in current_cells:
            if other is self or not isinstance(other, CellType) or not self.is_movable:
                continue

            vector_to_other = other._vector_position - self._vector_position
            dist = vector_to_other.length()
            if dist >= self.visual_distance or dist < const.OVERLAP:
                continue

            if self._object_state == "alive":
                result_force += self._relationships_move(other, vector_to_other)

            grav_force = self._gravitaion_move(other, vector_to_other)
            if self._hungerred:
                grav_force *= 0.1
            result_force += grav_force

        result_force += self._inscreen_force()

        self._metabolize()
        self._handle_spawning()
        self._check_death()
        self._add_movable(result_force)
            
    def _inscreen_force(self):
        margin = self.get_global_margin()
        strength = self.get_global_strength()
        size = self.get_global_screen_size()
        fx = 0.0
        fy = 0.0

        if self._vector_position.x < margin:
            fx = strength / max(self._vector_position.x, 1)
        elif self._vector_position.x > size[0] - margin:
            fx = -strength / max(size[0] - self._vector_position.x, 1) 

        if self._vector_position.y < margin:
            fy = strength / max(self._vector_position.y, 1) 
        elif self._vector_position.y > size[1] - margin:
            fy = -strength / max(size[1] - self._vector_position.y, 1) 
        return Vector2(fx, fy)
        
        
        
    def _add_movable(self, added_force) -> Vector2:
        if not self.is_movable:
            return Vector2(0, 0)

        vel = self._vector_velocity
        speed = vel.length()
        if self._hungerred:
            speed_max = self.speed_max * 2.0 
            drag_factor = 0.95
        else:
            speed_max = self.speed_max
            drag_factor = 0.9

        drag_multiplier = random.uniform(1 - self.drag, 1 + self.drag)
        added_force *= drag_multiplier

        if speed < speed_max:
            self.add_velocity(added_force / self.get_fps())

        self._vector_velocity *= drag_factor

        if speed < self.speed_min:
            self.add_velocity(self.speed_min / self.get_fps())

        self.add_position(self._vector_velocity)
        return self._vector_velocity

    def _gravitaion_move(self, other: CellType, vector_to_other) -> Vector2:
        if not self.is_gravitate:
            return Vector2(0, 0)

        g = self.get_constants().get("g", 0.0)
        distance_sq = max(vector_to_other.length_squared(), const.SAFE_DIST)
        if distance_sq <= 0:
            return Vector2(0, 0)

        try:
            force_dir = vector_to_other.normalize()
        except Exception:
            return Vector2(0, 0)

        acceleration = g * other.mass / distance_sq
        return force_dir * acceleration
    
    def _relationships_move(self, other: CellType, vector_to_other:Vector2) -> Vector2:
        force_to_return = Vector2(0,0)
        dist = max(vector_to_other.length(), const.SAFE_DIST)
        for cell_type in self.friendship:
            if other.name == cell_type["cell_type_name"]:
                if dist < cell_type["friend_distance"] and cell_type["is_line_need"]:
                    self._friendly_cells.append(other._vector_position)  
                    
        if not self.relationship:
            return force_to_return
        
        
        unit = vector_to_other / dist
        
        for cell_type in self.relationship:
            if other.name == cell_type["cell_type_name"]:
                if self._hungerred == False:
                    force_to_return += unit * self.strength * cell_type["relation"] / dist
                else:
                    force_to_return += unit * self.strength * abs(cell_type["relation"])

                distance_key = "preferred_distance" if self._hungerred else "hunger_distance"
                if other == self._hunting_at and self._hungerred == True:
                    continue
                if dist > cell_type[distance_key]:
                    force_to_return += unit * self.strength / dist
                elif dist < cell_type[distance_key]:
                    force_to_return -= unit * self.strength

                    
        for cell_type in self.attached_offset:
            if other.name == cell_type["cell_type_name"] and other in self._attached_to:
                if dist > cell_type["offset"]:
                    force_to_return += unit * self.strength
                elif dist < cell_type["offset"]:
                    force_to_return -= unit * self.strength
        
        if self._hunting_at and self._hunting_at._object_state == "alive":
            force_to_return += unit * self.strength
        else:
            self._hunting_at = None
        
        for cell_type in self.food:
            if other.name == cell_type["cell_type_name"] and other not in self._attached_to:
                if not self._hunting_at or dist <= (self._vector_position - self._hunting_at._vector_position).length():
                    self._hunting_at = other
                    
                if dist <= self.eatable_radius:
                    other.attach_to(self)
                    self._float_hunger += other._float_hunger * cell_type["stats_multiplier"]
                    self._hunting_at = None
        return force_to_return
    
    def attach_to(self, other):
        other._attached_to.append(self)
        self.initiate_death()

    def _metabolize(self): 
        if self._object_state != "alive":
            return
        
        if self.is_can_be_hungered:
            self._float_hunger -= self.metabolism / self.get_fps()
        
            if self._float_hunger <= self.hunger_trigger_value:
                self._hungerred = True
            else:
                self._hungerred = False
        return

    def _check_death(self):
        
        if self.is_mortal and self.is_can_be_hungered and self._float_hunger <= 0:
            self.initiate_death()
        
        if self.is_mortal and self.lifetime > 0 and self.local_timer >= self.lifetime:
            self.initiate_death()

    def _handle_spawning(self):
        if not self.spawn_cell_names or self.spawn_left_count <= 0 or not self._world_manager:
            return
        if self.spawn_delay <= 0 and self._last_spawn_time == 0.0:
            self._spawn_cell()
            return

        if self.local_timer >= self._last_spawn_time + self.spawn_delay:
            self._spawn_cell()
            
        self.local_timer += 1 / self.get_fps()

    def _spawn_cell(self):
        
        target_name = random.choice(self.spawn_cell_names)
        prototype = self.get_cell_with_name(target_name)
        if not prototype:
            _logger.critical(f"Cant find cell with name {target_name}")
            return
        
        new_cell = prototype.clone()
        new_cell.initiate_spawn(self._world_manager)
        new_cell.set_position(self._vector_position)
        if self.spawn_directions:
            try:
                dir_vector = Vector2(self.spawn_directions[0])
                new_cell.add_position(dir_vector)
            except Exception:
                new_cell.add_position(self.random_vector(-1, 1))
        else:
            new_cell.add_position(self.random_vector(-1, 1))
        new_cell.set_velocity(self.spawn_start_speed)
        # new_cell.mutate(self.spawn_mutation_rate, self.spawn_mutation_chance)
        self.spawn_to_world([new_cell])
        self.spawn_left_count -= 1
        self._last_spawn_time = self.local_timer
        
    def initiate_death(self):
        super().initiate_death()
        self.color = (20,20,20)

    def clone(self) -> CellType:
        """
        Create a safe clone of this CellType instance.
        Copy only plain data (numbers, tuples, lists, Vector2), avoid copying
        pygame-specific objects (like Clock) or references to world manager.
        """
        new = CellType()
        # Copy simple scalar and tuple attributes
        new.name = self.name
        new.color = tuple(self.color) if self.color is not None else const.MISSED_COLOR
        new.size = int(self.size)
        self.visual_distance = float(self.visual_distance)

        new.mass = float(self.mass)
        new.speed_min = float(self.speed_min)
        new.speed_max = float(self.speed_max)
        new.strength = float(self.strength)
        new.is_movable = bool(self.is_movable)
        new.is_gravitate = bool(self.is_gravitate)

        new.metabolism = float(self.metabolism)
        new.hunger_trigger_value = float(self.hunger_trigger_value)
        new.eatable_radius = float(self.eatable_radius)
        new.lifetime = float(self.lifetime)
        new.is_mortal = bool(self.is_mortal)
        new.is_can_be_hungered = bool(self.is_can_be_hungered)

        # Copy lists/structures safely
        new.food = copy.deepcopy(self.food)
        new.spawn_cell_names = list(self.spawn_cell_names)
        new.spawn_start_speed = Vector2(self.spawn_start_speed[0], self.spawn_start_speed[1])
        new.spawn_delay = int(self.spawn_delay)
        new.spawn_left_count = int(self.spawn_left_count)
        new.spawn_directions = copy.deepcopy(self.spawn_directions)
        new.spawn_mutation_rate = float(self.spawn_mutation_rate)
        new.spawn_mutation_chance = float(self.spawn_mutation_chance)

        new.relationship = copy.deepcopy(self.relationship)
        new.attached_offset = copy.deepcopy(self.attached_offset)
        new.friendship = copy.deepcopy(self.friendship)
        new.actions = copy.deepcopy(self.actions)
        new._float_hunger = float(random.randint(1, const.MISSED_HUNGER))
        new._attached_to = [] 
        new._hunting_at = None
        new.local_timer = 0.0
        new._last_spawn_time = 0.0

        new._vector_position = copy.deepcopy(self._vector_position)
        new._vector_velocity = copy.deepcopy(self._vector_velocity)
        new._object_state = const.NON_VALUE

        return new
