import multiprocessing
from multiprocessing import Pool
import time

class A:
    def __init__(self) -> None:
        self.y = [0]

def calc(args):
    x = args[0]
    a = args[1]
    fact = 1
    for i in range(1, x + 1):
        fact *= i
        fact %= (1000000007)
    a.y.append(fact)
    return (fact, a)

if __name__ == "__main__":
    a = A()
    start_time = time.time()
    with Pool(10) as p:
        b = p.map(calc, [(10000000, a)]*7)
    for i in b:
        print(i[1].y)
    print("Calculated in", time.time() - start_time)
    print(a.y)

    # start_time = time.time()
    # calc(10000000)
    # calc(10000000)
    # calc(10000000)
    # calc(10000000)
    # calc(10000000)
    # calc(10000000)
    # calc(10000000)
    # print("Calculated in", time.time() - start_time)