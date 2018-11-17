
import numpy as np
from numba import njit, prange


def lu_0(A):

    assert A.shape[0] == A.shape[1]

    U = A.astype(np.float64)
    n = A.shape[0]
    L = np.eye(n).astype(np.float64)

    for k in range(n - 1):
        u_k_k = U[k, k]
        u_k_kn = U[k, k:n]
        for j in range(k + 1, n):
            L[j, k] = U[j, k] / u_k_k
            U[j, k:n] -= L[j, k] * u_k_kn

    return L, U


def lu_1(A):
    A = A.astype(np.float64)
    n = A.shape[0]

    for k in range(n - 1):
        for i in range(k + 1, n):
            lambda_ = A[i, k] / A[k, k]
            A[i, k + 1: n] -= lambda_ * A[k, k + 1: n]
            A[i, k] = lambda_

    lower = np.tril(A, k=-1)
    np.fill_diagonal(lower, 1)

    upper = np.triu(A, k=0)

    return lower, upper


def lu_2(A):
    A = A.astype(np.float64)
    n = A.shape[0]

    for k in range(n - 1):
        a_k_k = A[k, k]
        a_k_k1_n = A[k, k + 1: n]

        for i in range(k + 1, n):
            lambda_ = A[i, k] / a_k_k
            A[i, k + 1: n] -= lambda_ * a_k_k1_n
            A[i, k] = lambda_

    lower = np.tril(A, k=-1)
    np.fill_diagonal(lower, 1)

    upper = np.triu(A, k=0)

    return lower, upper


@njit(parallel=True)
def lu_parallel(x):

    lower = np.zeros_like(x)
    upper = np.zeros_like(x)

    n = len(x)

    for i in range(n):
        lower[i][i] = 1.0

        for k in prange(i, n):
            total = 0.0
            for j in range(i):
                total += lower[i][j] * upper[j][k]

            upper[i][k] = x[i][k] - total

        for k in prange(i + 1, n):
            total = 0.0
            for j in range(i):
                total += lower[k][j] * upper[j][i]

            lower[k][i] = (x[k][i] - total) / upper[i][i]

    return lower, upper
