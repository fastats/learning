# Linear Systems, APIs and Authentication

This is a longer, more in-depth training piece; this is also a
pre-requisite for some of the `Numerical Programming` articles.

There are 3 main sections:

1. First of all, we are going to write some very simple functions
  which happen to be the low-level building blocks for solving all
  linear systems using matrix algebra.
2. However, instead of then progressing through some numerical
  programs, the second task will be to to expose these simple functions
  as HTTP APIs, ie. web services.
3. The final task is to add HTTP authentication to each of the three
  HTTP APIs. There are three main methods of authentication, and you
  should use one method for each of the HTTP APIs.

You should complete all of the tasks in **any** language of your choosing,
and send in a PR with the implementations of each task.

It is useful to all parties if you pick a new language that you're
currently unfamiliar with.

## Linear Systems

When solving linear systems (those of the form `Ax = b`), using
techniques such as Gaussian Elimination, all of the algorithms can be
expressed in terms of 3 simple functions:

1. Interchange two rows
2. Multiply a row by a scalar
3. Add a scalar multiple of another row

These are generally referred to as `elementary row operations`, which
we will discuss in turn below.

### Row interchange

Using a test data set defined as:

```bash
>>> data
array([[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]], dtype=int16)
```

We could expect the interchange of row index 0 and row index 1 to result
in:

```bash
>>> data
array([[4, 5, 6],
       [1, 2, 3],
       [7, 8, 9]], dtype=int16)
```

### Scalar multiplication

Using the same test data set as above, scalar multiplication of row
index 0 by 5 would result in:

```bash
>>> data
array([[5, 10, 15],
       [4, 5, 6],
       [7, 8, 9]], dtype=int16)
```

### Add a Scalar Multiple

You may recognise this as a Fused-Multiply-Add (FMA) instruction, which
is what we generally try to aim for with high-performance algorithms.
We want to take a multiple of two items and add it to our starting
value; this is similar to the inner loop of a matrix-matrix
multiplication.

If we take row index 2, multiply it by 5, and add it to row index 0, we
would end up with:

```bash
>>> data
array([[36, 42, 48],
       [ 4,  5,  6],
       [ 7,  8,  9]], dtype=int16)
```

> Task: Write simple functions to implement the three `elementary row
  operations`, and make sure there's sensible tests for them.

## APIs

In recent years, web APIs (sometimes called web services) have become
very highly regarded as good practices. The founder of Amazon, Jeff
Bezos, famously told all his developers that [all data had to be
accessed via publicly-exposable services](https://homepages.dcc.ufmg.br/~mtov/pmcc/modularization.pdf)
or they would get fired!

> Task: read [this article](https://apievangelist.com/2012/01/12/the-secret-to-amazons-success-internal-apis/)
  which introduces the high-level concepts that a service-based
  approach requires.

It is **extremely** important that any new architecture gets their
solutions to these correct.

As a result, before building any new APIs, ensure you are familiar
with the current best practices. Articles worth reading are:

- [API Design - The Guidelines](https://hackernoon.com/restful-api-designing-guidelines-the-best-practices-60e1d954e7c9)
- [Best Practices and Common Pitfalls](https://medium.com/@schneidenbach/restful-api-best-practices-and-common-pitfalls-7a83ba3763b5)
- [10 Best Practices](https://blog.mwaysolutions.com/2014/06/05/10-best-practices-for-better-restful-api/)
- [Make your users happy](https://blog.florimondmanca.com/restful-api-design-13-best-practices-to-make-your-users-happy)

However, there are thousands of blog posts/articles published which
describe best practices.

> Task: Once you've read the above, and done some further googling, this
  task is to expose the functions created previously via web service
  APIs according to commonly accepted best practices.

## Authentication (and Authorisation)

Once you have your service API operational, you will obviously want to
protect it from abuse, and protect your users' data. This is one of the
most important aspects of creating a web service, but unfortunately
is also one of the least well understood.

It is extremely important to understand the pros and cons of each
authentication system. Remember Jeff Bezos' instructions to the early
Amazon developers:

```
5. All service interfaces, without exception, must be designed from
the ground up to be externalizable. That is to say, the team must
plan and design to be able to expose the interface to developers
in the outside world. No exceptions.
```

In other words, the main benefit is in making all of our internal APIs
available to our users and the wider community.

This attitude is widely credited as helping Amazon grow from an online
bookshop to one of the world's largest tech companies.

Consequently, we need to be able to authenticate our users, even for
small/simple internal APIs.

As of January 2019, HTTP API Authentication is usually done in one
of three methods:

- HTTP Basic Authentication
- API Keys
- OAuth

There are variations and nuances to each of these, but the labels above
encompass the widely accepted practices.

When it comes to security, you are always best off following the best
practices of security professionals instead of creating your own
solutions. It is very easy to accidentally create very large security
problems in your application if you try to design something yourself.

For a good overview of these methods see:

- [3 Common Authentication methods explained](https://nordicapis.com/3-common-methods-api-authentication-explained/)
- [API Authentication Basics](https://blog.restcase.com/restful-api-authentication-basics/)
- [Why I love Basic Auth](https://www.rdegges.com/2015/why-i-love-basic-auth/)

I personally disagree with much of the last article, but I think it's
good to give a balanced viewpoint - there are a lot of different
opinions, and rarely a 'right way', just lots of 'wrong ways'.

> Task: Expose each of the `elementary row operations` functions APIs
  with a different method of authentication. It's important to document
  your API and authentication methods so that onboarding is easy for
  your users.
