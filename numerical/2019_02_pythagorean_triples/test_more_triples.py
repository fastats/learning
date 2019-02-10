from pytest import mark

from more_triples import (
    py_triples_stifel, py_triples_ozanam,
    py_triples_fibonacci, take,
    py_triples_stifel_ozanam
)

ALL_FNS = [
    py_triples_stifel, py_triples_ozanam,
    py_triples_fibonacci
]


def check(gen, first_n=100):
    for a, b, c in take(first_n, gen):
        assert a**2 + b**2 == c**2


@mark.parametrize('fn', ALL_FNS, ids=lambda x: f'{x.__name__}')
def test_py_triple(fn):
    gen = fn()
    check(gen)


def test_py_triples_fused_stifel_ozanam():
    gen = py_triples_stifel_ozanam()
    check(gen)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
