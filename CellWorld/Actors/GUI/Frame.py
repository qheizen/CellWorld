import pygame
from CellWorld.Actors.GUI.ActiveObject import ActiveObject

class Frame(ActiveObject):
    
    def __init__(self, id, pos=(0, 0), size=(0, 0), color=(240, 240, 240), form_id=None, padding = 10, offset = 10, board_pad = 2, board_color = (255,255,255)):
        super().__init__(id, pos, size, color, form_id, offset)
        self.children = []
        self.padding = padding
        self.spacing = 5
        self.layout_dirty = True
        self.dragging = False
        self._bord_radius = board_pad
        self._bord_color = board_color
        
    def add(self, child):
        self.children.append(child)
        self.layout_dirty = True
        return child
        
    def draw(self, screen):
        if not self.is_visible:
            return
            
        pygame.draw.rect(screen, self._bg_color, self.rectangle, border_radius=10)
        if not self._bord_radius == 0:
            pygame.draw.rect(screen, self._bord_color, self.rectangle, width=self._bord_radius, border_radius=10)
 
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
                y_offset = self.padding
                mouse_x, mouse_y = event.pos
                self.set_pos(mouse_x - self.drag_offset[0], mouse_y - self.drag_offset[1])
                for child in self.children:
                    child.set_pos(self.rectangle.x + self.padding, self.rectangle.y + y_offset)
                    child.set_size(self.rectangle.width - 2 * self.padding, child.rectangle.height)
                    y_offset += child.rectangle.height + self.spacing
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
    
    