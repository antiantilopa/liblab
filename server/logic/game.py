from .cell import Cell, CellTypes
from .objects import Sphere
from .substrate import Resource, ResourceTypes
from .vmath import Vector2d, to_bytes

class Player:
    id: int
    counter = 0
    cells: list[Cell]

    def __init__(self) -> None:
        self.id = Player.counter
        Player.counter += 1
        self.cells = []
    
    def add_cell(self, cell) -> None:
        self.cells.append(cell)

class Game:
    players: list[Player]
    objects: list[Sphere]
    size: Vector2d

    def __init__(self) -> None:
        self.players = []
        self.objects = []
        CellTypes.init()
        self.size = Vector2d(1000, 1000)
    
    def set_borders(self, size: Vector2d):
        self.size = size
    
    def add_player(self) -> None:
        self.players.append(Player())
    
    def add_test_obj(self):
        r = Resource(ResourceTypes.A, Vector2d(100, 100), 5, Vector2d(2, 0))
        self.objects.append(r)
    
    def add_obj(self, rtype:int, pos: Vector2d):
        r = Resource(ResourceTypes.all[rtype], pos, 20, Vector2d(0, 0))
        self.objects.append(r)
    
    def iteration(self):
        all_objects = self.objects.copy()
        for player in self.players:
            all_objects.extend(player.cells)
        Sphere.multicollisions(all_objects)
        for obj in all_objects:
            if obj.alive:
                result = obj.iteration()
                if result == None:
                    continue
                if issubclass(type(result), Cell):
                    self.players[obj.owner].add_cell(result)
            else:
                if obj in self.objects:
                    print("wha?!")
                    obj.mass = 20
                    obj.radius = obj.resourcetype.radius_mass_ratio * obj.mass
                    obj.pos = Vector2d(500, 500)
                    obj.alive = True
                else:
                    self.players[obj.owner].cells.remove(obj)
                    obj.set_rigit(False)
                    del obj
    
    def getPlayerData(self) -> bytes:
        cells = []
        for player in self.players:
            cells.extend(player.cells)
        return to_bytes([self.objects, cells])

    
