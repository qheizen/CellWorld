import pygame
from CellWorld.Actors.GUI.ActiveObject import ActiveObject

class Button(ActiveObject):
    
    def __init__(self, id, text, pos=(0, 0), size=(100, 40), color=(100, 150, 200), 
                 text_color=(255, 255, 255), form_id=None):
        super().__init__(id, pos, size, color, form_id)
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, 24)
        self._normal_color = color
        
    def draw(self, screen):
        if not self.is_visible:
            return
            
        pygame.draw.rect(screen, self._bg_color, self.rectangle, border_radius=5)
        
        if self.is_hovered:
            pygame.draw.rect(screen, (255, 255, 255, 50), self.rectangle, 
                            width=2, border_radius=5)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rectangle.center)
        screen.blit(text_surface, text_rect)