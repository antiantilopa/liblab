from engine.game_object import *
from engine.shape import *
from engine.surface import *
from engine.on_click import *
from engine.engine import *
from engine.label import *
from engine.camera import *

import pygame as pg

e = Engine(Vector2d(500, 500))

bind_keys_for_camera_movement()

world = GameObject("world")
world.add_component(Transform(Vector2d(0, 0)))
world.add_component(SurfaceComponent(Vector2d(500, 500)))
# world.add_component(ColorComponent((200, 200, 200)))

GameObject.root.add_child(world)

button = GameObject("button1")

button.add_component(CircleComponent(100))
button.add_component(ColorComponent((255, 0, 0)))
button.add_component(OnClickComponent((1, 1, 1), 1, 1, lambda *_: print("!1")))
button.add_component(Transform(Vector2d(0, 0)))
button.add_component(SurfaceComponent(Vector2d(1000, 1000)))
button.add_component(KeybindComponent([pg.K_q], 1, 1, lambda g_obj, _:g_obj.get_component(Transform).move(Vector2d(3, 0))))

world.add_child(button)

inner_button = GameObject("regregf")
inner_button.add_component(CircleComponent(50))
inner_button.add_component(ColorComponent((0, 255, 0)))
inner_button.add_component(OnClickComponent((1, 1, 1), 1, 1, lambda *_: print("inner3")))
inner_button.add_component(Transform(Vector2d(0, 0)))
inner_button.add_component(SurfaceComponent(Vector2d(200, 200)))

button.add_child(inner_button)

button2 = GameObject("button2")

button2.add_component(CircleComponent(50))
button2.add_component(ColorComponent((0, 0, 255)))
button2.add_component(OnClickComponent((1, 1, 1), 1, 1, lambda *_: print("!2")))
button2.add_component(Transform(Vector2d(0, 0)))
button2.add_component(SurfaceComponent(Vector2d(200, 200)))

Camera.add_child(button2)

GameObject.show_geneology_tree()

e.run()