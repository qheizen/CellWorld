import pygame
from CellWorld.Actors.GUI.ActiveObject import ActiveObject
from typing import Callable, Optional, Any, Tuple


class Button(ActiveObject):
    def __init__(
        self,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        text: str,
        callback: Optional[Callable[..., Any]] = None,
        callback_args: Optional[tuple] = None,
        bg_color: Tuple[int,int,int] = (200, 200, 200),
        fg_color: Tuple[int,int,int] = (0, 0, 0),
        hover_color: Tuple[int,int,int] = (170, 170, 170),
    ):
        super().__init__(pos, size)
        self.text = text
        self.callback = callback
        self.callback_args = callback_args or ()
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.is_hover = False
        self.font = pygame.font.Font(None, 24)
        self.pressed = False

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        color = self.hover_color if self.is_hover else self.bg_color
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        pygame.draw.rect(screen, (0,0,0), self.rect, width=1, border_radius=6)
        self.draw_text(screen, self.text, self.font, self.fg_color, self.rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not (self.visible and self.enabled):
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hover = self.rect.collidepoint(event.pos)
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.rect.collidepoint(event.pos):
                self.pressed = False
                if self.callback:
                    try:
                        self.callback(*self.callback_args)
                    except Exception as e:
                        print("Button callback exception:", e)
                return True
            self.pressed = False
        return False