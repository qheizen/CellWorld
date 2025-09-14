import pygame
from pygame import Vector2
import CellWorld.Tools.Logger.loggers as lg
import CellWorld.Constants.Constants as const

_logger = lg.get_module_logger("GUI")

class ActiveObject:
    def __init__(self, id, pos=(0, 0), size=(0, 0), color=const.TEMPLATE_COL, form_id=None):
        self.id = id
        self._position = Vector2(pos)
        self._size = Vector2(size)
        self._bg_color = color
        self._normal_color = color
        self.form_id = form_id
        
        self.rectangle = pygame.Rect(int(self._position.x), int(self._position.y), 
                                    int(self._size.x), int(self._size.y))
        
        self.is_visible = True
        self.is_enabled = True
        self.is_clickable = True
        self.is_hovered = False
        self.is_pressed = False
        
        self.status = const.STATUSES["0"]
        self._active_func = None
        self._transition_time = 0.2 
        self._transition_progress = 0  
        self._target_bg_color = color
        self._original_bg_color = color
        
    def draw(self, screen):
        raise NotImplementedError
    
    def update(self, dt):
        if self._transition_progress < 1 and self._bg_color != self._target_bg_color:
            self._transition_progress += dt / self._transition_time
            if self._transition_progress > 1:
                self._transition_progress = 1
                
            r = int(self._original_bg_color[0] + (self._target_bg_color[0] - self._original_bg_color[0]) * self._transition_progress)
            g = int(self._original_bg_color[1] + (self._target_bg_color[1] - self._original_bg_color[1]) * self._transition_progress)
            b = int(self._original_bg_color[2] + (self._target_bg_color[2] - self._original_bg_color[2]) * self._transition_progress)
            self._bg_color = (r, g, b)
    
    def on_mouse_enter(self):
        self.set_target_color(self.get_hover_color())
    
    def on_mouse_leave(self):
        self.set_target_color(self.get_normal_color())
    
    def handle_event(self, event):
        if not self.is_visible or not self.is_enabled or not self.is_clickable:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rectangle.collidepoint(event.pos):
                self.is_pressed = True
                self.set_target_color(self.get_pressed_color())
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed:
                self.is_pressed = False
                if self.rectangle.collidepoint(event.pos):
                    self.set_target_color(self.get_hover_color())
                    self._activate_func()
                else:
                    self.set_target_color(self.get_normal_color())
                return True
            
        return False
    
    def set_target_color(self, color):
        self._original_bg_color = self._bg_color
        self._target_bg_color = color
        self._transition_progress = 0
    
    def get_normal_color(self):
        return self._normal_color
    
    def get_hover_color(self):
        r, g, b = self._normal_color
        return (min(r + 20, 255), min(g + 20, 255), min(b + 20, 255))
    
    def get_pressed_color(self):
        r, g, b = self._normal_color
        return (max(r - 20, 0), max(g - 20, 0), max(b - 20, 0))
    
    def set_size(self, w, h):
        self._size.update(w, h)
        self.rectangle.size = (int(w), int(h))
    
    def set_pos(self, x, y):
        self._position.update(x, y)
        self.rectangle.topleft = (int(x), int(y))
    
    def _activate_func(self, *args, **kwargs):
        try:
            if callable(self._active_func):
                self._active_func(*args, **kwargs)
        except Exception as e:
            _logger.error(f"Error in active function: {e}")
    
    def set_handler(self, func):
        if callable(func):
            self._active_func = func