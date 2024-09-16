from server.logic.game import Game, Player
from server.logic.cell import Cell, Collector, CellTypes, CellType, Mother
from server.logic.vmath import Vector2d
from server.logic.substrate import Resource, ResourceTypes
from server.logic.objects import Sphere
import pygame

g = Game()

owner_colors = [
    (0, 255, 0), 
    (255, 0, 0),
    (0, 0, 255)
]

def main():


    g.add_player()
    g.add_player()
    CellTypes.init()
    g.players[0].cells.append(Cell.correct_init(CellType.CELLTYPES[0], Vector2d(200, 200), 0))
    g.players[0].cells.append(Cell.correct_init(CellType.CELLTYPES[4], Vector2d(200, 300), 0))
    g.players[0].cells.append(Cell.correct_init(CellType.CELLTYPES[8], Vector2d(300, 300), 0))
    g.players[1].cells.append(Cell.correct_init(CellType.CELLTYPES[0], Vector2d(800, 800), 1))
    g.players[1].cells.append(Cell.correct_init(CellType.CELLTYPES[4], Vector2d(700, 700), 1))
    g.players[1].cells.append(Cell.correct_init(CellType.CELLTYPES[8], Vector2d(800, 700), 1))
    # g.players[0].cells[0].init()

    for i in range(40):
        for j in range(40):
            g.objects.append(Resource(ResourceTypes.A, Vector2d(500 + i*21, 100 + j*21), 5 + (i+j) % 6, Vector2d(2, 0)))

    pygame.init()
    pygame.display.set_caption("liblab test")
    print(pygame.display.get_desktop_sizes())
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
                pygame.draw.circle(screen, owner_colors[cell.owner], cell.pos.as_tuple(), cell.radius + 5)
                pygame.draw.circle(screen, (0, 0, 0), cell.pos.as_tuple(), cell.radius + 2)
                pygame.draw.circle(screen, (min(50 + (cell.mass-5)*4, 255), max(200 - (cell.mass-5)*4, 0), 50), cell.pos.as_tuple(), cell.radius)
                pygame.draw.line(screen, (200, 200, 200), cell.pos.as_tuple(), (cell.pos + cell.velocity * 10).as_tuple(), 5)
        pygame.display.flip()

        print(clock.get_fps())


if __name__ == "__main__":
    main()