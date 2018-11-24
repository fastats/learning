
import numpy as np
from numba import njit, prange, config


# config.THREADING_LAYER = 'tbb'
# to use this, first do: conda install tbb


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
    assert A.shape[0] == A.shape[1]

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
    assert A.shape[0] == A.shape[1]

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


def lu_3(A):
    assert A.shape[0] == A.shape[1]

    n = A.shape[0]
    U = A.astype(np.float64)
    L = np.eye(n)
    for i in range(1, n):
        for j in range(i):
            L[i, j] = U[i, j] / U[j, j]
            for k in range(j, n):
                U[i, k] -= L[i, j] * U[j, k]
    return L, U


def lu_4(A):
    assert A.shape[0] == A.shape[1]

    n = A.shape[0]
    U = A.astype(np.float64)
    L = np.eye(n)
    for i in range(1, n):
        for j in range(i):
            L[i, j] = U[i, j] / U[j, j]
            U[i, :] -= L[i, j] * U[j, :]
    return L, U


def lu_5(A):
    assert A.shape[0] == A.shape[1]

    A = A.astype(np.float64)
    n = A.shape[0]

    for k in range(n - 1):
        A[k + 1: n, k] /= A[k, k]
        A[k + 1: n, k + 1: n] -= np.outer(A[k + 1: n, k], A[k, k + 1: n])

    lower = np.tril(A, k=-1)
    np.fill_diagonal(lower, 1)

    upper = np.triu(A, k=0)

    return lower, upper


@njit(parallel=True)
def lu_parallel(x):
    upper = np.zeros_like(x)
    n = len(x)
    lower = np.eye(n)

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


@njit(parallel=True)
def lu_parallel_2(x):
    upper = np.asfortranarray(np.zeros_like(x).astype(np.float64))
    n = len(x)
    lower = np.ascontiguousarray(np.eye(n).astype(np.float64))

    for i in range(n):
        lower[i][i] = 1.0

        for k in prange(i, n):
            total = lower[i, :] @ upper[:, k]
            upper[i][k] = x[i][k] - total

        for k in prange(i + 1, n):
            total = lower[k, :] @ upper[:, i]
            lower[k][i] = (x[k][i] - total) / upper[i][i]

    return lower, upper

