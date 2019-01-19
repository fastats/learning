from numba import guvectorize
import numpy as np


@guvectorize(
    ['void(float64[:, :], int64, int64, float64[:, :], float64[:, :])'],
    '(x, y), (), (), (m, n)->(m, n)',
    target='cpu', nopython=True
)
def upper_inner(x, i, n, lower, upper):
    for k in range(i, n):
        total = 0.0
        for j in range(i):
            total += lower[i][j] * upper[j][k]

        upper[i][k] = x[i][k] - total


@guvectorize(
    ['void(float64[:, :], int64, int64, float64[:, :], float64[:, :])'],
    '(x, y), (), (), (m, n)->(m, n)',
    target='cpu', nopython=True
)
def lower_inner(x, i, n, lower, upper):
    for k in range(i + 1, n):
        total = 0.0
        for j in range(i):
            total += lower[k][j] * upper[j][i]

        lower[k][i] = (x[k][i] - total) / upper[i][i]


def lu_vectorized(x):
    upper = np.asfortranarray(np.zeros(x.shape, dtype=np.float64))
    n = len(x)
    lower = np.eye(len(x))

    for i in range(n):
        upper_inner(x, i, n, lower, upper)
        lower_inner(x, i, n, lower, upper)

    return lower, upper


# I don't think this is actually supposed to work, the signature
# says we're just 'returning' one new array, but both lower and
# upper are mutated?
@guvectorize(
    ['void(float64[:, :], float64[:, :], float64[:, :])'],
    '(x, y), (m, n)->(m, n)',
    target='cpu', nopython=True
)
def inner(x, lower, upper):
    n = len(x)
    for i in range(n):
        for k in range(i, n):
            total = 0.0
            for j in range(i):
                total += lower[i][j] * upper[j][k]

            upper[i][k] = x[i][k] - total

        for k in range(i + 1, n):
            total = 0.0
            for j in range(i):
                total += lower[k][j] * upper[j][i]

            lower[k][i] = (x[k][i] - total) / upper[i][i]


def lu_vectorized_experimental(x):
    upper = np.asfortranarray(np.zeros(x.shape, dtype=np.float64))
    lower = np.eye(len(x))

    inner(x, lower, upper)

    return lower, upper
