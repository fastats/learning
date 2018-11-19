
from numba import njit
import numpy as np
import time


@njit
def lu_decomp_original(x):
    """ `x` must be a N x N matrix which is decomposable
        into lower and upper triangular sections.

        :param x: The array to factorise into lower and upper
        :type x: (int_array|float_array), square

        :rtype: tuple, lu_sanity(lower @ upper == input)
    """
    assert not np.any(np.isnan(x)), "NaN values not allowed"

    lower = np.zeros_like(x)
    upper = np.zeros_like(x)

    n = len(x)

    for i in range(n):
        for k in range(i, n):
            total = 0.0
            for j in range(i):
                total += lower[i][j] * upper[j][k]

            upper[i][k] = x[i][k] - total

        for k in range(i, n):
            if i == k:
                lower[i][i] = 1.0
            else:
                total = 0.0
                for j in range(i):
                    total += lower[k][j] * upper[j][i]

                lower[k][i] = (x[k][i] - total) / upper[i][i]

    return lower, upper


@njit
def lu_decomp_c_fortran(x):
    """ We notice that the upper matrix is always being accessed
    in the "wrong" order, relative to the optimal way to lay out
    nested loops for cache/register hits.
    
    This can't easily be changed due to the specifics of the 
    algorithm, so we cheat. We set up the upper matrix in Fortran 
    order. This makes it the "right" way round for cache hits, 
    leading to a much faster algorithm.
    
    However this might come back to bite us - the returned upper
    matrix might be slower to multiply with other arrays in the
    future as a result of its ordering.
    """
    assert not np.any(np.isnan(x)), "NaN values not allowed"

    lower = np.zeros_like(x)
    upper = np.asfortranarray(np.zeros_like(x))  # only this line changes!

    n = len(x)

    for i in range(n):
        for k in range(i, n):
            total = 0.0
            for j in range(i):
                total += lower[i][j] * upper[j][k]

            upper[i][k] = x[i][k] - total

        for k in range(i, n):
            if i == k:
                lower[i][i] = 1.0
            else:
                total = 0.0
                for j in range(i):
                    total += lower[k][j] * upper[j][i]

                lower[k][i] = (x[k][i] - total) / upper[i][i]

    return lower, upper




if __name__ == '__main__':
    n = 1024
    X = np.random.uniform(size=(n, n))

    for i in range(2):
        t1 = time.process_time()
        l, u = lu_decomp_original(X)
        t2 = time.process_time()
        print('Naive took:   ', t2 - t1)

        t1 = time.process_time()
        l2, u2 = lu_decomp_c_fortran(X)
        t2 = time.process_time()
        np.testing.assert_allclose(l, l2)
        print('Adjusted took:', t2 - t1)
        print('------------')


