from .vmath import Vector2d
from .substrate import ResourceTypes, Resource, ResourceType
from .objects import Sphere
from typing import Literal

class CellType:
    id:int
    counter = 0
    CELLTYPES: list["CellType"] = []
    ctype: type
    name: str
    can_melt_in: set[int]
    cost: dict[int, int]
    energy_cost: int
    production_time: int
    energy: int
    mass: int
    radius: int
    speed: int

    def __init__(self, name:str, can_melt_in:set[int], cost: dict[int,int], energy_cost:int, production_time: int, energy: int, mass:int, radius:int, speed:int, *args: list) -> None:
        self.id = CellType.counter
        CellType.counter += 1
        self.name = name
        self.can_melt_in = can_melt_in
        self.cost = cost
        self.energy_cost = energy_cost
        self.production_time = production_time
        self.energy = energy
        self.mass = mass 
        self.radius = radius
        self.speed = speed
        self.init(*args)
    
    def init(self):
        self.ctype = Cell

    def get(self):
        return self

    def add_to_celltypes(self):
        CellType.CELLTYPES.append(self)

class MotherType(CellType):
    can_produce: set[int]

    def init(self, can_produce: set[int]):
        self.can_produce = can_produce
        self.ctype = Mother
    
    def add(self, ctype: CellType):
        self.can_produce.add(ctype.id)

class CollectorType(CellType):
    can_collect: set[int]
    strenght: int

    def init(self, can_collect:set[int], strenght: int):
        self.can_collect = can_collect
        self.strenght = strenght
        self.ctype = Collector
    
    def add(self, rtype: ResourceType):
        self.can_collect.add(rtype.id)

class DigesterType(CellType):
    uses: set[int]

    def init(self, uses: set[int]):
        self.uses = uses
        self.ctype = Digester

    def add(self, rtype: ResourceType):
        self.uses.add(rtype.id)

class CellTypes:
    def init() -> None:
        Acollector = CollectorType("Acollector", {0, 1, 2, 3}, dict(), 10, 120, 3, 5, 20, 2, {0}, 5)
        Bcollector = CollectorType("Bcollector", {1, 2, 3}, {0: 2}, 15, 150, 5, 7, 20, 1, {1}, 1)
        Amother = MotherType("Amother", {2, 3}, {0: 20}, 20, 500, 1, 50, 50, 0.2, set())
        Amother.add(Acollector)
        Acollector.add_to_celltypes()
        Bcollector.add_to_celltypes()
        Amother.add_to_celltypes()

    
class Cell(Sphere):
    owner: int
    energy: int
    speed: float
    target: Vector2d
    can_melt_in: set[int]
    alive: bool
    celltype: CellType

    def __init__(self, celltype: CellType, pos: Vector2d, owner: int) -> None:
        Sphere.__init__(self, pos, celltype.radius, Vector2d(0, 0), celltype.mass)
        self.owner = owner
        self.celltype = celltype
        self.energy = celltype.energy
        self.speed = celltype.speed
        self.can_melt_in = celltype.can_melt_in
        self.target = pos
        self.alive = True
        self.init()

    def init(self):
        pass

    def go_to(self):
        if not (self.target - self.pos).isInBox(Vector2d(-self.speed, -self.speed), Vector2d(self.speed, self.speed)):
            self.velocity = self.velocity + ((self.target - self.pos).norm() * (self.speed / self.mass))
        else:
            if self.velocity.lenght() <= self.speed:
                self.velocity = Vector2d(0, 0)
            else:
                self.velocity = self.velocity - self.velocity.norm() * self.speed

    
    def collision_proceeding(self):
        for obj in self.collisions:
            if type(obj) == Resource:
                if obj.resourcetype.id in self.can_melt_in:
                    self.digest()
        self.clear_colisions()

    def new_target(self, target: Vector2d):
        self.target = target

    def burn_fat(self):
        self.energy -= 1
        if self.energy == 0:
            self.digest()
    
    def digest(self):
        self.alive = False
    
    def iteration(self):
        Sphere.iteration(self)    
        self.go_to()

class Mother(Cell):
    resources: dict[int, int]
    celltype: MotherType
    next_to_produce: int
    timer: int

    def init(self):
        self.timer = 0
        self.next_to_produce = -1
        self.resources = dict()
        self.can_produce = self.celltype.can_produce
        for rtype in ResourceTypes.all:
            self.resources[rtype.id] = 0
    
    def collision_proceeding(self):
        for obj in self.collisions:
            if type(obj) == Collector:
                did_smth = False
                for rtype in obj.can_collect:
                    if obj.collection[rtype] > 0:
                        did_smth = True
                    self.resources[rtype] += obj.collection[rtype]
                    obj.mass -= obj.collection[rtype]
                    obj.collection[rtype] = 0
                if did_smth:
                    obj.burn_fat()
            if type(obj) == Resource:
                if obj.resourcetype.id in self.can_melt_in:
                    self.digest()
        self.clear_colisions()

    def burn_resource(self, plan: dict[int, int]):
        for rtype in plan:
            if self.resources[rtype] < plan[rtype]:
                self.energy += self.resources[rtype] * ResourceTypes.all[rtype - 1].energy_mass_ratio
                self.resources[rtype] = 0
            else:
                self.energy += plan[rtype] * ResourceTypes.all[rtype - 1].energy_mass_ratio
                self.resources[rtype] -= plan[rtype]

    def produce(self):
        if self.next_to_produce != -1:
            self.timer += 1
            if self.timer >= CellType.CELLTYPES[self.next_to_produce].production_time:
                new_cell: Cell = CellType.CELLTYPES[self.next_to_produce].ctype(CellType.CELLTYPES[self.next_to_produce], self.pos, self.owner)
                new_cell.new_target(self.pos + Vector2d(self.radius + new_cell.radius, 0))
                self.timer = 0
                return new_cell
    
    def start_production(self, ctype: int):
        if ctype in self.can_produce:
            for rtype in CellType.CELLTYPES[ctype].cost:
                if CellType.CELLTYPES[ctype].cost[rtype] > self.resources[rtype]:
                    return
            for rtype in CellType.CELLTYPES[ctype].cost:
                self.resources[rtype] -= CellType.CELLTYPES[ctype].cost[rtype]
            self.next_to_produce = ctype
            self.timer = 0


class Collector(Cell):
    celltype: CollectorType
    collection: dict[int, int]

    def init(self):
        self.can_collect = self.celltype.can_collect
        self.strenght = self.celltype.strenght
        self.collection = dict()
        for rtype in ResourceTypes.all:
            self.collection[rtype.id] = 0

    def collision_proceeding(self):
        for obj in self.collisions:
            if type(obj) == Resource:
                if obj.resourcetype.id in self.can_collect:
                    if self.strenght > self.mass - self.celltype.mass:
                        self.collection[obj.resourcetype.id] += 1
                        self.mass += 1
                        obj.mass -= 1
                        if obj.mass == 0:
                            obj.digest()
                elif obj.resourcetype.id in self.can_melt_in:
                    self.digest()
        self.clear_colisions()

class Digester(Cell):
    celltype: DigesterType
    uses: set[int]

    def init(self):
        self.uses = self.celltype.uses
    
    def collision_proceeding(self):
        for obj in self.collisions:
            if type(obj) == Digester:
                if obj.owner == self.owner:
                    continue
                for rtype in obj.can_melt_in:
                    if rtype in self.uses:
                        obj.digest()
                        self.burn_fat()
                        continue
            elif type(obj) == Cell:
                if obj.owner == self.owner:
                    continue
                for rtype in obj.can_melt_in:
                    if rtype in self.uses:
                        obj.digest()
                        break
                obj.burn_fat()
            if type(obj) == Resource:
                if obj.resourcetype.id in self.can_melt_in:
                    self.digest()
        self.clear_colisions()