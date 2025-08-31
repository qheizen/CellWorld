import pygame
import CellWorld.Constants.Constants as const
import CellWorld.Tools.Logger.loggers as lg
from CellWorld.Actors.GUI.Form import Form
from typing import List, Any

class GUIManager:
    def __init__(self):
        self.widgets: List[Any] = [] 

    def add(self, widget: Any):
        self.widgets.append(widget)

    def draw(self, screen: pygame.Surface):
        for w in self.widgets:
            if isinstance(w, Form):
                w.draw(screen)
            else:
                w.draw(screen)

    def update(self, dt: float):
        for w in self.widgets:
            if isinstance(w, Form):
                w.update(dt)
            else:
                w.update(dt)

    def handle_event(self, event: pygame.event.Event):
        for w in reversed(self.widgets):
            taken = False
            if isinstance(w, Form):
                taken = w.handle_event(event)
            else:
                taken = w.handle_event(event)
            if taken:
                return True
        return False