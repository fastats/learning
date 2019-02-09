import numpy as np
from pytest import approx, mark
from scipy.special import logsumexp

from .log_sum_exp import streaming_stable_log_sum_exp, stable_log_sum_exp


@mark.parametrize('n', np.logspace(0, 6, 7).astype(np.int64), ids='n={0:,}'.format)
def test_log_sum_exp_basic(n):
    rng = np.random.RandomState(0)
    data = rng.randn(n)

    # sanity
    expected = np.log(np.sum(np.exp(data)))
    expected_scipy = logsumexp(data)
    assert expected_scipy == approx(expected)

    # not streaming
    got = stable_log_sum_exp(data)
    assert expected_scipy == approx(got)

    # streaming
    got = streaming_stable_log_sum_exp(data)
    assert expected == approx(got)


def test_stability():
    rng = np.random.RandomState(0)
    data = rng.randn(10_000_000) * 500

    # this is not numerically stable
    got = np.log(np.sum(np.exp(data)))
    assert got == np.inf

    # these guys are
    got = logsumexp(data)
    assert got == approx(2545.277321558401)

    got = streaming_stable_log_sum_exp(data)
    assert got == approx(2545.277321558401)

    got = stable_log_sum_exp(data)
    assert got == approx(2545.277321558401)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
