from .cell import Cell, BaseCell, BaseCellType
from .transporter_cell import TransporterType, Transporter

class SupplyCenterType(BaseCellType):

    def init(self, produces: list[Cell|BaseCell]):
        super().init(produces)
        self.ctype = SupplyCenter

class SupplyCenter(BaseCell):
    objs: list["SupplyCenter"]
    target_cell: BaseCell

    def init(self):
        self.target_cell = None
        return super().init()

    def auto(self):
        if not (self.target_cell is None):
            for ctype in self.celltype.produces:
                if isinstance(ctype, TransporterType):
                    self.add_to_queue(ctype)
        