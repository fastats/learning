
import numpy as np
# from pytest import approx


def west_79():

    x = np.array([1, 2, 3, 4, 5, 6])
    weights = np.array([0, 0, 0, 0, 0, 0])

    means = []
    vars = []

    sumw = weights[0]
    total = x[0]
    M = x[0]
    T = 0

    for i in range(1, len(x)):
        Q = x[i] - M
        temp = total + weights[i]
        R = Q * weights[i] / temp
        M = M + R
        T = T + R * sumw * Q
        sumw = temp

        x_bar = M
        s2 = T * i+1 / ((i+1 - 1) * sumw)

        means.append(x_bar)
        vars.append(s2)

        print(means)
        print(vars)

    x_bar = M
    s2 = T * 6 / ((6 - 1) * sumw)


if __name__ == '__main__':
    west_79()