from .vmath import Vector2d, to_bytes, merge
from .substrate import ResourceTypes, Resource, ResourceType
from .objects import Sphere

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
        self.add_to_celltypes()
    
    def init(self):
        self.ctype = Cell

    def get(self):
        return self

    def add_to_celltypes(self):
        CellType.CELLTYPES.append(self)
    
    def as_bytes(self) -> bytes:
        return to_bytes(self.id)

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
        MotherType("Amother", {1, 2, 3}, {0: 20}, 20, 500, 1, 50, 50, 0.2, {4, 8, 0, 1})
        MotherType("Bmother", {2, 3}, {0: 20}, 30, 600, 1, 75, 75, 0.2, {5, 9, 0, 1, 2})
        MotherType("Cmother", {3}, {1: 20}, 40, 700, 1, 100, 100, 0.2, {6, 10, 0, 1, 2, 3})
        MotherType("Dmother", {3}, {2: 20}, 50, 800, 1, 125, 125, 0.2, {7, 11, 0, 1, 2, 3})
        CollectorType("Acollector", {0, 1, 2, 3}, {}, 10, 120, 3, 5, 20, 2, {0}, 5)
        CollectorType("Bcollector", {1, 2, 3}, {0: 2}, 15, 150, 5, 7, 20, 1, {1}, 3)
        CollectorType("Ccollector", {2, 3}, {1: 2}, 20, 180, 7, 9, 20, 0.5, {2}, 1)
        CollectorType("Dcollector", {3}, {2: 2}, 25, 210, 9, 11, 20, 0.25, {3}, 1)
        DigesterType("Adigester", {1, 2, 3}, {0: 5}, 15, 150, 1, 5, 25, 3, {0})
        DigesterType("Bdigester", {2, 3}, {1: 5}, 25, 200, 2, 2, 25, 3, {1})
        DigesterType("Cdigester", {3}, {2: 5}, 35, 250, 3, 3, 25, 2, {2})
        DigesterType("Ddigester", {3}, {3: 5}, 45, 300, 4, 4, 25, 2, {3})
        

    
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

    @staticmethod
    def correct_init(celltype: CellType, pos: Vector2d, owner: int) -> "Cell":
        return celltype.ctype(celltype, pos, owner)

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
        if self.energy <= 0:
            self.digest()
    
    def digest(self):
        self.alive = False
    
    def iteration(self):
        Sphere.iteration(self)    
        self.go_to()
    
    def as_bytes(self) -> bytes:
        return merge(to_bytes([self.celltype, self.owner, self.energy]), Sphere.as_bytes(self))

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
            self.timer -= 1
            if self.timer <= 0:
                new_cell: Cell = Cell.correct_init(CellType.CELLTYPES[self.next_to_produce], self.pos, self.owner)
                new_cell.new_target(self.pos + Vector2d(self.radius + new_cell.radius, 0))
                self.next_to_produce = -1
                return new_cell

    def start_production(self, ctype: int):
        if ctype in self.can_produce:
            if self.energy < CellType.CELLTYPES[ctype].energy_cost:
                return
            for rtype in CellType.CELLTYPES[ctype].cost:
                if CellType.CELLTYPES[ctype].cost[rtype] > self.resources[rtype]:
                    return
            self.energy -= CellType.CELLTYPES[ctype].energy_cost
            for rtype in CellType.CELLTYPES[ctype].cost:
                self.resources[rtype] -= CellType.CELLTYPES[ctype].cost[rtype]
            self.next_to_produce = ctype
            self.timer = CellType.CELLTYPES[self.next_to_produce].production_time

    def iteration(self):
        Cell.iteration(self)
        return self.produce()

    def as_bytes(self) -> bytes:
        return merge(Cell.as_bytes(self), to_bytes([list(self.resources.values()), self.next_to_produce + 1, self.timer]))

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
                        obj.radius = obj.resourcetype.radius_mass_ratio * obj.mass
                        if obj.mass == 0:
                            obj.digest()
                elif obj.resourcetype.id in self.can_melt_in:
                    self.digest()
        self.clear_colisions()
    
    def as_bytes(self) -> bytes:
        return merge(Cell.as_bytes(self), to_bytes([list(self.collection.values())]))

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
            elif issubclass(type(obj), Cell):
                if obj.owner == self.owner:
                    continue
                for rtype in obj.can_melt_in:
                    if rtype in self.uses:
                        obj.digest()
                        break
            elif type(obj) == Resource:
                if obj.resourcetype.id in self.can_melt_in:
                    self.digest()
        self.clear_colisions()

