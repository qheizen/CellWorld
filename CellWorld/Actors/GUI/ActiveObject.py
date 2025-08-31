import pygame
from pygame import Vector2
from typing import Tuple

class ActiveObject:
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int]):
        self.pos = Vector2(pos)
        self.size = Vector2(size)
        self.rect = pygame.Rect(int(self.pos.x), int(self.pos.y), int(self.size.x), int(self.size.y))
        self.visible: bool = True
        self.enabled: bool = True

    def draw(self, screen: pygame.Surface):
        raise NotImplementedError

    def update(self, dt: float):
        pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Return True if the event was consumed.
        """
        return False

    def set_pos(self, x: int, y: int):
        self.pos.update(x, y)
        self.rect.topleft = (x, y)
        
    def draw_text(surface, text, font, color, rect, aa=True, bkg=None):
        text_surf = font.render(text, aa, color, bkg)
        surface.blit(text_surf, (rect.x + 5, rect.y + (rect.height - text_surf.get_height()) // 2))