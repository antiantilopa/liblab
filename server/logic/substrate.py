from .vmath import Vector2d
from .objects import Sphere

class ResourceType:
    id: int
    counter: int = 0
    energy_mass_ratio: float
    radius_mass_ratio: float

    def __init__(self, energy_mass_ratio: float, radius_mass_ratio: float) -> None:
        self.id = ResourceType.counter
        ResourceType.counter += 1
        self.energy_mass_ratio = energy_mass_ratio
        self.radius_mass_ratio = radius_mass_ratio

class ResourceTypes:
    A = ResourceType(0.01, 1)
    B = ResourceType(0.02, 0.5)
    C = ResourceType(0.03, 0.3)
    D = ResourceType(0.01, 0.4)
    all = (A, B, C, D)

class Resource(Sphere):
    resourcetype: ResourceType
    alive: bool

    def __init__(self, resourceType: ResourceType, pos: Vector2d, mass: int, velocity: Vector2d) -> None:
        self.resourcetype = resourceType
        self.alive = True
        Sphere.__init__(self, pos, resourceType.radius_mass_ratio * mass, velocity, mass)
    
    def digest(self) -> tuple[int, int]:
        self.alive = False
