from ..vmath import to_bytes, merge
from ..resources import ResourceTypes, Resource
from .cell import Cell, CellType
from .supply_center_cell import SupplyCenter
from .mode import Modes

class CollectorType(CellType):
    load_capacity: int

    def init(self, load_capacity: int):
        self.load_capacity = load_capacity
        self.ctype = Collector

class Collector(Cell):
    celltype: CollectorType
    target_resource: Resource
    target_cell: Cell

    def init(self, target_resource: Resource = None, target_cell: Cell = None):
        self.load_capacity = self.celltype.load_capacity
        self.target_resource = target_resource
        self.target_cell = target_cell

    def collision_proceeding(self):
        for obj in self.collisions:
            if isinstance(obj, Resource):
                if self.load_capacity > self.mass - self.celltype.mass:
                    self.collection[obj.resourcetype.id] += 1
                    self.mass += 1
                    obj.mass -= 1
                    obj.radius = obj.resourcetype.radius_mass_ratio * obj.mass
                    if obj.mass == 0:
                        obj.digest()
            if isinstance(obj, SupplyCenter):
                for rtype in range(len(ResourceTypes.all)):
                    obj.collection[rtype] += self.collection[rtype]
                    self.mass -= self.collection[rtype]
                    self.collection[rtype] = 0
        self.clear_colisions()
    
    def auto(self):
        if self.load_capacity == self.mass - self.celltype.mass:
            if (self.target_cell is None) or not (self.target_cell in SupplyCenter.objs):
                self.target_cell = self.get_nearest(SupplyCenter.objs, lambda s: s.owner == self.owner)
                if self.target_cell is None:
                    self.mode = Modes.passive
                    self.new_target(self.pos)
                    return
            self.new_target(self.target_cell.pos)
        else:
            if (self.target_resource is None) or not (self.target_resource in Resource.objs):
                self.target_resource = self.get_nearest(Resource.objs)
                if self.target_resource is None:
                    self.mode = Modes.passive
                    self.new_target(self.pos)
                    return
            self.new_target(self.target_resource.pos)

    def as_bytes(self) -> bytes:
        return merge(Cell.as_bytes(self), to_bytes([self.collection]))