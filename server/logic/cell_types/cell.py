from ..vmath import Vector2d, to_bytes, merge
from ..resources import Resource
from ..objects import Sphere

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


