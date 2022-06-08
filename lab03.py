# Mateusz Woźniak - RPiS Lab 03
import math
import scipy


def new(X):
    average = avg(X)
    s = 0
    for x in X:
        diff = x - average
        s += diff * diff
    return s / (len(X) - 1)


def avg(X):
    avg = 0
    for x in X:
        avg += x
    return avg / len(X)


# available hypothesis_type values: l, r, d
def average_hypothesis(X, guessed_average, deviation, hypothesis_type, alfa):
    average = avg(X)
    if guessed_average == -1:
        guessed_average = new(X)
    w = (average - guessed_average) / (deviation / math.sqrt(len(X)))

    def ppf(k):
        if len(X) < 30:
            return scipy.stats.t.ppf(k, len(X) - 1)
        else:
            return scipy.stats.norm.ppf(k)

    if hypothesis_type == 'd':
        return ppf(1 - alfa / 2) < w or w < - ppf(1 - alfa / 2)
    if hypothesis_type == 'l':
        return w < - ppf(1 - alfa)
    if hypothesis_type == 'r':
        return w > ppf(1 - alfa)


def sp(X, Y):
    i1 = (len(X) - 1) * new(X)
    i2 = (len(Y) - 1) * new(Y)
    return (i1 + i2) / (len(X) + len(Y) - 2)


def compare_averages(X, Y, variance1, variance2, alfa, hypothesis_type):
    if variance1 != -1 or variance2 != -1:
        w = (avg(X) - avg(Y)) / math.sqrt((variance1 / len(X)) + (variance2 / len(Y)))
    else:
        w = (avg(X) - avg(Y)) / (sp(X, Y) * math.sqrt((1 / len(X)) + (1 / len(Y))))

    def ppf(k):
        if len(X) < 30 or len(Y) < 30:
            return scipy.stats.t.ppf(k, len(X) + len(Y) - 2)
        else:
            return scipy.stats.norm.ppf(k)

    if hypothesis_type == 'd':
        return ppf(1 - alfa / 2) < w or w < - ppf(1 - alfa / 2)
    if hypothesis_type == 'l':
        return w < - ppf(1 - alfa)
    if hypothesis_type == 'r':
        return w > ppf(1 - alfa)


def dependant_variables(X, Y, guessed_diff, hypothesis_type, alfa):
    if len(X) != len(Y):
        raise Exception('Datasets sizes are not equal')
    D = [item for item in X if item not in Y]
    w = (avg(D) - guessed_diff) / (new(D) / math.sqrt(len(X)))
    ppf = scipy.stats.t.ppf
    if hypothesis_type == 'd':
        return ppf(1 - alfa / 2) < w or w < - ppf(1 - alfa / 2)
    if hypothesis_type == 'l':
        return w < - ppf(1 - alfa)
    if hypothesis_type == 'r':
        return w > ppf(1 - alfa)


def variance_hypothesis(X, guessed_variance, alfa, hypothesis_type):
    w = ((len(X) - 1) * new(X)) / guessed_variance
    if hypothesis_type == 'l':
        return w < scipy.stats.chi2.ppf(alfa, len(X) - 1)
    if hypothesis_type == 'r':
        return w > scipy.stats.chi2.ppf(1 - alfa, len(X) - 1)
    if hypothesis_type == 'd':
        return w > scipy.stats.chi2.ppf(alfa, len(X) - 1) or w < scipy.stats.chi2.ppf(alfa, len(X) - 1)


def uniform_distribution(X, alfa):
    expected_value = avg(X)
    w = 0
    for x in X:
        w += (x - expected_value) ** 2 / expected_value
    return w > scipy.stats.chi2.ppf(alfa, len(X) - 1)


def poisson_distribution(X, lambd, alfa):
    w = 0
    i = 0
    for x in X:
        d = scipy.stats.poisson.pmf(i, lambd)
        w += (x - d) ** 2 / d
        i += 1
    return w > scipy.stats.chi2.ppf(alfa, len(X) - 2)
