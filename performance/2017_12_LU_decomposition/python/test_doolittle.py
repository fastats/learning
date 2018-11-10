
from numba import jit
import numpy as np
from numpy.testing import assert_array_almost_equal

from doolittle import lu_decomp


def test_doolittle_geeks_for_geeks():
    """
    This example is taken from the geeks for geeks
    website:
    https://www.geeksforgeeks.org/doolittle-algorithm-lu-decomposition/
    """
    arr = np.array([
        [2, -1, -2],
        [-4, 6, 3],
        [-4, -2, 8]
    ])

    lower, upper = lu_decomp(arr)

    # basic sanity
    final = lower @ upper
    assert_array_almost_equal(final, arr)

    expected_lower = np.array([
        [ 1.,  0.,  0.],
        [-2.,  1.,  0.],
        [-2., -1.,  1.],
    ])
    assert_array_almost_equal(expected_lower, lower)

    expected_upper = np.array([
        [2., -1., -2.],
        [0.,  4., -1.],
        [0.,  0.,  3.]
    ])
    assert_array_almost_equal(upper, expected_upper)


def test_doolittle_chapter_7():
    """ This example comes from the PDF of chapter 7:
        www.math.iit.edu/~fass/477577_Chapter_7.pdf

        also found in lu_decomp/literature
    """
    arr = np.array([
        [1, 1, 1],
        [2, 3, 5],
        [4, 6, 8]
    ])

    lower, upper = lu_decomp(arr)

    assert_array_almost_equal(lower @ upper, arr)

    expected_lower = np.array([
        [1, 0, 0],
        [2, 1, 0],
        [4, 2, 1]
    ])

    assert_array_almost_equal(expected_lower, lower)

    expected_upper = np.array([
        [1, 1, 1],
        [0, 1, 3],
        [0, 0, -2]
    ])

    assert_array_almost_equal(expected_upper, upper)


def test_doolittle_ust_hk():
    """ This is the example from Ch06 UST HK:
        https://www.math.ust.hk/~mamu/courses/231/Slides/CH06_5A.pdf

        also in literature/CH06_5A.pdf
    """
    arr = np.array([
        [1, 1, 0, 3],
        [2, 1, -1, 1],
        [3, -1, -1, 2],
        [-1, 2, 3 , -1]
    ])

    lower, upper = lu_decomp(arr)

    assert_array_almost_equal(lower @ upper, arr)

    expected_lower = np.array([
        [1, 0, 0, 0],
        [2, 1, 0, 0],
        [3, 4, 1, 0],
        [-1, -3, 0, 1]
    ])

    assert_array_almost_equal(expected_lower, lower)

    expected_upper = np.array([
        [1, 1, 0, 3],
        [0, -1, -1, -5],
        [0, 0, 3, 13],
        [0, 0, 0, -13]
    ])

    assert_array_almost_equal(expected_upper, upper)


def test_lu_decomp_heavy():
    arr = np.random.random((500, 500))
    lower, upper = jit(lu_decomp)(arr)
    assert_array_almost_equal(lower @ upper, arr)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
