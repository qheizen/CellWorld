import pygame
from CellWorld.Actors.GUI.ActiveObject import ActiveObject

class Frame(ActiveObject):
    
    def __init__(self, id, pos=(0, 0), size=(0, 0), color=(240, 240, 240), form_id=None):
        super().__init__(id, pos, size, color, form_id)
        self.children = []
        self.padding = 10
        self.spacing = 5
        self.layout_dirty = True
        self.dragging = False
        
    def add(self, child):
        self.children.append(child)
        self.layout_dirty = True
        return child
        
    def draw(self, screen):
        if not self.is_visible:
            return
            
        pygame.draw.rect(screen, (47,41,75), self.rectangle, border_radius=10)
        pygame.draw.rect(screen, (255,255,255), self.rectangle, width=2, border_radius=10)
 
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
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if (self.rectangle.x <= mouse_x <= self.rectangle.x + self.rectangle.width and 
                    self.rectangle.y <= mouse_y <= self.rectangle.y + 25):
                    self.dragging = True
                    self.drag_offset = (mouse_x - self.rectangle.x, mouse_y - self.rectangle.y)
                    return True
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.set_pos(mouse_x - self.drag_offset[0], mouse_y - self.drag_offset[1])
                for child in self.children:
                    child.rectangle.x = (-child.offset_x) + child.offset + self._position.x
                    child.rectangle.y = (-child.offset_y) + child.offset + self._position.y
                return True
            
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
    
    