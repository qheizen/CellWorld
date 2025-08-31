import pygame
from CellWorld.Actors.GUI.ActiveObject import ActiveObject
from typing import Callable, Optional, Any, Tuple


class TextField(ActiveObject):
    def __init__(
        self,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        placeholder: str = "",
        text: str = "",
        max_length: int = 256,
        submit_callback: Optional[Callable[[str], Any]] = None,
        change_callback: Optional[Callable[[str], Any]] = None,
    ):
        super().__init__(pos, size)
        self.text = text
        self.placeholder = placeholder
        self.max_length = max_length
        self.font = pygame.font.Font(None, 24)
        self.active = False  # focus
        self.cursor_visible = True
        self.cursor_timer = 0.0
        self.cursor_interval = 0.5
        self.submit_callback = submit_callback
        self.change_callback = change_callback

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        # background
        bg = (255, 255, 255) if self.active else (245, 245, 245)
        pygame.draw.rect(screen, bg, self.rect, border_radius=4)
        pygame.draw.rect(screen, (0,0,0), self.rect, width=1, border_radius=4)

        if self.text:
            self.draw_text(screen, self.text, self.font, (0,0,0), self.rect)
        else:
            self.draw_text(screen, self.placeholder, self.font, (120,120,120), self.rect)

        # cursor
        if self.active and self.cursor_visible:
            text_surf = self.font.render(self.text, True, (0,0,0))
            cursor_x = self.rect.x + 5 + text_surf.get_width()
            cursor_y1 = self.rect.y + 6
            cursor_y2 = self.rect.y + self.rect.height - 6
            pygame.draw.line(screen, (0,0,0), (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)

    def update(self, dt: float):
        # cursor blink
        self.cursor_timer += dt
        if self.cursor_timer >= self.cursor_interval:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0.0

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not (self.visible and self.enabled):
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.active = True
                # start text input if you want system IME:
                # pygame.key.start_text_input()
                return True
            else:
                self.active = False
                return False

        if not self.active:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.text:
                    self.text = self.text[:-1]
                    if self.change_callback:
                        try:
                            self.change_callback(self.text)
                        except Exception as e:
                            print("TextField change callback error:", e)
                return True
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if self.submit_callback:
                    try:
                        self.submit_callback(self.text)
                    except Exception as e:
                        print("TextField submit callback error:", e)
                return True
            # other control keys ignored
            if event.unicode and len(event.unicode) > 0 and len(self.text) < self.max_length:
                # basic filter: ignore control chars
                if ord(event.unicode) >= 32:
                    self.text += event.unicode
                    if self.change_callback:
                        try:
                            self.change_callback(self.text)
                        except Exception as e:
                            print("TextField change callback error:", e)
                return True

        return False