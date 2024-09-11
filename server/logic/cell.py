from .vmath import Vector2d
from .substrate import ResourceTypes, Resource
from .objects import Sphere

class Cell(Sphere):
    owner: int
    energy: int
    speed: int
    target: Vector2d
    can_melt_in: set[int]
    alive: bool

    def __init__(self, pos: Vector2d, radius: int, speed: int, mass: int, owner: int, energy: int, can_melt_in: set[int] = set()) -> None:
        Sphere.__init__(self, pos, radius, Vector2d(0, 0), mass)
        self.owner = owner
        self.energy = energy
        self.speed = speed
        self.can_melt_in = can_melt_in
        self.target = pos
        self.alive = True

    def go_to(self):
        if self.target != self.pos:
            if (self.target - self.pos).lenght() < self.speed and self.velocity.dotMultiply(self.target - self.pos) > 0:
                self.velocity = self.target - self.pos
            else:
                self.velocity = (self.target - self.pos).norm() + self.velocity
                if self.velocity.lenght() > self.speed:
                    self.velocity = self.velocity.norm() * self.speed
        else:
            self.velocity = Vector2d(0, 0)
    
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
    
class Mother(Cell):
    resources: dict[int, int]
    next_to_produce: int

    def init_resources(self):
        self.resources = dict()
        for rtype in ResourceTypes.all:
            self.resources[rtype.id] = 0
    
    def collision_proceeding(self):
        for obj in self.collisions:
            if type(obj) == Collecter:
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
        pass # TODO

class Collecter(Cell):
    can_collect: set[int]
    collection: dict[int, int]
    strenght: int

    def init_collection(self, can_collect: set[int], strenght: int):
        self.can_collect = can_collect
        self.strenght = strenght
        self.collection = dict()
        for rtype in ResourceTypes.all:
            self.collection[rtype.id] = 0

    def collision_proceeding(self):
        for obj in self.collisions:
            if type(obj) == Resource:
                if obj.resourcetype.id in self.can_collect:
                    if self.strenght > self.mass:
                        self.collection[obj.resourcetype.id] += 1
                        self.mass += 1
                        obj.mass -= 1
                        if obj.mass == 0:
                            obj.digest()
                elif obj.resourcetype.id in self.can_melt_in:
                    self.digest()
        self.clear_colisions()

class Digester(Cell):
    uses: set[int]

    def init_uses(self, uses):
        self.uses = uses
    
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
    
class CellType:
    id:int
    counter = 1
    name: str
    can_melt_in: set[int]
    cost: dict[int, int]
    energy_cost: int
    energy: int
    mass: int
    radius: int
    speed: int

    def __init__(self, name:str, can_melt_in:set[int], cost: dict[int,int], energy_cost:int, energy: int, mass:int, radius:int, speed:int) -> None:
        self.id = CellType.counter
        CellType.counter += 1
        self.name = name
        self.can_melt_in = can_melt_in
        self.cost = cost
        self.energy_cost = energy_cost
        self.energy = energy
        self.mass = mass 
        self.radius = radius
        self.speed = speed


class CellTypes:
    pass