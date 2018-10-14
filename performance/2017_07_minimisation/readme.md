
# Minimisation

*18th July 2017*, by Dave Willmer

In the [last lesson](../2017_06_performance_basics) we saw optimisations to
improve performance relating to memory bandwidth (RAM optimisation), as well as CPU cache and CPU register
optimisations using Matrix-Matrix multiplication (MMM) as the learning vehicle.

In this lesson we will build on the concepts from the previous lesson by
using MMM to build a working version of the Simplex method for minimising
an objective function.

- We will start by learning about `numba`, the numerical
JIT compiler for python, which hugely improves our edit-test cycle compared
with assembly/C code.
- We will then implement the naive MMM in numba,
write a Simplex minimisation routine, and then optimise it.

### Numba

[Numba](https://www.numba.org) is a project from [Continuum Analytics](https://continuum.io)
which converts numerical python code into native code using a Just-In-Time
compiler (JIT).

You can use numba by adding the `@jit` decorator to a function which takes
numpy objects or scalars as arguments:

```python
from numba import jit

@jit
def add_five(x):
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            x[i, j] += 5
```

The first time this function is called, `numba` will work out whether the
types are consistent, and if so will generate native code using LLVM.
