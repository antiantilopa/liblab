from .header_cell import HeaderType
from .supply_center_cell import SupplyCenterType
from .transporter_cell import TransporterType
from .transformer_cell import TransformerType
from .collector_cell import CollectorType
from .digester_cell import DigesterType

class CellTypes:
    def init() -> None:
        h = HeaderType("Header", (1, 1, 1, 1), (1, 0, 0, 0), 100, 100, 50, 20, 1)
        s = SupplyCenterType("SupplyCenter", (1, 1, 1, 1), (1, 0, 0, 0), 100, 100, 30, 20, 1)
        tp = TransporterType("Transporter", (1, 1, 1, 1), (1, 0, 0, 0), 100, 100, 5, 20, 1)
        tf = TransformerType("Transformer", (1, 1, 1, 1), (1, 0, 0, 0), 100, 100, 40, 20, 1)
        c = CollectorType("Collector", (1, 1, 1, 1), (1, 0, 0, 0), 100, 100, 10, 20, 1)
        d = DigesterType("Digester", (1, 1, 1, 1), (1, 0, 0, 0), 100, 100, 1, 20, 1)

        h.init([s, tp, tf])
        s.init([c, tp])
        tp.init()
        tf.init([tp], 100)
        c.init(3)
        d.init(0)