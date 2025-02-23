from .game_object import GameObject, Component
from .surface import SurfaceComponent
from .vmath_mini import Vector2d
from .transform import Transform
import pygame as pg



class LabelComponent(Component):
    text: str
    font: pg.font.Font
    delta_pos: Vector2d
    color: tuple[int, int, int]

    def __init__(self, text: str, font: pg.font.Font, delta_pos: Vector2d = Vector2d(0, 0), color: tuple[int, int, int] = (255, 255, 255)):
        self.text = text
        self.font = font
        self.delta_pos = delta_pos
        self.color = color
    
    def draw(self):
        surf = self.game_object.parent.get_component(SurfaceComponent)
        text = self.font.render(self.text, 1, self.color)
        size = Vector2d.from_tuple(text.get_size())

        surf.pg_surf.blit(text, (self.game_object.get_component(Transform).pos - (size*(1/2)) + self.delta_pos).as_tuple())



