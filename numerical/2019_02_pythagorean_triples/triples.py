from itertools import count
from math import sqrt
import numpy as np


def naive_triples(up_to=20):
    for a in range(1, up_to):
        for b in range(a, up_to):
            for c in range(b, up_to):
                if a*a + b*b == c*c:
                    yield (a, b, c)


def fibonacci_triples():
    odd_ints = []
    for idx, odd in enumerate(count(start=1, step=2)):
        odd_ints.append(odd)

        if int(odd**0.5)**2 == int(odd) and len(odd_ints) >= 4:
            n = (odd + 1) / 2
            b2 = sum(odd_ints[:-1])
            c2 = sum(odd_ints)
            yield tuple(map(int, (sqrt(odd), sqrt(b2), sqrt(c2))))


A = np.array([
    [1, -2, 2],
    [2, -1, 2],
    [2, -2, 3]
])

B = np.array([
    [1, 2, 2],
    [2, 1, 2],
    [2, 2, 3]
])

C = np.array([
    [-1, 2, 2],
    [-2, 1, 2],
    [-2, 2, 3]
])


def barning_triples(start=(3, 4, 5)):
    last_a = last_b = last_c = np.array(start)
    while True:
        last_a = A @ last_a
        yield last_a

        last_b = B @ last_b
        yield last_b

        last_c = C @ last_c
        yield last_c


if __name__ == '__main__':
    for x in naive_triples(up_to=20):
        print(x)

    fib = fibonacci_triples()
    for x in range(10):
        r = next(fib)
        print(r, r[0]*r[0] + r[1]*r[1] == r[2]*r[2])

    barn = barning_triples()
    for x in range(10):
        print(next(barn))
