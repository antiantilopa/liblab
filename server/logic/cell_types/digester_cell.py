from .cell import Cell, CellType

class DigesterType(CellType):
    weapon: int

    def init(self, weapon: int):
        self.ctype = Digester
        self.wea = weapon


class Digester(Cell):
    celltype: DigesterType
    
    def collision_proceeding(self):
        for obj in self.collisions:
            if isinstance(obj, Cell):
                if obj.owner == self.owner:
                    continue
                obj.get_hurt(obj.celltype.weakness_to[self.celltype.weapon])
        self.clear_colisions()