from ..vmath import to_bytes, merge
from ..resources import ResourceTypes, Resource, ResourceType
from ..objects import Sphere
from .cell import Cell, CellType, BaseCell
from .mode import Modes

class TransporterType(CellType):
    def init(self):
        self.ctype = Transporter

class Transporter(Cell):
    celltype: TransporterType
    target_cell: Cell
    timer: int

    def init(self, target_cell: Cell = None, timer: int = 0):
        self.target_cell = target_cell
        self.timer = timer

    def collision_proceeding(self):
        if self.timer != 0:
            self.clear_colisions()
            return
        for obj in self.collisions:
            if isinstance(obj, BaseCell):
                for rtype in range(len(ResourceTypes.all)):
                    obj.collection[rtype] += self.collection[rtype]
                    self.collection[rtype] = 0
                self.digest()
        self.clear_colisions()
    
    def update(self):
        if self.timer != 0:
            self.timer -= 1
        return super().update()

    def auto(self):
        if (self.target_cell is None) or not (self.target_cell in BaseCell.objs):
            self.mode = Modes.passive
            self.new_target(self.pos)
            return
        self.new_target(self.target_cell.pos)

    def as_bytes(self) -> bytes:
        return merge(Cell.as_bytes(self), to_bytes([list(self.collection.values())]))