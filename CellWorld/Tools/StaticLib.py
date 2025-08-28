from pygame import Vector2
import pygame
import CellWorld.Constants.Constants as const
import random
import hashlib

def convert_to_vec(value) -> Vector2:
    """
    Safe value convertation to two dimensial Vector
    """
    if value is None:
        return Vector2(0, 0)
    if isinstance(value, Vector2):
        return value
    try:
        if isinstance(value, (int, float)):
            return Vector2(value, value)
        return Vector2(value)
    except (TypeError, ValueError):
        return Vector2(0, 0)
    

def random_vector(start=-const.RANDOM_RANGE, final=const.RANDOM_RANGE):
    start_vector: Vector2 = convert_to_vec(start)
    final_vector: Vector2 = convert_to_vec(final)
    return Vector2(
            random.uniform(start_vector.x, final_vector.x),
            random.uniform(start_vector.y, final_vector.y)
        )
    
    
def draw_text_table(canvas, text, x, y, color = const.TEMPLATE_COL):
    font = pygame.font.SysFont(const.FONT, const.FONT_SIZE)
    text_surface = font.render(text, True, color)
    canvas.blit(text_surface, (x, y))
    

def get_random_hash():
    return hashlib.md5(str(random.random()).encode()).hexdigest()