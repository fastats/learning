
import numpy as np
from numpy import sum as nsum, power, std
from scipy import stats
from pytest import approx


def moment(data, order=1):
    x_bar = nsum(data) / len(data)
    x_i = power(data - x_bar, order)
    return nsum(x_i) / len(data)


def test_moment():
    x = np.random.random(1000)

    moments = ['zeroth', 'mean', 'var', 'skew', 'kurt']
    for i, m in enumerate(moments):
        calc = moment(x, order=i)
        lib = stats.moment(x, moment=i)
        assert calc == approx(lib), m + ' failed'
