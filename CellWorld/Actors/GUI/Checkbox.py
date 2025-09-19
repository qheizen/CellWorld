import pygame
from CellWorld.Actors.GUI.ActiveObject import ActiveObject

class Checkbox(ActiveObject):
    def __init__(self, id, text, pos=(0, 0), size=(20, 20), color=(100, 150, 200), 
                 text_color=(0, 0, 0), checked=False, form_id=None, font_size = 15):
        super().__init__(id, pos, (size[0] + 150, size[1]), color, form_id)
        self.text = text
        self.text_color = text_color
        self.checked = checked
        self.font = pygame.font.SysFont("Consolas", font_size)
        self.box_size = size
        self._normal_color = color
        
    def draw(self, screen):
        if not self.is_visible:
            return
            
        box_rect = pygame.Rect(self.rectangle.x, self.rectangle.y, 
                              self.box_size[0], self.box_size[1])
        pygame.draw.rect(screen, (55,51,86), box_rect, border_radius=4)
        pygame.draw.rect(screen, (100, 100, 100), box_rect, width=2, border_radius=4)
        
        if self.checked:
            pygame.draw.line(screen, (230, 230, 230), 
                            (box_rect.x + 4, box_rect.y + box_rect.height // 2),
                            (box_rect.x + box_rect.width // 2, box_rect.y + box_rect.height - 6), 3)
            pygame.draw.line(screen, (230, 230, 230), 
                            (box_rect.x + box_rect.width // 2, box_rect.y + box_rect.height - 6),
                            (box_rect.x + box_rect.width - 4, box_rect.y + 4), 3)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(midleft=(self.rectangle.x + self.box_size[0] + 10, 
                                                  self.rectangle.y + self.box_size[1] // 2))
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if not self.is_visible or not self.is_enabled or not self.is_clickable:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_rect = pygame.Rect(self.rectangle.x, self.rectangle.y, 
                                    self.rectangle.width, self.rectangle.height)
            if click_rect.collidepoint(event.pos):
                self.checked = not self.checked
                self._activate_func()
                return True
                
        return False
        
    def get_value(self):
        return self.checked