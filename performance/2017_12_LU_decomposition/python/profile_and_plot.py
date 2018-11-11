
import time

import matplotlib.pyplot as plt
from numba import njit
import numpy as np
from numpy.testing import assert_array_almost_equal
import pandas as pd
import numba

from doolittle import lu_decomp
from lu_smorgasbord import lu_0, lu_1, lu_2, lu_parallel


if __name__ == '__main__':
    np.random.seed(0)

    lu_decomp_python = lu_decomp

    def collect_results(fn, jit=True):
        if jit:
            sizes = (100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000)

            if not isinstance(fn, numba.targets.registry.CPUDispatcher):
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

    df = collect_results(lu_decomp_python, jit=False)
    plt.loglog(df, label=lu_decomp_python.__name__)

    # jitted functions
    for fn in lu_decomp, lu_0, lu_1, lu_2, lu_parallel:
        df = collect_results(fn)
        plt.loglog(df, label=fn.__name__)

    plt.xlabel('Length of array axis (n)')
    plt.ylabel('Calculation time (s)')
    plt.legend()
    plt.show()
