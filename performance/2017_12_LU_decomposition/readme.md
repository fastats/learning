# LU Decomposition

*8th December 2017*, by Dave Willmer

In school we learn that every positive integer that's not a prime number
can be written as a `product of primes`; ie, you can formulate every
number by multiplying prime numbers together.

This is generally known as the `fundamental theorem of
arithmetic`.

For example, `15 = 5 x 3`; the prime factors that can be multiplied to
get the number `15` are `5` and `3`. You can think of these prime factors
as the low-level building blocks of all numbers, and as one of the building
blocks of numerical algorithms.

We can also do the same with matrices - we can usually calculate the low-level building
blocks of a matrix, which end up being extremely useful as building blocks
for many algorithms in linear algebra. However, as opposed to the real numbers
where all of them have prime factors, not all matrices have a LU
decomposition.

Getting the prime factors of an integer is, obviously, called
`factorisation`. With matrices, this process is either called
`factorisation` or `decomposition`.

`LU Decomposition` is a specific form of matrix decomposition which gives
us the factors of a matrix as a `lower` matrix and an `upper` matrix.

A `lower` matrix is one where all values above the diagonal are zero, and
an `upper` matrix is one where all values below the matrix are zero, shown
nicely in this image [from wikipedia](https://en.wikipedia.org/wiki/LU_decomposition):

<img src="./images/lu_wiki.svg">

This represents a [matrix multiplication]() between the lower and upper
matrices on the right-hand side.
