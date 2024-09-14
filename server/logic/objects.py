from .vmath import Vector2d

def abs(x):
    if x < 0:
        return -x
    return x

FRICTIOON_KOEFICIENT = 0.999
WORLD_SIZE = Vector2d(1800, 1000)

class Sphere:
    id: int
    counter = 0
    pos: Vector2d
    radius: int
    velocity: Vector2d
    mass: int
    rigit: bool
    collisions: set

    def __init__(self, pos: Vector2d, radius: int, velocity: Vector2d, mass: int) -> None:
        self.id = Sphere.counter
        Sphere.counter += 1
        self.pos = pos
        self.radius = radius
        self.velocity = velocity
        self.mass = mass
        self.rigit = True
        self.collisions = set()
    
    def set_rigit(self, rigit):
        self.rigit = rigit
    
    def flow(self):
        self.pos = self.pos + self.velocity
        if self.velocity != Vector2d(0, 0):
            self.velocity = self.velocity - self.velocity.norm() * self.velocity.dotMultiply(self.velocity) * (1 - FRICTIOON_KOEFICIENT)
    
    def collide(self, spheres: list["Sphere"]):
        nvelocity = self.velocity
        if self.rigit:
            for sphere in spheres:
                if self.id < sphere.id and sphere.rigit:
                    center_line = self.pos - sphere.pos
                    radius_sum = self.radius + sphere.radius
                    if not center_line.isInBox(Vector2d(-radius_sum, -radius_sum), Vector2d(radius_sum, radius_sum)):
                        continue
                    if center_line.lenght() > radius_sum:
                        continue
                    central_line_norm = center_line.norm()
                    if self.mass > 0:
                        nvelocity = (central_line_norm * (-nvelocity.dotMultiply(central_line_norm)) + nvelocity) + (central_line_norm * (abs(sphere.velocity.dotMultiply(central_line_norm)) * sphere.mass / self.mass))
                    if sphere.mass > 0:
                        sphere.velocity = (central_line_norm * (-sphere.velocity.dotMultiply(central_line_norm)) + sphere.velocity) + (central_line_norm * (-abs(self.velocity.dotMultiply(central_line_norm))) * self.mass / sphere.mass)
                    self.collisions.add(sphere)
                    sphere.collisions.add(self)
                    break
            self.velocity = nvelocity
    
    def collide_with(self, sphere: "Sphere"):
        center_line = self.pos - sphere.pos
        radius_sum = self.radius + sphere.radius
        if center_line.lenght() > radius_sum:
            return
        nvelocity = self.velocity
        central_line_norm = center_line.norm()
        if self.mass > 0:
            nvelocity = (central_line_norm * (-nvelocity.dotMultiply(central_line_norm)) + nvelocity) + (central_line_norm * (abs(sphere.velocity.dotMultiply(central_line_norm)) * sphere.mass / self.mass))
        if sphere.mass > 0:
            sphere.velocity = (central_line_norm * (-sphere.velocity.dotMultiply(central_line_norm)) + sphere.velocity) + (central_line_norm * (-abs(self.velocity.dotMultiply(central_line_norm))) * self.mass / sphere.mass)
        self.velocity = nvelocity
        self.collisions.add(sphere)
        sphere.collisions.add(self)
        
    @staticmethod
    def multicollisions(spheres: list["Sphere"]):
        # sweep and prune algorithm
        # there is better, but i do not like trees
        x_lefts_coords_rel: list[int] = []
        spheres_rel: list[int] = [i for i in range(len(spheres))]
        x_coords: list[int] = []
        for i in range(len(spheres)):
            x_lefts_coords_rel.append(spheres[i].pos.x - spheres[i].radius)
            x_coords.append(spheres[i].pos.x - spheres[i].radius)
        x_coords.sort()
        active: list[int] = []
        pairs: list[tuple[int]] = []
        for i in range(len(spheres)):
            sp = spheres_rel[x_lefts_coords_rel.index(x_coords[i])]
            for j in active:
                if spheres[sp].pos.x - spheres[j].pos.x >= spheres[sp].radius + spheres[j].radius:
                    active.remove(j)
                else:
                    pairs.append((min(j, sp), max(j, sp)))
            active.append(sp)
            x_lefts_coords_rel.remove(x_coords[i])
            spheres_rel.remove(sp)
        
        for pair in pairs:
            if -(spheres[pair[0]].radius + spheres[pair[1]].radius) < spheres[pair[0]].pos.y - spheres[pair[1]].pos.y < spheres[pair[0]].radius + spheres[pair[1]].radius:
                spheres[pair[0]].collide_with(spheres[pair[1]])

    def collision_proceeding(self):
        self.clear_colisions()

    
    def touches(self, pos: Vector2d) -> bool:
        center_line = self.pos - pos
        radius_sum = self.radius
        if center_line.isInBox(Vector2d(-radius_sum, -radius_sum), Vector2d(radius_sum, radius_sum)):
            if center_line.lenght() <= radius_sum:
                return True
        return False

    def borders(self, pos: Vector2d, size: Vector2d):
        if self.pos.isInBox(pos + Vector2d(self.radius, self.radius), pos + size - Vector2d(self.radius, self.radius)):
            return
        q1 = (self.pos - pos - Vector2d(self.radius, self.radius)).getQuarter()
        q2 = (self.pos - pos - size + Vector2d(self.radius, self.radius)).getQuarter()
        if q1 == 4:
            self.velocity.y = -self.velocity.y
            self.pos.y = pos.y + self.radius
        elif q1 == 3:
            self.velocity = self.velocity * -1
            self.pos.y = pos.y + self.radius
            self.pos.x = pos.x + self.radius
        elif q1 == 2:
            self.velocity.x = -self.velocity.x
            self.pos.x = pos.x + self.radius
        if q2 == 4:
            self.velocity.x = -self.velocity.x
            self.pos.x = pos.x + size.x - self.radius
        elif q2 == 2:
            self.velocity.y = -self.velocity.y
            self.pos.y = pos.y + size.y - self.radius
        elif q2 == 1:
            self.velocity = self.velocity * -1
            self.pos.x = pos.x + size.x - self.radius
            self.pos.y = pos.y + size.y - self.radius
    
    def clear_colisions(self):
        self.collisions = set()
    
    def iteration(self):
        self.flow()
        self.borders(Vector2d(0, 0), WORLD_SIZE)
        self.collision_proceeding()
