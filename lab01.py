# Mateusz Woźniak - RPiS Lab 01
import math


def poisson(n, p, s):
    lambd = n * p
    return math.e ** (-lambd) * (lambd ** s / math.factorial(s))


def poisson_multiple(n, p, list):
    lambd = n * p
    estimation = 0
    for s in list:
        estimation += poisson(n, p, s)
    error = lambd * lambd / n
    return estimation, error


print(poisson(100, 0.05, 1))
print(poisson_multiple(100, 0.05, [1]))
