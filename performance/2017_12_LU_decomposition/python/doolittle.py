
import numpy as np


def lu_decomp(x):
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
