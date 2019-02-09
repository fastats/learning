# Statistical Moments

*29th August 2018*, by Dave Willmer

In this tutorial we will:

- Cover the basics of statistical moments.
- Write a simple python function to calculate arbitrary order moments.
- Expand on this by looking at single-pass algorithms.
- Finish with a generalised arbitrary-order single-pass moment algorithm.

### Basics of statistical moments
Please start by watching this video from Quantopian:

https://www.quantopian.com/lectures/statistical-moments

The important item from this video is to understand that a moment is
just E[X - E[X]]^k / sigma^k where

- k = 1 gives the mean
- k = 2 gives the variance
- k = 3 gives the skewness
- k = 4 gives the kurtosis

and hence the mean is the first moment, variance is the second moment,
skewness is the third moment and kurtosis is the fourth moment.

> **Task** - The first task is to write a python function which
  calculates statistical moments. The function should take two
  arguments; one for the data and one integer which defines the order
  `k`. Make sure your results match scipy/statsmodels.

### Single-pass algorithms

After completing this task, you should have a simple 2-3 line python
function. This function can be used on any sized data set, however the
simple implementation suffers from some performance issues with larger
arrays.

The naive implementation performs multiple passes over the input array;
at first glance this seems required because each datum gets the mean
subtracted from itself, however with streaming updates the mean (and
other measures) also need updating, and we don't want to continually
re-scan the same data on each update.

Let's take the first moment as a simple example:

```python
def mean(x):
    return sum(x) / len(x)
```

The naive version shown above will scan the input data twice on each
call (once for the sum, once for the length, although some python
containers store their length, so may return in O(1)).

In order to keep a running mean with streaming updates, we could store
both the sum and length separately, and just update them with the new
data:

```python
def bad_streaming_mean(datum, total, length):
    total += datum
    length += 1
    return total / length, total, length

mean, total, length = bad_streaming_mean(5, 0, 0)
mean, total, length = bad_streaming_mean(6, total, length)
mean, total, length = bad_streaming_mean(7, total, length)
```

The `bad_streaming_mean` function above shows how we can update our
calculated mean value without re-scanning the entire data set, however
it suffers from a few issues, including having to do manual book-keeping
for the `total` and `length`, as well as potential issues with a very large
`total` value.

The latter point here is an important item to remember: as `total` gets
very large, the relative size of the new data we are adding will get
smaller and smaller compared with the value of `total`.
With floating point numbers, this will eventually lead to large
round-off errors (sometimes called the big-number little-number problem).

To demonstrate this, try executing the following code:

```python
# Set `x` to a floating-point value of one million
x = 1e6

# Add a very small number (one millionth) to `x` a million times.
for i in range(1_000_000):
    x += 1e-6

# `x` should now be one million and one (1_000_001). print x
print(x)
```

You should get something similar to this:

```bash
1000001.0000076145
```

As you can see, the actual value is around 7.6 millionths higher than what
it should be. This is due to `x` being 12 orders of magnitude larger
than the increment.

If we repeat the exercise with `x = 1e4` (ie, 2 orders of magnitude smaller)
then we get 10001.000000338536, which is an error of only 0.3 millionths,
for a 10 order-of-magnitude difference.

The larger the magnitude difference of the floating point
values, the more the calculation will be affected by this problem.

As a result, we need a slightly smarter algorithm to keep the relative
magnitudes of the numbers fairly similar regardless of the number of
updates performed.

To cover this, we will refer to the following papers - please download
and read to complete the final tasks:

1. [West - Updating Mean and Variance Estimates: An Improved Method (1979)][1]
2. [Meng - Simpler Online Updates for Arbitrary Order Central Moments (2015)][2]

West's paper introduces streaming Mean and Variance calculations which
don't suffer from the round-off errors shown above. This is just one of
the problems that has to be understood when dealing with streaming
algorithms, and the solution is not always simple.

Meng's paper enhances West's algorithm with one that is simpler to code,
and has fewer data operations.

> **Task**: write an arbitrary order streaming moment calculator
  as per Meng's paper, which can calculate mean, variance, skewness and
  kurtosis.

If you're feeling mathematical, try the advanced task below:

> **Advanced task**: write a streaming version of
  `np.log(np.sum(np.exp(x)))`

To conclude:

- We learned about the four main statistical moments, the general
  equation for them, and how to write this as a python function.
- We saw that streaming versions of these calculations are possible, but
  we have to be *very* careful to ensure that floating-point numbers
  are of similar magnitudes.
- We then saw smarter streaming update versions (in [West's paper][1]
  and [Meng's paper][2]), which do not have the numerical stability
  issues of the naive version.
- These two algorithms are general solutions for streaming updates to
  statistical moment calculations, the more elegant versions of which
  have only recently been discovered.

This is still an active area of research.


[1]: https://people.xiph.org/~tterribe/tmp/homs/West79-_Updating_Mean_and_Variance_Estimates-_An_Improved_Method.pdf
[2]: https://arxiv.org/pdf/1510.04923.pdf
