"""
Entities package — содержит классы игровых акторов, типов клеток, событий и менеджера мира.

Мы не импортируем всё содержимое модулей здесь автоматически, поскольку это может привести к
циклическим импортам (WorldManager <-> GameActor). Вместо этого даём пользователям возможность
импортировать конкретные модули:

from CellWorld.MainActors.Entities import game_cell_class
from CellWorld.MainActors.Entities.game_cell_class import CellType
"""

__all__ = [
    "game_actor_class",
    "game_cell_class",
    "game_event_class",
    "game_group_class",
    "game_world_manager",
]

# не делаем from .game_world_manager import WorldManager
# чтобы избежать циклических импортов при импорте модулей
