from .cell_types.cell import Cell, BaseCell, CellType
from .cell_types.cell_types import CellTypes
from .objects import Sphere, WORLD_SIZE
from .resources import Resource, ResourceTypes
from .vmath import Vector2d, to_bytes

class Player:
    id: int
    counter = 0
    cells: list[Cell]
    base_cells: list[BaseCell]

    def __init__(self) -> None:
        self.id = Player.counter
        Player.counter += 1
        self.cells = []
        self.base_cells = []
    
    def add_cell(self, celltype: CellType, pos: Vector2d) -> None:
        cell = celltype.ctype(celltype, pos, self.id)
        self.cells.append(cell)
        if isinstance(cell, BaseCell):
            self.base_cells.append(cell)

class Game:
    players: list[Player]
    size: Vector2d

    def __init__(self) -> None:
        self.players = []
        CellTypes.init()
        self.size = Vector2d(1000, 1000)
    
    def set_borders(self, size: Vector2d):
        self.size = size
    
    def add_player(self) -> None:
        self.players.append(Player())
    
    def add_test_obj(self):
        Resource(ResourceTypes.A, Vector2d(100, 100), 5, Vector2d(2, 0))
    
    def add_obj(self, rtype:int, pos: Vector2d, mass: int = 5):
        Resource(ResourceTypes.all[rtype], pos, mass, Vector2d(0, 0))
    
    def iteration(self):
        all_objects = Resource.objs + Cell.objs
        Sphere.multicollisions(all_objects)
        for obj in all_objects:
            if obj.alive:
                if isinstance(obj, Cell):
                    obj.update()
                obj.iteration()
            else:
                if isinstance(obj, Resource):
                    obj.digest()
                    obj.set_rigit(False)
                    del obj
                else:
                    self.players[obj.owner].cells.remove(obj)
                    obj.digest()
                    obj.set_rigit(False)
                    del obj
    
    def getGameData(self) -> bytes:
        cells = []
        for player in self.players:
            cells.extend(player.cells)
        return to_bytes([self.objects, cells])

    
