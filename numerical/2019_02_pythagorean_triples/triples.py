from itertools import count
from math import sqrt

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




if __name__ == '__main__':
    # for x in naive_triples(up_to=20):
    #     print(x)

    fib = fibonacci_triples()
    for x in range(10):
        r = next(fib)
        print(r, r[0]*r[0] + r[1]*r[1] == r[2]*r[2])

