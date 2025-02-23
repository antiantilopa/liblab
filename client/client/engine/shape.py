from .vmath_mini import Vector2d, Angle
from .game_object import GameObject, Component
from .surface import SurfaceComponent
from .transform import Transform
from typing import Callable
from .color import ColorComponent
import pygame as pg

class ShapeComponent(Component):
    collide_formula: Callable[[Vector2d], bool]

    def __init__(self, collide_formula: Callable[[Vector2d], bool]) -> None:
        self.collide_formula = collide_formula

    def does_collide(self, pos: Vector2d) -> bool:
        return self.collide_formula((pos - self.game_object.get_component(Transform).pos).complexMultiply(self.game_object.get_component(Transform).rotation.toVector2d()))

    def iteration(self):
        pass

    def draw(self):
        pass

    def __str__(self):
        return f""

class CircleComponent(ShapeComponent):
    radius: float

    def __init__(self, radius: float) -> None:
        def collide_formula(pos: Vector2d) -> bool:
            return (pos.x**2 + pos.y**2) <= radius**2
        super().__init__(collide_formula)
        self.radius = radius

    def does_collide(self, pos: Vector2d) -> bool:
        return self.collide_formula(pos - self.game_object.get_component(Transform).pos)

    def draw(self):
        if self.game_object.contains_component(ColorComponent):
            pg.draw.circle(
                surface=self.game_object.parent.get_component(SurfaceComponent).pg_surf, 
                color=self.game_object.get_component(ColorComponent).color, 
                center=self.game_object.get_component(Transform).pos.as_tuple(),
                radius=self.radius)

    def __str__(self):
        return f"CircleComponent: {self.radius}"
    
class RectComponent(ShapeComponent):
    size: Vector2d

    def __init__(self, size: Vector2d) -> None:
        def collide_formula(pos: Vector2d) -> bool:
            return 2 * abs(pos.x) <= size.x and 2 * abs(pos.y) <= size.y
        super().__init__(collide_formula)
        self.size = size

    def draw(self):
        if self.game_object.contains_component(ColorComponent):
            pg.draw.rect(
                surface=self.game_object.parent.get_component(SurfaceComponent).pg_surf, 
                color=self.game_object.get_component(ColorComponent).color, 
                rect=((self.game_object.get_component(Transform).pos - (self.size * (1/2))).as_tuple() + self.size.as_tuple())
            )

    def __str__(self):
        return f"RectComponent: {self.size}"