
# ref:
# https://en.wikipedia.org/wiki/Formulas_for_generating_Pythagorean_triples

from itertools import islice
from heapq import merge

from numba import njit


def take(n, iterable):
    return list(islice(iterable, n))


@njit
def py_triples_stifel():
    n = 1

    while True:
        denom = n * 2 + 1
        improper_numerator = n * (denom + 1)

        yield denom, improper_numerator, improper_numerator + 1

        n += 1


@njit
def py_triples_ozanam():
    n = 1

    while True:
        denom = 4 * (n + 1)
        improper_numerator = denom * (1 + n) - 1

        yield denom, improper_numerator, improper_numerator + 2

        n += 1


def py_triples_stifel_ozanam():
    # all primitive triples of the Plato and Pythagoras families
    return merge(py_triples_stifel(), py_triples_ozanam())


@njit
def py_triples_fibonacci():
    k = 3

    while True:
        c_2 = k ** 2
        n = (c_2 + 1) >> 1

        yield k, (n - 1), n

        k += 2
