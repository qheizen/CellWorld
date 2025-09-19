import pygame
import CellWorld.Tools.StaticLib as st

class DebugConsoleObject:
    
    def __init__(self,  pos=(0, 0), size=(400, 50), font_color=(240, 240, 240), font_size = 10, offset= 2, filled = False):
        
        self.pos = pos
        self.size = size
        self.text_color = font_color
        self.font = pygame.font.SysFont("Consolas", font_size)
        self.font_size = font_size
        self.offset = offset
        
        self.stack_size = int((self.size[1])/(font_size+offset))
        self.stack = []
        self.filled = filled
        
    def console_print(self, msg:str):
        self.stack.append(msg)
        if not self.filled:
            if len(self.stack) >= self.stack_size:
                self.stack.pop(0)
            
    def draw(self, screen):
        offset = 0
        for line in self.stack:
            st.draw_text_table(screen, line, self.pos[0], self.pos[1] + offset, self.text_color, "consolas", self.font_size)
            offset += self.font_size+self.offset
        
    def reform_stack(self, stack: list):
        self.stack = stack
        
    