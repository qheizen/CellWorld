import pygame
from pygame import Vector2
from typing import Callable, Dict, List, Optional, Any, Tuple
from CellWorld.Actors.GUI.ActiveObject import ActiveObject
from CellWorld.Actors.GUI.TextField import TextField


class Form:
    def __init__(self, pos: Tuple[int,int], size: Tuple[int,int], game_manager_callback: Optional[Callable[[Dict[str,str]],Any]] = None):
        self.pos = Vector2(pos)
        self.size = Vector2(size)
        self.rect = pygame.Rect(int(self.pos.x), int(self.pos.y), int(self.size.x), int(self.size.y))
        self.fields: Dict[str, TextField] = {}
        self.widgets: List[ActiveObject] = []
        self.game_manager_callback = game_manager_callback
        self.visible = True
        self.bg_color = (230, 230, 230)
        self.font = pygame.font.Font(None, 20)

    def add_field(self, name: str, field: TextField):
        # position field relative to form
        field.set_pos(int(self.pos.x + field.pos.x), int(self.pos.y + field.pos.y))
        self.fields[name] = field
        self.widgets.append(field)

    def add_widget(self, widget: ActiveObject):
        if isinstance(widget, ActiveObject):
            # position assumed absolute; keep it
            self.widgets.append(widget)

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, (0,0,0), self.rect, width=1)
        # title
        # pygame.draw... (optional)
        for w in self.widgets:
            w.draw(screen)

    def update(self, dt: float):
        for w in self.widgets:
            w.update(dt)

    def handle_event(self, event: pygame.event.Event) -> bool:
        consumed = False
        for w in self.widgets:
            taken = w.handle_event(event)
            consumed = consumed or taken
        return consumed

    def submit(self):
        data = {name: field.text for name, field in self.fields.items()}
        if self.game_manager_callback:
            try:
                self.game_manager_callback(data)
            except Exception as e:
                print("Form callback error:", e)