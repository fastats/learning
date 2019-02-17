import numpy as np


def row_interchange(arr: np.ndarray, index_one: int, index_two: int):
    res = arr.copy()
    res[[index_one, index_two]] = res[[index_two, index_one]]
    return res


def scalar_multiplication(
    arr: np.ndarray,
    mult_index: int,
    multiply_by: np.float64
):
    res = arr.copy()
    res[mult_index] *= multiply_by
    return res


def add_scalar_mult(
    arr: np.ndarray,
    mult_index: int,
    multiply_by: np.float64,
    add_index: int
):
    res = arr.copy()
    res[add_index] += res[mult_index] * multiply_by
    return res
