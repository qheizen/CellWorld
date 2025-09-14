import os
import sys

_this_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_this_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import pygame
from pygame import Vector2
import CellWorld.Tools.Logger.loggers as lg
import CellWorld.Constants.Constants as const

# Настройка логирования
_logger = lg.get_module_logger("GUI")

# Пример использования
def create_login_form(gui_manager):
    # Создаем форму входа
    login_frame = Frame("login_frame", (100, 100), (300, 250), (240, 240, 240), "login_form")
    
    # Добавляем заголовок
    title_label = Button("title", "Login Form", (0, 0), (280, 30), (240, 240, 240), (0, 0, 0), "login_form")
    title_label.is_clickable = False
    login_frame.add(title_label)
    
    # Поле для имени пользователя
    username_input = TextInput("username", (0, 0), (280, 40), (255, 255, 255), 
                              (0, 0, 0), "Username", "login_form")
    login_frame.add(username_input)
    
    # Поле для пароля
    password_input = TextInput("password", (0, 0), (280, 40), (255, 255, 255), 
                              (0, 0, 0), "Password", "login_form")
    login_frame.add(password_input)
    
    # Чекбокс "Запомнить меня"
    remember_check = Checkbox("remember", "Remember me", (0, 0), (20, 20), 
                             (255, 255, 255), (0, 0, 0), False, "login_form")
    login_frame.add(remember_check)
    
    # Кнопка отправки
    def submit_login():
        form_data = gui_manager.get_form_data("login_form")
        print("Login form data:", form_data)
        
    submit_btn = Button("submit", "Login", (0, 0), (100, 40), (100, 150, 200), 
                       (255, 255, 255), "login_form")
    submit_btn.set_handler(submit_login)
    login_frame.add(submit_btn)
    
    gui_manager.add(login_frame)

# Инициализация приложения
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("GUI Example")
    clock = pygame.time.Clock()
    
    gui_manager = GUIManager()
    
    # Создаем форму входа
    create_login_form(gui_manager)
    
    # Добавляем обычную кнопку
    def test_button_click():
        print("Test button clicked!")
        
    test_button = Button("test_btn", "Click Me!", (500, 100), (120, 40), (200, 100, 100))
    test_button.set_handler(test_button_click)
    gui_manager.add(test_button)
    
    # Добавляем чекбокс
    test_checkbox = Checkbox("test_check", "Check me", (500, 160), (20, 20), 
                            (255, 255, 255), (0, 0, 0), False)
    test_checkbox.set_handler(lambda: print(f"Checkbox: {test_checkbox.checked}"))
    gui_manager.add(test_checkbox)
    
    # Добавляем текстовое поле
    test_text_input = TextInput("test_input", (500, 220), (200, 40), (255, 255, 255), 
                               (0, 0, 0), "Test input")
    gui_manager.add(test_text_input)
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # delta time in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            gui_manager.handle_event(event)
        
        gui_manager.update(dt)
        
        screen.fill((230, 230, 230))
        gui_manager.draw(screen)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()