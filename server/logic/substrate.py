from .vmath import Vector2d, to_bytes, merge
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
    
    def as_bytes(self) -> bytes:
        return to_bytes(self.id)

class ResourceTypes:
    A = ResourceType(3, 1)
    B = ResourceType(4, 1)
    C = ResourceType(5, 1)
    D = ResourceType(3, 1)
    all = (A, B, C, D)

class Resource(Sphere):
    resourcetype: ResourceType
    alive: bool

    def __init__(self, resourceType: ResourceType, pos: Vector2d, mass: int, velocity: Vector2d) -> None:
        self.resourcetype = resourceType
        self.alive = True
        Sphere.__init__(self, pos, resourceType.radius_mass_ratio * mass, velocity, mass)
    
    def digest(self):
        self.alive = False

    def as_bytes(self) -> bytes:
        return merge(self.resourcetype.as_bytes(), Sphere.as_bytes(self))