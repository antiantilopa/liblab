from ..vmath import Vector2d, to_bytes, merge
from ..resources import ResourceTypes, Resource
from .cell import Cell, CellType
from .collector_cell import Collector

class MotherType(CellType):
    can_produce: set[int]

    def init(self, can_produce: set[int]):
        self.can_produce = can_produce
        self.ctype = Mother
    
    def add(self, ctype: CellType):
        self.can_produce.add(ctype.id)
    
class Mother(Cell):
    resources: dict[int, int]
    celltype: MotherType
    queue: list[int]
    timer: int

    def init(self):
        self.timer = 0
        self.queue = []
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
            if obj is Resource:
                if obj.resourcetype.id in self.can_melt_in:
                    self.digest()
                else:
                    self.resources[obj.resourcetype.id] += 1
                    obj.mass -= 1
                    obj.radius = obj.resourcetype.radius_mass_ratio * obj.mass
                    if obj.mass == 0:
                        obj.digest()
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
        if len(self.queue) != 0:
            self.timer -= 1
            if self.timer <= 0:
                new_cell: Cell = Cell.correct_init(CellType.CELLTYPES[self.queue[0]], self.pos, self.owner)
                new_cell.new_target(self.pos + Vector2d(self.radius + new_cell.radius, 0))
                self.queue.pop(0)
                if len(self.queue) != 0:
                    self.timer = CellType.CELLTYPES[self.queue[0]].production_time
                return new_cell

    def add_to_queue(self, ctype: int):
        if ctype in self.can_produce:
            if self.energy < CellType.CELLTYPES[ctype].energy_cost:
                return
            for rtype in CellType.CELLTYPES[ctype].cost:
                if CellType.CELLTYPES[ctype].cost[rtype] > self.resources[rtype]:
                    return
            self.energy -= CellType.CELLTYPES[ctype].energy_cost
            for rtype in CellType.CELLTYPES[ctype].cost:
                self.resources[rtype] -= CellType.CELLTYPES[ctype].cost[rtype]
            if len(self.queue) == 0:
                self.timer = CellType.CELLTYPES[ctype].production_time
            self.queue.append(ctype)
    
    def pop_from_queue(self, index: int):
        if index < len(self.queue):
            self.energy += CellType.CELLTYPES[self.queue[index]].energy_cost
            for rtype in CellType.CELLTYPES[self.queue[index]].cost:
                self.resources += CellType.CELLTYPES[self.queue[index]].cost[rtype]
            self.queue.pop(index)

    def iteration(self):
        Cell.iteration(self)
        return self.produce()

    def as_bytes(self) -> bytes:
        return merge(Cell.as_bytes(self), to_bytes([list(self.resources.values()), self.queue, self.timer]))
