from ..resources import Resource, ResourceType
from .cell import Cell, CellType

class DigesterType(CellType):
    uses: set[int]

    def init(self, uses: set[int]):
        self.uses = uses
        self.ctype = Digester

    def add(self, rtype: ResourceType):
        self.uses.add(rtype.id)


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