
# Strassen's Algorithm

*25th July 2017*, by Dave Willmer

In the [first lesson](../2017_06_performance_basics) we focussed on matrix-matrix multiplication (MMM), partially because it's a simple concept and a nice way to teach the more complex performance ideas, but also because it's an important building block for all of linear algebra.

Given that it is so central to understanding linear algebra, we are going to focus on it in this lesson as well, however instead of looking at optimising for hardware, we will look at optimising the algorithm from a mathematical point of view.

- We will cover [Strassen's Algorithm](https://en.wikipedia.org/wiki/Strassen_algorithm), as a simple, pragmatic introduction to implementing divide-and-conquer algorithms to reduce the algorithmic complexity.

### Strassen's Algorithm

In the first lesson, we saw that the naive MMM is implemented as:

```python
for i in range(A.shape[0]):
    for j in range(B.shape[1]):
        for k in range(A.shape[1]):
            C[i,j] += A[i,k] * B[k,j] 
```

Clearly this scales as `O(n^3)` (ignoring the difference in matrix dimensions for the sake of clarity), however it is possible to reduce the number of calculations required by using a divide-and-conquer algorithm:

(1) Divide each of the matrices into 4 equal parts:

```
----------------       |-------- |--------
|              |       |       | |       |
|              |       |  A11  | |  A12  |
|              |       |       | |       |
|       A      |       |       | |       |
|              |  ==>  |-------- |--------
|              |       |       | |       |
|              |       |  A21  | |  A22  |
|              |       |       | |       |
----------------       |_______| |_______|
```

(2) Calculate the intermediate matrices:

```
M1 = (A11 + A22)(B11 + B22)
M2 = (A21 + A22)B11
M3 = A11(B12 - B22)
M4 = A22(B21 - B11)
M5 = (A11 + A12)B22
M6 = (A21 - A11)(B11 + B12)
M7 = (A12 - A22)(B21 + B22)
```

(3) Reconstruct C from the intermediates:

```
C11 = M1 + M4 - M5 + M7
C12 = M3 + M5
C21 = M2 + M4
C22 = M1 - M2 + M3 + M6
```

The complexity of Strassen's algorithm is covered in detail [here](http://mathworld.wolfram.com/StrassenFormulas.html), [here](http://www.geeksforgeeks.org/strassens-matrix-multiplication/) and [here](http://www.cs.mcgill.ca/~pnguyen/251F09/matrix-mult.pdf), however the important detail is:

- The number of multiplications for each section goes from 8 to 7, therefore the complexity goes from `O(n^log(8))` to `O(n^log(7))`.
- In algorithmics we use log base 2, therefore log(8) = 3, log(7) = 2.807.
- This makes a huge difference to calculation times.

> *Task:* The task for this lesson is to implement Strassen's algorithm in a language of your choice.

Strassen's algorithm is not the fastest for MMM - recent advancements based on Strassen's algorithm have reduced the asymptotic complexity from `O(n^2.807)` to `O(n^2.37)`. The [Coppersmith-Winograd](https://people.csail.mit.edu/virgi/matrixmult-f.pdf) algorithm and the [Le Gall](https://arxiv.org/abs/1401.7714) algorithm are examples of these faster algorithms.
