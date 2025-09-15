import pygame
from pygame import Vector2
import CellWorld.Tools.Logger.loggers as lg
from CellWorld.Actors.GUI.Button import Button
from CellWorld.Actors.GUI.Checkbox import Checkbox
from CellWorld.Actors.GUI.Frame import Frame
from CellWorld.Actors.GUI.TextInput import TextInput
import CellWorld.Tools.StaticLib as static

_logger = lg.get_module_logger("GUI")

def create_window(gui_manager):
    create_cell_frame = Frame("login_frame", (100, 100), (300, 500), (240, 240, 240), "create_cell")
    name_input = TextInput("cell_name", (0, 0), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Название клетки", "create_cell")
    create_cell_frame.add(name_input)
    
    mass = TextInput("cell_mass", (0, -40), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Вес клетки (float)", "create_cell")
    create_cell_frame.add(mass)
    
    strength = TextInput("cell_strength", (0, -80), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Сила клетки (float)", "create_cell")
    create_cell_frame.add(strength)
    
    hunger_border = TextInput("cell_hunger", (0, -120), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Когда голодает (float)", "create_cell")
    create_cell_frame.add(hunger_border)
    
    food_names = TextInput("food_names", (0, -160), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Кого ест (перечислить через запятую)", "create_cell")
    create_cell_frame.add(food_names)
    
    relationship = TextInput("food_names", (0, -200), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Отношения (клетка:отношение)", "create_cell")
    create_cell_frame.add(relationship)
    
    friendship = TextInput("food_names", (0, -240), (280, 30), (255, 255, 255), 
                              (240, 240, 240), "Друзья (клетка:отношение)", "create_cell")
    create_cell_frame.add(friendship)
    
    can_move = Checkbox("can_move", "Может двигаться?", (0, -280), (20, 20), 
                             (255, 255, 255), (240, 240, 240), True, "create_cell")
    create_cell_frame.add(can_move)
    
    def submit_login():
        form_data = gui_manager.get_form_data("create_cell")
        print("Login form data:", form_data)
        
    submit_btn = Button("submit", "Создать клетку", (0, -340), (100, 40), (100, 150, 200), 
                       (255, 255, 255), "login_form")
    submit_btn.set_handler(submit_login)
    create_cell_frame.add(submit_btn)
    
    gui_manager.add(create_cell_frame)
    return gui_manager