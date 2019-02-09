# Pythagorean Triples

Recently there has been a huge interest in Pythagorean Triples; one of
the C++ ISO committee members (Eric Niebler) published [this blog post](http://ericniebler.com/2018/12/05/standard-ranges/)
showing how to calculate Pythagorean Triples using a new C++ feature
called 'Ranges'.

This blog post from Niebler caused quite a storm in the programming
community, with [many people](http://aras-p.info/blog/2018/12/28/Modern-C-Lamentations/)
commenting that the code is over-complicated and difficult to read.

Despite being a long-term C++ programmer I tend to agree that the new
language features are cumbersome, but what I find far more interesting
are the various different ways that something like this can be
calculated.

In this article we will **not** take pot-shots at the C++ committee (mainly
because I've worked with some of them before and they're really very
nice people!), but we will have a look at some more elegant ways of
calculating Pythagorean Triples.

### Naive Method

A Pythagorean Triple is a set of three positive integers `(a, b, c)`
such that $a^2 + b^2 = c^2$, which is commonly taught in primary school.

What we would like to do is generate a stream of Pythagorean Triples.

> **Task**: Most people have come across the `(3, 4, 5)` triangle, which
  is a Pythagorean Triple. Starting with these three integers, how would
  you calculate the next Pythagorean Triple?

Most people would start with a naive implementation which scans through
the integers and tests whether `a**2 + b**2 == c**2` , so let's start
with that.

We know immediately that given a triple `(a, b, c)`, that `a <= b < c`,
so we can offset the for-loops like this

```python
def naive_triples(up_to=20):
    for a in range(1, up_to):
        for b in range(a, up_to):
            for c in range(b, up_to):
                if a*a + b*b == c*c:
                    yield (a, b, c)
```

which gives:

```
>>> for x in naive_triples(up_to=20):
...     print(x)

(3, 4, 5)
(5, 12, 13)
(6, 8, 10)
(8, 15, 17)
(9, 12, 15)
```

This works, and is basically the same algorithm as Eric Niebler uses in
his blog post (see [lines 55-59 here](http://ericniebler.com/2018/12/05/standard-ranges/)).
However this algorithm is extremely inefficient as we are effectively
doing a complete brute force search through the domain.

As the numbers get larger, and the gaps between the Triples get
potentially very big, this algorithm is going to scale very badly.

Also, in pragmatic terms, you have to specify the integer at the upper
bound of your search space (ie, `up_to`). Without specifying this, the
innermost loop would continue forever, and you would never find any
triples at all!

This means that we can't use this algorithm to just go and find the
next Triple.

So let's take a look at some less naive ways of calculating
Pythagorean Triples.

### Fibonacci's Method

This is described on Wikipedia [here](https://en.wikipedia.org/wiki/Formulas_for_generating_Pythagorean_triples).

Essentially this uses various properties of square numbers, specifically
that the sum of `n` odd integers is $n^2$.

Implementing this in python can be done as follows:

```python
from itertools import count
from math import sqrt

def fibonacci_triples():
    odd_ints = []
    for idx, odd in enumerate(count(start=1, step=2)):
        odd_ints.append(odd)

        if int(odd**0.5)**2 == int(odd) and len(odd_ints) >= 4:
            b2 = sum(odd_ints[:-1])
            c2 = sum(odd_ints)
            yield tuple(map(int, (sqrt(odd), sqrt(b2), sqrt(c2))))
```

The `int(odd**0.5)**2 == int(odd)` is a short-hand way of checking that
the integer is a perfect square. This method is not perfect, however,
but suffices for what we're showing here.

This gives:

```python
>>> fib = fibonacci_triples()
>>> for x in range(10):
...     r = next(fib)
...     print(r, r[0]*r[0] + r[1]*r[1] == r[2]*r[2])

(3, 4, 5) True
(5, 12, 13) True
(7, 24, 25) True
(9, 40, 41) True
(11, 60, 61) True
(13, 84, 85) True
(15, 112, 113) True
(17, 144, 145) True
(19, 180, 181) True
(21, 220, 221) True
```

There are two important things to note here:
- We can specify the number of return values we want, not the max bound
  to check up to. This means that we could have an endless stream of
  Pythagorean Triples if we wanted to, and consequently this scales
  much better than the naive version above.
- This has missed some valid answers. Although this algorithm is provably
  correct, and has been proven to provide an infinite stream of
  Pythagorean Triples, it does miss some triples due to its reliance
  on the sequence of odd integers.

If you compare with the naive version above, you will quickly see that
the Fibonacci version has missed `(6, 8, 10)` and `(8, 15, 17)` among
others.

The implementation above also requires the entire list of previous odd
integers to be kept in memory - this could be improved by storing just
the sum and the sum up to `n - 1`, however in its current state this
algorithm's memory usage scales as `O(n)`.

So is it possible to have an algorithm which allows streaming values
(unlike the naive version), but which also generates all triples (unlike
the Fibonacci method), and also operates in constant time and constant
memory?

### Berggren Method

In 1934 Berggren showed that Linear Algebra can be used to
generate all *primitive* Pythagorean Triples from a known starting
triple \[1\].

> Note: A *primitive* triple is one where the values `(a, b, c)` do
  **not** share a common divisor.

Using these three hard-coded matrices:

```python
A = np.array([
    [1, -2, 2],
    [2, -1, 2],
    [2, -2, 3]
])

B = np.array([
    [1, 2, 2],
    [2, 1, 2],
    [2, 2, 3]
])

C = np.array([
    [-1, 2, 2],
    [-2, 1, 2],
    [-2, 2, 3]
])
```

If we take the dot product of these three matrices and a vector of a
known Pythagorean Triple, then for each dot product we will get
another Pythagorean Triple:

```python
def barning_triples(start=(3, 4, 5)):
    last_a = last_b = last_c = np.array(start)
    while True:
        last_a = A @ last_a
        yield last_a

        last_b = B @ last_b
        yield last_b

        last_c = C @ last_c
        yield last_c
```

Which can be run as follows:

```python
>>> barn = barning_triples()
>>> for x in range(10):
... print(next(barn))

[ 5 12 13]
[21 20 29]
[15  8 17]
[ 7 24 25]
[119 120 169]
[35 12 37]
[ 9 40 41]
[697 696 985]
[63 16 65]
[11 60 61]
```

Obviously this runs in constant time and constant space (up to the
max integer size supported by numpy).

In 1963, F.J.M. Barning rediscovered these matrices \[2\], as did Hall
in 1970 \[3\].

Interestingly, this Berggren algorithm can be shortened using the new
[assignment expression syntax](https://www.python.org/dev/peps/pep-0572/)
in python 3.8:

```python
def barning_triples(start=(3, 4, 5)):
    last_a = last_b = last_c = np.array(start)
    while True:
        yield (last_a := A @ last_a)
        yield (last_b := B @ last_b)
        yield (last_c := C @ last_c)
```

Which, when you understand the mathematics, is considerably more
elegant than the C++ ranges implementation.

## Conclusions

In this post we have tried to show that when faced with a seemingly
simple numerical problem to solve, there are usually many ways of
solving it and the simple, naive method may be terribly inefficient.

It is usually best to search for or derive smarter solutions which have
better scaling in time or space, and in a large number of problems you
will generally find very elegant solutions using Linear Algebra.

## References

1. B. Berggren. Pytagoreiska trianglar. TidskriftforElementarMatematik,
   Fysik och Kemi, 17(1934), 129{139}.

2. Barning F.J.M. Over pythagorese en bijna-pythagorese driehoeken en
  een generatieproces met behulp van unimodulaire matrices. Stichting
  Mathematisch Centrum. Zuivere Wiskunde. Stichting Mathematisch
  Centrum; 1963.

3. A. Hall. Genealogy of Pythagorean Triads. The Mathematical Gazette,
   54(1970), 377{379}.

## Tasks

- Implement a robust check for square integers, and show it working in
  the Fibonacci Method above. The current `square` check fails on
  certain edge cases.

- Implement the Fibonacci Method with constant memory usage instead of
  linear.

- Create a program which will visualise the [Tree of Primitive
  Pythagorean Triples](https://en.wikipedia.org/wiki/Tree_of_primitive_Pythagorean_triples).
  Note that only **primitive** triples should be on this tree, which
  are triples where `(a, b, c)` do not share a common divisor.

- Write numba `jit` implementations of the algorithms above, and show
  how they scale in time and memory by calculating all triples up to the
  size of a 32-bit integer.

- Show why the Berggren / Barning matrices work.

- Show alternative methods of calculating Pythagorean Triples (we have
  only shown 3 above, but there are many more in the literature).