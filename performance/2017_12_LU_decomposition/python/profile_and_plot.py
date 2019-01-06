
import time

import matplotlib.pyplot as plt
from numba import njit
import numpy as np
from numpy.testing import assert_array_almost_equal
import pandas as pd
import numba

from doolittle import lu_decomp
from lu_smorgasbord import (
    lu_0, lu_1, lu_2, lu_3, lu_4, lu_5,
    lu_parallel, lu_parallel_2
)
from lu_c_fortran import lu_decomp_c_fortran
from lu_vectorized import lu_vectorized, lu_vectorized_experimental

if __name__ == '__main__':
    np.random.seed(0)

    lu_decomp_python = lu_decomp

    def collect_results(fn, fast=True, should_jit=True):
        if fast:
            sizes = (100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000)

            if should_jit and not isinstance(fn, numba.targets.registry.CPUDispatcher):
                fn = njit(fn)

            fn(np.random.random((10, 10)))  # force compile
        else:
            sizes = (100, 200, 300, 400, 500, 600)

        raw_data = []
        for n in sizes:
            data = np.random.random((n, n))
            start = time.time()
            lower, upper = fn(data)
            end = time.time()
            elapsed = float(str(end - start)[:8])
            print(f'{fn.__name__}: {n}: {elapsed}')
            raw_data.append((n, elapsed))

            # sanity check
            assert_array_almost_equal(lower @ upper, data)

        raw_results = np.array(raw_data)
        raw_df = pd.DataFrame(raw_results, columns=['idx', 'vals']).set_index('idx')
        return raw_df

    df = collect_results(lu_decomp_python, fast=False, should_jit=False)
    plt.loglog(df, label=lu_decomp_python.__name__)

    # jitted functions
    fns = [lu_decomp, lu_decomp_c_fortran, lu_0, lu_1, lu_2,
           lu_3, lu_4, lu_5, lu_parallel, lu_parallel_2]

    for fn in fns:
        plt.loglog(collect_results(fn), label=fn.__name__)

    # We don't want to jit our vectorized functions, as calling guvectorized
    # functions from a jitted function is troublesome and not currently well supported
    for fn in [lu_vectorized, lu_vectorized_experimental]:
        plt.loglog(collect_results(fn, should_jit=False), label=fn.__name__)

    plt.xlabel('Length of array axis (n)')
    plt.ylabel('Calculation time (s)')
    plt.legend()
    plt.show()
