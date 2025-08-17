"""
CellWorld package.

Содержит базовую метаинформацию о пакете.
Не выполняет импорт модулей, чтобы избежать циклических импортов при инициализации.
"""

__all__ = [
    "Simulation",
    "Constant",
    "MainActors",
    "SerializableTools",
    "Tools",
]

__version__ = "0.1.0"
