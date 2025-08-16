MISSED_COLOR: tuple = (255, 0, 255)
BLACK_HOLE_MASS = 1e5
MISSED_SIZE = 3
MISSED_HUNGER = 100

RAN_START = -100
RAN_END = 100

WINDOW_SIZE = [1920, 1080]
FPS = 60

NON_VALUE = "non-init-value"

EVENT_TYPES: list = ["spawn_entity_to_scene",
                     "spawn_empty_entity", "kill_all", "kill_with_name",
                     "kill_with_hunger_lower_than", "spawn_entity_near_entity",
                     "replace_entitie_type", "random", "hunger_debuff", "hunger_zero",
                     "mutate_all", "gravitation_off", "gravitation_on", "respawn_all"]