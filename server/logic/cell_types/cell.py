from ..vmath import Vector2d, to_bytes, merge
from ..resources import Resource, ResourceTypes
from ..objects import Sphere
from .mode import Modes

class CellType:
    id: int
    counter = 0
    CELLTYPES: dict[str, "CellType"] = {}
    ctype: type
    name: str
    weakness_to: tuple[int, int, int, int]
    cost: tuple[int, int, int, int]
    production_time: int
    max_health: int
    mass: int
    radius: int
    speed: int
    isbuilding: bool

    def __init__(self, name: str, weakness_to: tuple[int, int, int, int], cost: tuple[int, int, int, int], production_time: int, max_health: int, mass: int, radius: int, speed: int) -> None:
        self.id = CellType.counter
        CellType.counter += 1
        self.name = name
        self.weakness_to = weakness_to
        self.cost = cost
        self.production_time = production_time
        self.max_health = max_health
        self.mass = mass 
        self.radius = radius
        self.speed = speed
        self.add_to_celltypes()
    
    def init(self):
        self.ctype = Cell

    def add_to_celltypes(self):
        CellType.CELLTYPES[self.name] = (self)
    
    def as_bytes(self) -> bytes:
        return to_bytes(self.id)

class Cell(Sphere):
    objs: list["Cell"] = []
    owner: int
    health: int
    speed: float
    target: Vector2d
    weakness_to: tuple[int, int, int, int]
    collection: list[int]
    alive: bool
    mode: int
    celltype: CellType
    target_pos: Vector2d
    target_resource: Resource
    target_cell: "Cell"

    def __init__(self, celltype: CellType, pos: Vector2d, owner: int) -> None:
        Sphere.__init__(self, pos, celltype.radius, Vector2d(0, 0), celltype.mass)
        self.owner = owner
        self.celltype = celltype
        self.health = celltype.max_health
        self.speed = celltype.speed
        self.weakness_to = celltype.weakness_to
        self.collection = [0] * len(ResourceTypes.all)
        self.target = pos
        self.alive = True
        self.mode = Modes.auto
        self.target_pos = None
        self.target_resource = None
        self.target_cell = None
        self.init()
        Cell.objs.append(self)

    def init(self):
        pass

    def go_to(self):
        if not (self.pos).fast_reach_test(self.target, self.speed):
            self.velocity = self.velocity + ((self.target - self.pos).norm() * (self.speed / self.mass))
        else:
            if self.velocity.lenght() <= self.speed:
                self.velocity = Vector2d(0, 0)
            else:
                self.velocity = self.velocity - self.velocity.norm() * self.speed

    def update(self):
        """update cell state and mode"""
        if self.mode == Modes.auto:
            self.auto()

    def auto(self):
        """cell auto mode"""
        pass

    def collision_proceeding(self):
        self.clear_colisions()

    def new_target(self, target: Vector2d):
        self.target = target

    def get_hurt(self, value: int = 1):
        self.health -= value
        if self.health <= 0:
            self.digest()
    
    def digest(self):
        self.alive = False
        Cell.objs.remove(self)
    
    def iteration(self):
        """sphere physics iteration"""
        Sphere.iteration(self)    
        self.go_to()

class BaseCellType(CellType):
    produces: list["CellType|BaseCellType"]

    def init(self, produces: list["CellType|BaseCellType"]):
        self.produces = produces
        self.isbuilding = True
        self.ctype = BaseCell

class BaseCell(Cell):
    queue: list[CellType]
    timer: int
    objs: list["BaseCell"] = []
    celltype: BaseCellType
    
    def init(self):
        self.timer = 0
        self.queue = []
        BaseCell.objs.append(self)

    def produce(self):
        if len(self.queue) != 0:
            self.timer -= 1
            if self.timer <= 0:
                new_cell: Cell = self.queue[0].ctype(self.queue[0], self.pos, self.owner)
                if self.target_pos is None:
                    new_cell.new_target(self.pos + Vector2d(self.radius + new_cell.radius, 0))
                else:
                    new_cell.new_target(self.target_pos)
                if not (self.target_cell is None):
                    new_cell.target_cell = self.target_cell
                if not (self.target_resource is None):
                        new_cell.target_resource = self.target_resource # for collectors and supply centers only
                self.queue.pop(0)
                if len(self.queue) != 0:
                    self.timer = self.queue[0].production_time

    def add_to_queue(self, ctype: CellType):
        if ctype in self.celltype.produces:
            for rtype in range(len(ResourceTypes.all)):
                if ctype.cost[rtype] > self.collection[rtype]:
                    return
            for rtype in range(len(ResourceTypes.all)):
                self.collection[rtype] -= ctype.cost[rtype]
            if len(self.queue) == 0:
                self.timer = ctype.production_time
            self.queue.append(ctype)
    
    def pop_from_queue(self, index: int):
        if index < len(self.queue):
            for rtype in range(len(ResourceTypes.all)):
                self.collection[rtype] += self.queue[index].cost[rtype]
            self.queue.pop(index)

    def update(self):
        self.produce()
        return super().update()

    def digest(self):
        BaseCell.objs.remove(self)
        return super().digest()