from .mother_cell import MotherType
from .collector_cell import CollectorType
from .digester_cell import DigesterType

class CellTypes:
    def init() -> None:
        MotherType("Amother", {1, 2, 3}, {}, 40, 500, 1, 50, 50, 0.2, {4, 8, 0, 1})
        MotherType("Bmother", {2, 3}, {0: 20}, 30, 600, 1, 75, 75, 0.2, {5, 9, 0, 1, 2})
        MotherType("Cmother", {3}, {1: 20}, 40, 700, 1, 100, 100, 0.2, {6, 10, 0, 1, 2, 3})
        MotherType("Dmother", {3}, {2: 20}, 50, 800, 1, 125, 125, 0.2, {7, 11, 0, 1, 2, 3})
        CollectorType("Acollector", {0, 1, 2, 3}, {}, 10, 120, 3, 5, 20, 2, {0}, 5)
        CollectorType("Bcollector", {1, 2, 3}, {0: 2}, 15, 150, 5, 7, 20, 1, {1}, 3)
        CollectorType("Ccollector", {2, 3}, {1: 2}, 20, 180, 7, 9, 20, 0.5, {2}, 1)
        CollectorType("Dcollector", {3}, {2: 2}, 25, 210, 9, 11, 20, 0.25, {3}, 1)
        DigesterType("Adigester", {0, 1, 2, 3}, {0: 5}, 15, 150, 1, 5, 25, 3, {0})
        DigesterType("Bdigester", {2, 3}, {1: 5}, 25, 200, 2, 2, 25, 3, {1})
        DigesterType("Cdigester", {3}, {2: 5}, 35, 250, 5, 3, 25, 2, {2})
        DigesterType("Ddigester", {3}, {3: 5}, 45, 300, 6, 4, 25, 2, {3})
