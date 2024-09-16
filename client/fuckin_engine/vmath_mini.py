from math import pi, sqrt, sin, cos, atan2
from typing import Callable


class Vector2d:
    """
    Class to represent a pair of floats.
    """

    x: float
    y: float

    def __init__(self, a: float = 0, b: float = 0):
        self.x = a
        self.y = b

    @staticmethod
    def from_tuple(tpl: tuple[float, float]) -> "Vector2d":
        return Vector2d(tpl[0], tpl[1])

    def as_tuple(self) -> tuple[float, float]:
        return self.x, self.y

    def distance(self, other: "Vector2d") -> float:
        return sqrt(((self.x - other.x) ** 2) + ((self.y - other.y) ** 2))

    def lenght(self) -> float:
        return sqrt((self.x ** 2) + (self.y ** 2))

    def intx(self) -> int:
        return int(self.x)

    def inty(self) -> int:
        return int(self.y)
    
    def norm(self) -> "Vector2d":
        l = self.lenght()
        if l == 0:
            return Vector2d(0, 0)
        return Vector2d(self.x / l, self.y / l)

    def distanceLooped(self, other: "Vector2d", size: "Vector2d") -> float:
        return sqrt(((self.x - other.x + size.x / 2) % size.x - (size.x / 2)) ** 2 + ((self.y - other.y + size.y / 2) % size.y - (size.y / 2)) ** 2)

    def as_bytes(self) -> bytes:
        return to_bytes(self.as_tuple())
    
    def fast_reach_test(self, other: "Vector2d", mapSize: "Vector2d", dist: float|int) -> bool:
        divercity = ((other - self + (mapSize / 2)) % mapSize.x - (mapSize / 2))
        if not (-dist <= divercity.x <= dist and -dist <= divercity.y <= dist):
            return False
        if self.distanceLooped(other, mapSize) > dist:
            return False
        return True

    def getQuarter(self) -> int:
        if self.x == 0 and self.y == 0:
            return 1
        if self.x >= 0 and self.y >= 0:
            return 1
        elif self.x <= 0 and self.y <= 0:
            return 3
        elif self.x < 0:
            return 2
        elif self.y < 0:
            return 4

    def isInBox(self, other1: "Vector2d", other2: "Vector2d") -> bool:
        x1, y1 = other1.x, other1.y
        x2, y2 = other2.x, other2.y
        x1, x2 = (min(x1, x2), max(x1, x2))
        y1, y2 = (min(y1, y2), max(y1, y2))
        return (x1 <= self.x and self.x <= x2 and y1 <= self.y and self.y <= y2)

    def get_squeezed(self, min_values: "Vector2d", max_values: "Vector2d") -> "Vector2d":
        return Vector2d(min(max(self.x, min_values.x), max_values.x),min(max(self.y, min_values.y), max_values.y))

    @staticmethod
    def from_bytes(x: bytes) -> "Vector2d":
        return Vector2d.from_tuple(tuple(from_bytes(x)))
    
    def __add__(self, other: "Vector2d") -> "Vector2d":
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2d") -> "Vector2d":
        return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other: "float|Vector2d") -> "Vector2d":
        if type(other) == Vector2d:
            return Vector2d(self.x * other.x, self.y * other.y)
        else:
            return Vector2d(self.x * other, self.y * other)
    
    def complexMultiply(self, other: "Vector2d") -> "Vector2d":
        # complex multiplying
        return Vector2d(self.x * other.x - self.y * other.y, self.y * other.x + self.x * other.y)

    def dotMultiply(self, other: "Vector2d") -> float:
        return self.x * other.x + self.y * other.y

    def __truediv__(self, other: float) -> "Vector2d":
        return Vector2d(self.x / other, self.y / other)

    def __floordiv__(self, other: float) -> "Vector2d":
        return Vector2d(self.x // other, self.y // other)
    
    def __mod__(self, other: float) -> "Vector2d":
        return Vector2d(self.x % other, self.y % other)

    def operation(self, other: "Vector2d", operation: Callable[[float, float], float]) -> "Vector2d":
        return Vector2d(operation(self.x, other.x), operation(self.y, other.y))

    def __repr__(self) -> str:  # for debugging
        return f"<{self.x}, {self.y}>"

    def __eq__(self, other: "Vector2d") -> bool:
        return (self.x == other.x and self.y == other.y)

    def __ne__(self, other: "Vector2d") -> bool:
        return (self.x != other.x or self.y != other.y)


def to_bytes(x) -> bytes:
    '''
    turns integers, floats into 4 length bytearray.\n
    float is rounded.\n
    lists are encoded badly
    '''
    if type(x) == int:
        res = bytearray(5)
        res[0] = 0
        for i in range(4):
            res[4-i] = (x // (256 ** i)) % 256
    elif type(x) == float:
        res = bytearray(5)
        res[0] = 1
        for i in range(4):
            res[4-i] = int((x // (256 ** (i - 2))) % 256)
    elif type(x) == bool:
        res = bytes((2, int(x)))
    elif type(x) in (bytes, bytearray):
        res = bytes((3, x[0]))
    elif type(x) in (tuple, list):
        res = bytearray(1)
        res[0] = 4
        for item in x:
            if type(item) in (int, float):
                res.extend(to_bytes(item))
            elif type(item) == bool:
                res.extend(to_bytes(item))
            elif type(item) in (tuple, list):
                ext = to_bytes(item)
                res.extend(ext)
            elif "as_bytes" in item.__dir__():
                ext = item.as_bytes()
                res.extend(ext)
            else:
                raise Exception(f"{type(item)}({item}) is not alowed")
        res.append(5)
    else:
        if "as_bytes" in x.__dir__():
            res = x.as_bytes()
        else:
            raise Exception(f"{type(x)}({x}) is not alowed")
    return bytes(res)

def from_bytes(x : bytes, is_initial: bool = True):
    if x[0] == 0:
        res = 0
        for i in range(4):
            res += x[4-i] * (256 ** i)
    elif x[0] == 1:
        res = 0
        for i in range(4):
            res += x[4-i] * (256 ** (i - 2))
    elif x[0] == 2:
        res = bool(x[1])
    elif x[0] == 3:
        res = x[1]
    elif x[0] == 4:
        res = []
        curr = 1
        while x[curr] != 5:
            if x[curr] in (0, 1):
                res.append(from_bytes(x[curr: curr + 5]))
                curr += 5
            elif x[curr] == 2:
                res.append(from_bytes(x[curr: curr + 2]))
                curr += 2
            elif x[curr] == 3:
                res.append(from_bytes(x[curr: curr + 2]))
                curr += 2
            elif x[curr] == 4:
                ext, length = from_bytes(x[curr:], False)
                res.append(ext)
                curr += length + 1
        if not is_initial:
            return (res, curr)
    else:
        raise Exception(f"{x[0]} type is not expected. expected (0, 1, 2, 3, 4) for int, float, bytes, bool, list respectively")
    
    return res

def merge(b1 :bytes, b2: bytes) -> bytes:
    b1 = bytearray(b1)
    b2 = bytearray(b2)
    if b1[0] == 4 and b2[0] == 4:
        b1.pop(-1)
        b1.extend(b2[1:-1])
        b1.append(5)
    elif b1[0] == 4:
        b1.pop(-1)
        b1.extend(b2)
        b1.append(5)
    elif b2[0] == 4:
        b1.insert(0, 4)
        b1.extend(b2[1:-1])
        b1.append(5)
    else:
        b1.insert(0, 4)
        b1.extend(b2)
        b1.append(5)
    return bytes(b1)

def print_bytes(b: bytes):
    for i in b:
        print(i, end = " ")
    print()

