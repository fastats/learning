
import numpy as np
from numba import jit


@jit(nopython=True, nogil=True)
def lu(A, L, U):
    size = len(A)

    for i in range(size):
        for k in range(size):
            total = np.sum(L[i, 0:i] * U[0:i, k])
            U[i, k] = A[i, k] - total

        for k in range(size):
            if i == k:
                L[i, i] = 1.0
            else:
                total = np.sum(L[k, 0:i] * U[0:i, i])
                L[k, i] = (A[k, i] - total) / U[i, i]


if __name__ == '__main__':
    A = np.array([
        [1, 2, 4],
        [3, 8, 14],
        [2, 6, 13]
    ])

    L, U = np.zeros_like(A), np.zeros_like(A)

    lu(A, L, U)

    expected_L = [
        [1, 0, 0],
        [3, 1, 0],
        [2, 1, 1]
    ]
    expected_U = [
        [1, 2, 4],
        [0, 2, 2],
        [0, 0, 3]
    ]
    assert L.tolist() == expected_L
    assert U.tolist() == expected_U
    print('Correct')
