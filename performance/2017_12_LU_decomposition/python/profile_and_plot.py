
import time

import matplotlib.pyplot as plt
from numba import jit
import numpy as np
import pandas as pd

from doolittle import lu_decomp

np.random.seed(0)

# Generate raw python data
raw_data = []
for n in (100, 200, 300, 400, 500, 600):
    data = np.random.random((n, n))
    start = time.time()
    lower, upper = lu_decomp(data)
    end = time.time()
    elapsed = float(str(end-start)[:8])
    print(f'Raw: {n}: {elapsed}')
    raw_data.append((n, elapsed))

raw_results = np.array(raw_data)
raw_df = pd.DataFrame(raw_results, columns=['idx', 'vals']).set_index('idx')

jit_lu = jit(lu_decomp)
jit_lu(np.random.random((100, 100)))

# Generate jitted function data
jit_data = []
for n in (100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000):
    data = np.random.random((n, n))
    start = time.time()
    lower, upper = jit_lu(data)
    end = time.time()
    elapsed = float(str(end-start)[:8])
    print(f'Jit: {n}: {elapsed}')
    jit_data.append((n, elapsed))

jit_results = np.array(jit_data)
jit_df = pd.DataFrame(jit_results, columns=['idx', 'vals']).set_index('idx')

# Plot everything
plt.loglog(raw_df, label='Doolittle, Python')
plt.loglog(jit_df, label='Doolittle, Numba')
plt.xlabel('Length of array axis (n)')
plt.ylabel('Calculation time (s)')
plt.legend()
plt.show()