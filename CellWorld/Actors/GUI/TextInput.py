import pygame
from CellWorld.Actors.GUI.ActiveObject import ActiveObject

class TextInput(ActiveObject):
    def __init__(self, id, pos=(0, 0), size=(200, 30), color=(55,51,86), 
                 text_color=(230, 230, 230), placeholder="", form_id=None, type_name: type = str, font_size = 15):
        super().__init__(id, pos, size, color, form_id)
        self.text_color = text_color
        self.placeholder = placeholder
        self.value = ""
        self.font = pygame.font.SysFont("Consolas", font_size)
        self.focusable = True
        self.focused = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self._normal_color = color
        self.type = type_name
        
    def draw(self, screen):
        if not self.is_visible:
            return
            
        pygame.draw.rect(screen, (55,51,86), self.rectangle, border_radius=5)
        border_color = (100, 100, 255) if self.focused else (55,51,86)
        pygame.draw.rect(screen, border_color, self.rectangle, width=2, border_radius=5)
        
        display_text = self.value if self.value else self.placeholder
        text_color = self.text_color if self.value else (150, 150, 150)
        
        text_surface = self.font.render(display_text, True, text_color)
        
        clip_rect = pygame.Rect(self.rectangle.x + 5, self.rectangle.y, 
                               self.rectangle.width - 10, self.rectangle.height)
        screen.set_clip(clip_rect)
        
        text_rect = text_surface.get_rect(midleft=(self.rectangle.x + 5, self.rectangle.centery))
        screen.blit(text_surface, text_rect)
        
        if self.focused and self.cursor_visible:
            if self.value:
                cursor_x = text_rect.right + 2
            else:
                cursor_x = text_rect.left
            pygame.draw.line(screen, self.text_color, 
                            (cursor_x, self.rectangle.y + 10),
                            (cursor_x, self.rectangle.bottom - 10), 2)
        
        screen.set_clip(None)
    
    def update(self, dt):
        super().update(dt)
        
        if self.focused:
            self.cursor_timer += dt
            if self.cursor_timer > 0.5:
                self.cursor_timer = 0
                self.cursor_visible = not self.cursor_visible
    
    def handle_event(self, event):
        if not self.is_visible or not self.is_enabled:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rectangle.collidepoint(event.pos):
                self.focused = True
                return True
            else:
                self.focused = False
                return False
                
        if self.focused and event.type == pygame.KEYDOWN:
            value_before = self.value
            if event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
                if self._active_func:
                    super()._activate_func()
                return True
            elif event.key == pygame.K_RETURN:
                self.focused = False
                if self._active_func:
                    super()._activate_func()
                return True
            elif event.unicode and event.unicode.isprintable():
                self.value += event.unicode
            try:
                self.type(self.value)
                if self._active_func:
                    super()._activate_func()
                return True
            except Exception as e:
                self.value = value_before
                return True
            
            
        return super().handle_event(event)
        
    def get_value(self):
        return self.value if self.value else None