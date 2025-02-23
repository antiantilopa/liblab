from .transform import Transform
from .game_object import GameObject, DEBUG
from .vmath_mini import Vector2d
from .keybind import KeybindComponent
from .surface import SurfaceComponent
import pygame as pg

Camera = GameObject("Camera")

Camera.add_component(Transform(Vector2d(0, 0), 0))
Camera.add_component(SurfaceComponent(Vector2d(500, 500), 1))


def bind_keys_for_camera_movement(keys = [pg.K_w, pg.K_a, pg.K_s, pg.K_d], speed = 10):

    def camera_movement(g_obj: GameObject, active_keys: tuple[int]):
        if keys[0] in active_keys:
            g_obj.get_component(Transform).pos += Vector2d(0, -speed)
        if keys[1] in active_keys:
            g_obj.get_component(Transform).pos += Vector2d(-speed, 0)
        if keys[2] in active_keys:
            g_obj.get_component(Transform).pos += Vector2d(0, +speed)
        if keys[3] in active_keys:
            g_obj.get_component(Transform).pos += Vector2d(+speed, 0)
        if DEBUG:
            print(g_obj.get_component(Transform).pos)

    Camera.add_component(KeybindComponent(keys, 1, 0, camera_movement))
