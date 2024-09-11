from .cell import Cell
from .objects import Sphere

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

    def __init__(self) -> None:
        self.players = []
        self.objects = []
    
    def add_player(self) -> None:
        self.players.append(Player())
    