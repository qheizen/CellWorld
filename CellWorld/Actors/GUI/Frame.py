import pygame
from CellWorld.Actors.GUI.ActiveObject import ActiveObject

class Frame(ActiveObject):
    
    def __init__(self, id, pos=(0, 0), size=(0, 0), color=(240, 240, 240), form_id=None):
        super().__init__(id, pos, size, color, form_id)
        self.children = []
        self.padding = 10
        self.spacing = 5
        self.layout_dirty = True
        
    def add(self, child):
        self.children.append(child)
        self.layout_dirty = True
        return child
        
    def draw(self, screen):
        if not self.is_visible:
            return
            
        pygame.draw.rect(screen, self._bg_color, self.rectangle, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), self.rectangle, width=1, border_radius=5)
 
        if self.layout_dirty:
            self._update_layout()
        
        for child in self.children:
            if child.is_visible:
                child.draw(screen)
                
    def _update_layout(self):
        y_offset = self.padding
        for child in self.children:
            if child.is_visible:
                child.set_pos(self.rectangle.x + self.padding, self.rectangle.y + y_offset)
                child.set_size(self.rectangle.width - 2 * self.padding, child.rectangle.height)
                y_offset += child.rectangle.height + self.spacing
        self.layout_dirty = False
            
    def update(self, dt):
        super().update(dt)
        for child in self.children:
            if child.is_visible and child.is_enabled:
                child.update(dt)
                
    def handle_event(self, event):
        if not self.is_visible or not self.is_enabled:
            return False
            
        for child in reversed(self.children):
            if child.is_visible and child.is_enabled and child.handle_event(event):
                return True
                
        return super().handle_event(event)
        
    def get_children_data(self, form_id=None):
        data = {}
        for child in self.children:
            if hasattr(child, 'get_value') and (form_id is None or child.form_id == form_id):
                value = child.get_value()
                if value is not None:
                    data[child.id] = value

            if hasattr(child, 'get_children_data'):
                children_data = child.get_children_data(form_id)
                data.update(children_data)
        return data