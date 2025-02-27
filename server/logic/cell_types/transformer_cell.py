from .cell import CellType, BaseCell, BaseCellType
from .transporter_cell import Transporter
from ..resources import ResourceTypes

class TransformerType(BaseCellType):
    transform_time: int

    def init(self, produces: list[CellType|BaseCell], transform_time: int):
        self.transform_time = transform_time
        super().init(produces)
        self.ctype = Transformer

class Transformer(BaseCell):
    transform_timer: int
    from_to: tuple[int, int]
    celltype: TransformerType

    def init(self):
        super().init()
        self.transform_timer = self.celltype.transform_time
        self.from_to = (0, 0)
    
    def update(self):
        super().update()
        if self.from_to[0] != self.from_to[1] and self.collection[self.from_to[0]] > 0:
            if self.transform_timer == 0:
                self.transform_timer = self.celltype.transform_time
                self.collection[self.from_to[0]] -= 1
                self.collection[self.from_to[1]] += 1
            else:
                self.transform_timer -= 1
        else:
            self.transform_timer = self.celltype.transform_time
    
    def auto(self):
        for cell in self.celltype.produces:
            if isinstance(cell, Transporter):
                for rtype in range(len(ResourceTypes.all)):
                    if rtype == self.from_to[1]:
                        if cell.cost[rtype] > self.collection[rtype]:
                            return
                    else:
                        if cell.cost[rtype] > 0:
                            return
                self.add_to_queue(cell)