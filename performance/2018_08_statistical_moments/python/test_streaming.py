
import numpy as np
import pandas as pd
from pytest import mark

from .streaming import streaming_all_stats, naive_all_stats

TWO_YEARS = 365 * 2
ASSETS = ['A', 'B', 'C', 'D', 'E']


def make_df(data, label):
    return pd.DataFrame(data.reshape(TWO_YEARS, len(ASSETS)), columns=ASSETS), label


def sample_returns():
    n = len(ASSETS)
    rng = np.random.RandomState(0)

    data = rng.randn(TWO_YEARS * n) / 10
    yield make_df(data, 'normal')

    data = rng.randn(TWO_YEARS * n) * 1e12
    yield make_df(data, 'normal very large')

    data = rng.randn(TWO_YEARS * n) * 1e-12
    yield make_df(data, 'normal very small')

    data = rng.lognormal(0.1, 0.2, TWO_YEARS * n) / 10
    yield make_df(data, 'lognormal')

    data = rng.standard_gamma(2, TWO_YEARS * n) / 100
    yield make_df(data, 'gamma')


@mark.parametrize('data', sample_returns(), ids=lambda x: x[1])
def test_streaming_all(data):
    expected = naive_all_stats(data[0])
    got = streaming_all_stats(data[0])

    assert expected.keys() == got.keys()

    for k, v in expected.items():
        if k != 'skewness':
            np.testing.assert_allclose(v, got[k], equal_nan=True)
        else:
            np.testing.assert_allclose(v, got[k], equal_nan=True, atol=1e-9)
            # difference is retained precision vs scipy...


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
