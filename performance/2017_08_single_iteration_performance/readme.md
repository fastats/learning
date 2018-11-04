# Single Iteration Performance

*6th August 2017*, by Dave Willmer

In the [previous](../2017_06_performance_basics) [two](../2017_07_minimisation) lessons, we have looked at improving performance
when iterating over 2-dimensional arrays. These techniques can be applied
to any algorithms over 2 or more dimensions, as they mainly concern re-using
data in CPU caches.

However, a number of algorithms would *not* benefit from these techniques
because we only iterate once, and therefore never re-use any previous
cached values.

In this lesson we will look at improving the performance of a loop which
only iterates over an array once.

We will also **not** be using threads - best practice is to concentrate on single-thread
performance, and only distribute work amongst threads later, if necessary.

- We will start with an introduction to a rolling standard deviation algorithm using [numba](https://numba.pydata.org/).
- We will then improve the algorithm to only perform a single iteration over the data set.
- We will then implement this same algorithm in C and introduce various optimizations.
- Finally, we will inspect the assembler output of both the numba and C versions to compare the optimization efficacy.

### Rolling standard deviation

