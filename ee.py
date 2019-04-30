import math
from functools import reduce

def ackley(X):
    "X eh um vetor de n posicoes"
    n = len(X)

    a = 20
    b = 0.2
    c = 2 * math.pi

    sum1 = 0
    sum2 = 0
    for x in X:
        sum1 += x**2
        sum2 += math.cos(c * x)
    
    result = ((-a) * math.exp((-b) * math.sqrt((1/n) * sum1)) - math.exp((1/n) * sum2)) + (a + math.e)

    return result


