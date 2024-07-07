import numpy as np

def pretty_fraction(a, b):
    if a % b == 0:
        return f'{int(a / b)}'
    g = np.gcd(int(a), b)
    return f'{int(a/g)}/{int(b/g)}'