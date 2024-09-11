class A:
    def __init__(self, x) -> None:
        self.x = x
    def __repr__(self) -> str:
        return str(self.x)

a = (4, 5, 6)

b = {1, 2, 3}

c = {
    "a": 1,
    "b": 2,
    "c": 3
}
for i in c:
    print(i)