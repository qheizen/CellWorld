import pygame
import os
from CellWorld.Actors.GUI.ActiveObject import ActiveObject
import CellWorld.Tools.Logger.loggers as lg

_logger = lg.get_module_logger("ICON")

class Icon(ActiveObject):
    
    def __init__(self, id, text, pos=(0, 0), size=(100, 40), color=(100, 150, 200), 
                 text_color=(255, 255, 255), form_id=None, image_path = "", font_size = 15):
        super().__init__(id, pos, size, color, form_id)
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont("Consolas", font_size)
        self._normal_color = color
        self._image = self._get_image(image_path)
    
    def _get_image(self, image_path):
        try:
            if not image_path:
                return None
            if not os.path.exists(image_path):
                _logger.warning(f"Файл изображения не найден: {image_path}")
                return None
            image = pygame.image.load(image_path)
            image = image.convert_alpha()
            
            if self.rectangle:
                image = pygame.transform.scale(image, (self.rectangle.height, self.rectangle.height))
                
            return image
        except pygame.error as e:
            _logger.warning(f"Ошибка загрузки изображения: {e}")
            return None
        
    def draw(self, screen):
        if not self.is_visible:
            return
            
        pygame.draw.rect(screen, self._bg_color, self.rectangle, border_radius=5)
        
        if self.is_hovered:
            pygame.draw.rect(screen, (255, 255, 255, 50), self.rectangle, 
                            width=2, border_radius=2)
        
        if self._image:
            screen.blit(self._image, self.rectangle)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rectangle.center)
        screen.blit(text_surface, text_rect)
            