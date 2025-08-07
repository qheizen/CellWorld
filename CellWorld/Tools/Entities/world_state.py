import pygame

class WorldItem:

    def __init__(self, cell_types:list, game_events:list, groups:list, global_options: dict):
        self.cell_types = cell_types
        self.game_events = game_events
        self.groups = groups

        self.global_options = global_options

    def get_cell_type_info(self, name: str) -> dict:

        