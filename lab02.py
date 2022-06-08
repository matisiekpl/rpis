# Mateusz Woźniak - RPiS Lab 02
import math
from math import sqrt

import numpy
import scipy.stats


def avg(list):
    avg = 0
    for x in list:
        avg += x
    return avg / len(list)


def new(list):
    average = avg(list)
    s = 0
    for x in list:
        diff = x - average
        s += diff * diff
    return s / (len(list) - 1)


def confidence_interval_with_known_variance(list, variance, alfa):
    average = avg(list)
    z = scipy.stats.norm.ppf(1 - alfa / 2)
    d = z * math.sqrt(variance) / sqrt(len(list))
    return [average - d, average + d]


print('Task 3 - TVs - confidence_interval_with_known_variance')
TVs = [8.1, 7.9, 9.6, 6.4, 8.7, 8.8, 7.9]
print(f'Variance for TVs: {numpy.var(TVs)}')
print(confidence_interval_with_known_variance(TVs, numpy.var(TVs), 0.1))


def confidence_interval_with_unknown_variance(list, alfa):
    average = avg(list)
    t = scipy.stats.t.ppf(1 - alfa / 2, len(list) - 1)
    d = t * sqrt(new(list)) / sqrt(len(list))
    return [average - d, average + d]


def confidence_interval_for_variance(list, alfa):
    a = (len(list) - 1) * new(list)
    b1 = scipy.stats.chi2.ppf(1 - alfa / 2, len(list) - 1)
    b2 = scipy.stats.chi2.ppf(alfa / 2, len(list) - 1)
    return [a / b1, a / b2]


print('Task 3 - TVs - confidence_interval_with_unknown_variance')
print(confidence_interval_with_unknown_variance(TVs, 0.1))

print('Task 3 - TVs - confidence_interval_for_variance')
print(confidence_interval_for_variance(TVs, 0.1))
