from .game_object import Component, GameObject, DEBUG
import pygame as pg
from .vmath_mini import Vector2d

from .transform import Transform
from .color import ColorComponent

class SurfaceComponent(Component):
    layer: int 
    pg_surf: pg.Surface
    
    sorted_objs: list[GameObject] = []
    update_list: bool = False

    def __init__(self, size: Vector2d, layer: int = 0):
        self.pg_surf = pg.Surface(size.as_tuple())
        if DEBUG:
            self.pg_surf.set_alpha(128)
        self.layer = layer
        SurfaceComponent.update_list = True

    def set_layer(self, layer: int):
        self.layer = layer
        sorted(SurfaceComponent.sorted_objs, lambda g_obj: g_obj.get_component(SurfaceComponent).layer)

    def draw(self):
        if self.game_object.contains_component(ColorComponent):
            self.pg_surf.fill(self.game_object.get_component(ColorComponent).color)

    def blit(self):
        if self.game_object == GameObject.root:
            surf = self
        else:
            surf = self.game_object.parent.get_component(SurfaceComponent) 

        pos = self.game_object.get_component(Transform).pos - GameObject.get_group_by_tag("Camera")[0].get_component(Transform).pos
        g_obj = self.game_object
        while not (g_obj.parent is None):
            pos += g_obj.parent.get_component(Transform).pos
            g_obj = g_obj.parent
        surf.pg_surf.blit(self.pg_surf, pos.as_tuple())


