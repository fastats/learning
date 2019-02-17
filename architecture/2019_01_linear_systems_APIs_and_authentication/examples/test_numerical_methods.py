import numpy as np
import pytest
from hypothesis import given
from hypothesis.strategies import integers, tuples, floats
from hypothesis.extra.numpy import arrays
from numerical_methods import row_interchange, scalar_multiplication, add_scalar_mult


# For the sake of simplicity, not bothering with nans or infs.
reasonable_floats = floats(min_value=0.001, max_value=10 * 7, allow_nan=False, allow_infinity=False)
reasonable_f_array = arrays(
    dtype=np.float64,
    shape=tuples(integers(min_value=2, max_value=250), integers(min_value=2, max_value=250)),
    elements=reasonable_floats
)


@given(reasonable_f_array)
def test_row_interchange(arr):
    num_rows = arr.shape[0]
    index_one = np.random.randint(0, num_rows)
    index_two = np.random.randint(0, num_rows)

    res = row_interchange(arr, index_one, index_two)

    # Confirm the arrays have been changed
    np.testing.assert_array_equal(arr[index_one], res[index_two])
    np.testing.assert_array_equal(res[index_one], arr[index_two])

    # If we swap the rows back, arrays should be perfectly equal
    res[[index_one, index_two]] = res[[index_two, index_one]]
    np.testing.assert_array_equal(res, arr)


@given(reasonable_f_array, reasonable_floats)
def test_scalar_multiplication(arr, multiplier):
    row_to_mult = np.random.randint(0, arr.shape[0])

    res = scalar_multiplication(arr, row_to_mult, multiplier)

    # We would expect that row_to_mult would be arr[row_to_mult] * multiplier
    np.testing.assert_array_equal(arr[row_to_mult] * multiplier, res[row_to_mult])

    # And if we scale it back down, we'd expect the arrays to be the same.
    res[row_to_mult] /= multiplier
    # almost_equal needed due to potential imprecision on the way back
    np.testing.assert_array_almost_equal(arr, res)


@given(reasonable_f_array, reasonable_floats)
def test_add_scalar_mult(arr, multiplier):
    row_to_mult = np.random.randint(0, arr.shape[0])
    row_to_add = np.random.randint(0, arr.shape[0])

    res = add_scalar_mult(arr, row_to_mult, multiplier, row_to_add)

    # We would expect that row_to_add would be row_to_add + (row_to_mult * multiplier)
    np.testing.assert_array_equal(arr[row_to_add] + (arr[row_to_mult] * multiplier), res[row_to_add])

    # And if we scale it back down, we'd expect the arrays to be the same.
    res[row_to_add] -= arr[row_to_mult] * multiplier
    # almost_equal needed due to potential imprecision on the way back
    np.testing.assert_array_almost_equal(arr, res)


if __name__ == '__main__':
    pytest.main([__file__, '-s'])
