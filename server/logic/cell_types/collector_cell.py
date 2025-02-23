from ..vmath import to_bytes, merge
from ..resources import ResourceTypes, Resource, ResourceType
from .cell import Cell, CellType

class CollectorType(CellType):
    can_collect: set[int]
    strenght: int

    def init(self, can_collect:set[int], strenght: int):
        self.can_collect = can_collect
        self.strenght = strenght
        self.ctype = Collector
    
    def add(self, rtype: ResourceType):
        self.can_collect.add(rtype.id)

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