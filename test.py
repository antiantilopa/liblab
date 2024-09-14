from server.logic.game import Game, Player
from server.logic.cell import Cell, Collector, CellTypes, CellType, Mother
from server.logic.vmath import Vector2d
from server.logic.substrate import Resource, ResourceTypes
from server.logic.objects import Sphere
import pygame

g = Game()

def calc(arg):
    x = arg
    for obj in g.objects[x * 30 : (x + 1) * 30]:
        if obj.alive:
            obj.collide(g.objects)
    return g.objects[x * 30 : (x + 1) * 30]

def main():


    g.add_player()
    CellTypes.init()
    g.players[0].cells.append(Collector(CellType.CELLTYPES[0], Vector2d(100, 100), 0))
    g.players[0].cells.append(Mother(CellType.CELLTYPES[2], Vector2d(100, 300), 0))
    # g.players[0].cells[0].init()

    for i in range(30):
        for j in range(30):
            g.objects.append(Resource(ResourceTypes.A, Vector2d(500 + i*21, 100 + j*21), 10, Vector2d(0, 0)))

    pygame.init()
    pygame.display.set_caption("liblab test")
    screen=pygame.display.set_mode((1800,1000))
    clock = pygame.time.Clock()
    selected: int = None
    sel = False

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit()
                processes.close()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    sel = False
                    for cell in g.players[0].cells:
                        if cell.touches(Vector2d.from_tuple(event.pos)):
                            selected = g.players[0].cells.index(cell)
                            sel = True
                            break
                    if sel == False:
                        for obj in g.objects:
                            if obj.touches(Vector2d.from_tuple(event.pos)):
                                print(obj.id)
                if event.button == 3:
                    if sel == True:
                        g.players[0].cells[selected].new_target(Vector2d.from_tuple(event.pos))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    if selected == 1:
                        g.players[0].cells[selected].start_production(0)


        screen.fill((0, 0, 0))

        # Sphere.multicollisions(g.objects + g.players[0].cells)
        g.iteration()

        for obj in g.objects:
            if obj.alive:
                pygame.draw.circle(screen, (obj.mass * 2, 200 - obj.mass * 2, 50), obj.pos.as_tuple(), obj.radius)
                pygame.draw.line(screen, (200, 20, 20), obj.pos.as_tuple(), (obj.pos + obj.velocity * 10).as_tuple(), 5)


        for cell in g.players[0].cells:
            if cell.alive:
                if type(cell) == Mother:
                    new = cell.produce()
                    if new != None:
                        g.players[0].add_cell(new)
                pygame.draw.circle(screen, (50 + (cell.mass-5)*4, 200 - (cell.mass-5)*4, 50), cell.pos.as_tuple(), cell.radius)
                pygame.draw.line(screen, (200, 200, 200), cell.pos.as_tuple(), (cell.pos + cell.velocity * 10).as_tuple(), 5)
        pygame.display.flip()

        print(clock.get_fps())


if __name__ == "__main__":
    main()