from server.logic.game import Game, Player
from server.logic.cell import Cell, Collecter
from server.logic.vmath import Vector2d
from server.logic.substrate import Resource, ResourceTypes
import pygame

g = Game()
g.add_player()
c = Collecter(Vector2d(100, 100), 20, 5, 5, 0, 100)
g.players[0].add_cell(c)
c.init_collection({1, 2, 3, 4}, 25)
g.objects.append(Resource(ResourceTypes.C, Vector2d(500, 500), 100, Vector2d(1, 2)))
pygame.init()
pygame.display.set_caption("liblab test")
screen=pygame.display.set_mode((1800,1000))

selected: int = None
sel = False

while True:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # print("here1")
                sel = False
                for cell in g.players[0].cells:
                    # print("here2")
                    if cell.touches(Vector2d.from_tuple(event.pos)):
                        # print("here3")
                        selected = g.players[0].cells.index(cell)
                        sel = True
                        break
                if sel == False:
                    selected = None
            if event.button == 3:
                # print("here4")
                if sel == True:
                    # print("here5")
                    g.players[0].cells[selected].new_target(Vector2d.from_tuple(event.pos))


    screen.fill((0, 0, 0))
    
    for obj in g.objects:
        if obj.alive:
            obj.flow()
            obj.collide(g.objects)
            obj.borders(Vector2d(0, 0), Vector2d(1800, 1000))
            pygame.draw.circle(screen, (obj.mass * 2, 200 - obj.mass * 2, 50), obj.pos.as_tuple(), obj.radius)
            pygame.draw.line(screen, (200, 20, 20), obj.pos.as_tuple(), (obj.pos + obj.velocity * 10).as_tuple(), 5)
    
    for cell in g.players[0].cells:
        cell.flow()
        cell.go_to()
        cell.collide(g.objects)
        cell.collide(g.players[0].cells)
        cell.borders(Vector2d(0, 0), Vector2d(1800, 1000))
        cell.collision_proceeding()
        pygame.draw.circle(screen, (cell.mass * 10, 250 - cell.mass * 10, 50), cell.pos.as_tuple(), cell.radius)
        pygame.draw.line(screen, (200, 20, 20), cell.pos.as_tuple(), (cell.pos + cell.velocity * 10).as_tuple(), 5)

    pygame.display.flip()