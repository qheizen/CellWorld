import pygame
import CellWorld.Tools.Logger.loggers as lg

_logger = lg.get_module_logger("GUI")

class GUIManager:
    def __init__(self):
        self.widgets = []
        self.focused_widget = None
        self.last_hovered_widget = None

    def add(self, widget):
        self.widgets.append(widget)
        return widget

    def draw(self, screen):
        for widget in self.widgets:
            if widget.is_visible:
                widget.draw(screen)

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        
        current_hovered = None
        for widget in reversed(self.widgets):
            if widget.is_visible and widget.is_enabled and widget.is_clickable:
                was_hovered = widget.is_hovered
                widget.is_hovered = widget.rectangle.collidepoint(mouse_pos)
                
                if widget.is_hovered:
                    current_hovered = widget
                    if not was_hovered:
                        widget.on_mouse_enter()
                elif was_hovered:
                    widget.on_mouse_leave()
            
            if widget.is_visible and widget.is_enabled:
                widget.update(dt)
        
        if self.last_hovered_widget and self.last_hovered_widget != current_hovered:
            self.last_hovered_widget.on_mouse_leave()
        
        self.last_hovered_widget = current_hovered

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            focus_changed = False
            for widget in self.widgets:
                if hasattr(widget, 'focused') and widget.focused:
                    if not widget.rectangle.collidepoint(event.pos):
                        widget.focused = False
                        focus_changed = True
            
            if focus_changed:
                self.focused_widget = None

        for widget in reversed(self.widgets):
            if widget.is_visible and widget.is_enabled and widget.handle_event(event):
                return True
        return False

    def get_form_data(self, form_id=None):
        data = {}
        for widget in self.widgets:
            if hasattr(widget, 'form_id') and (form_id is None or widget.form_id == form_id):
                if hasattr(widget, 'get_value'):
                    value = widget.get_value()
                    if value is not None:
                        data[widget.id] = value

            if hasattr(widget, 'get_children_data'):
                children_data = widget.get_children_data(form_id)
                data.update(children_data)
        return data