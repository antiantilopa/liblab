from .cell import BaseCell, BaseCellType

class HeaderType(BaseCellType):

    def init(self, produces: list[BaseCellType]):
        super().init(produces)
        self.ctype = Header
    
class Header(BaseCell):
    celltype: HeaderType