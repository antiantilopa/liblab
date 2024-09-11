from .vmath import Vector2d

def abs(x):
    if x < 0:
        return -x
    return x

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
    
    def collide(self, spheres: list["Sphere"]):
        nvelocity = self.velocity
        if self.rigit:
            for sphere in spheres:
                if self.id < sphere.id and sphere.rigit:
                    center_line = self.pos - sphere.pos
                    central_line_norm = center_line.norm()
                    radius_sum = self.radius + sphere.radius
                    if not center_line.isInBox(Vector2d(-radius_sum, -radius_sum), Vector2d(radius_sum, radius_sum)):
                        continue
                    if center_line.lenght() > radius_sum:
                        continue
                    # print("Collide!")
                    if self.mass > 0:
                        nvelocity = (central_line_norm * (-nvelocity.dotMultiply(central_line_norm)) + nvelocity) + (central_line_norm * (abs(sphere.velocity.dotMultiply(central_line_norm)) * sphere.mass / self.mass))
                    if sphere.mass > 0:
                        sphere.velocity = (central_line_norm * (-sphere.velocity.dotMultiply(central_line_norm)) + sphere.velocity) + (central_line_norm * (-abs(self.velocity.dotMultiply(central_line_norm))) * self.mass / sphere.mass)
                    self.collisions.add(sphere)
                    sphere.collisions.add(self)
            self.velocity = nvelocity
    
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
        print(q1, q2)
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
