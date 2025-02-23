from engine.game_object import *
from engine.shape import *
from engine.surface import *
from engine.button import *
from engine.engine import *
from engine.label import *
from engine.camera import *

import pygame as pg

e = Engine(Vector2d(500, 500))

bind_keys_for_camera_movement()

world = GameObject("world")
world.add_component(Transform(Vector2d(0, 0)))
world.add_component(SurfaceComponent(Vector2d(500, 500)))
world.add_component(ColorComponent((200, 200, 200)))

GameObject.root.add_child(world)

button = GameObject("button1")

button.add_component(CircleComponent(50))
button.add_component(ColorComponent((255, 0, 0)))
button.add_component(ButtonComponent((1, 1, 1), 1, 1, lambda *_: print("!1")))
button.add_component(Transform(Vector2d(100, 100)))

world.add_child(button)

button2 = GameObject("button2")

button2.add_component(CircleComponent(50))
button2.add_component(ColorComponent((0, 200, 0)))
button2.add_component(ButtonComponent((1, 1, 1), 1, 1, lambda *_: print("!2")))
button2.add_component(Transform(Vector2d(0, 0)))

Camera.add_child(button2)

GameObject.show_geneology_tree()

e.run()