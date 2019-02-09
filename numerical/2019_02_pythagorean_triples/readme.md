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