from .game_object import GameObject
from .surface import SurfaceComponent
from .camera import Camera
from .transform import Transform
from .color import ColorComponent
from .vmath_mini import Vector2d
import pygame as pg

class Engine:

    def __init__(self, window_size: Vector2d):
        pg.init()
        pg.font.init()
        screen = GameObject("main_screen")
        screen.add_component(Transform(Vector2d(0, 0)))
        screen.add_component(SurfaceComponent(window_size))
        screen.get_component(SurfaceComponent).pg_surf = pg.display.set_mode(screen.get_component(SurfaceComponent).pg_surf.get_size())
        GameObject.root = screen
        screen.add_child(Camera)

    def run(self):
        screen = GameObject.root
        
        run = True
        while run:
            pg.time.delay(100)
            for event in pg.event.get(eventtype=pg.QUIT):
                if event.type == pg.QUIT:
                    run = False
            self.iteration()
            self.draw()
            pg.display.flip()
            screen.get_component(SurfaceComponent).pg_surf.fill((0,0,0))

    def iteration(self):
        if SurfaceComponent.update_list:
            for g_obj in GameObject.objs:
                if g_obj.contains_component(SurfaceComponent):
                    SurfaceComponent.sorted_objs.append(g_obj)
                    print(g_obj, "was added")
            SurfaceComponent.update_list = False
            SurfaceComponent.sorted_objs = sorted(SurfaceComponent.sorted_objs, key = lambda g_obj: g_obj.get_component(SurfaceComponent).layer)
            print(*SurfaceComponent.sorted_objs)
        for g_obj in GameObject.objs:
            g_obj.iteration()

    def draw(self):
        g_obj = GameObject.root
        for g_obj in SurfaceComponent.sorted_objs:
            g_obj.draw()
            for child in g_obj.childs:
                if not child.contains_component(SurfaceComponent):
                    child.draw()
            g_obj.get_component(SurfaceComponent).blit()
    
    def update(self):
        for g_obj in GameObject.objs:
            g_obj.update()