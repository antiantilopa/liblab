from .cell import Cell
from .objects import Sphere
from .vmath import Vector2d

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
        self.size = Vector2d(1000, 1000)
    
    def set_borders(self, size: Vector2d):
        self.size = size
    
    def add_player(self) -> None:
        self.players.append(Player())
    
    def iteration(self):
        all_objects = self.objects.copy()
        for player in self.players:
            all_objects.extend(player.cells)
        Sphere.multicollisions(all_objects)
        for obj in all_objects:
            if obj.alive:
                obj.iteration()
            else:
                if obj in self.objects:
                    self.objects.remove(obj)
                else:
                    self.players[obj.owner].cells.remove(obj)
                obj.set_rigit(False)
                del obj
        

    
