import random
import math
from pprint import pprint

# random.seed(1)

# Probabilities of any randomly selected (generated) person to be within a certain age range
# For simplicity there is an equal chance of that person being any ones-digit age
AGES = [
    {
        'age': 0,
        'weight': 22
    },
    {
        'age': 10,
        'weight': 17
    },
    {
        'age': 20,
        'weight': 18
    },
    {
        'age': 30,
        'weight': 16
    },
    {
        'age': 40,
        'weight': 12
    },
    {
        'age': 50,
        'weight': 9
    },
    {
        'age': 60,
        'weight': 6
    },
    {
        'age': 70,
        'weight': 2
    },
]

ORIENTATIONS = {
    'male': {
        'heterosexual': 93.0,
        'homosexual': 2.5,
        'bisexual': 4.5,
    },
    'female': {
        'heterosexual': 88.0,
        'homosexual': 1.0,
        'bisexual': 11.0,
    },
}


def rand_low(min, max):
    """
    Random number biased towards lower values
    """
    r = random.uniform(0, 1)
    return ((max - min) * r ** 2) + min


def rand_high(min, max):
    """
    Random number biased towards higher values
    """
    r = random.uniform(0, 1)
    return ((max - min) * math.sqrt(r)) + min


def rand_mid(min, max):
    """
    Random number biased towards center
    """
    return random.triangular(min, max)


def clamp(value, low_bound, high_bound):
    """
    Clamp a value between two bounds
    """
    return max(low_bound, min(value, high_bound))


def chance(prob=50, times=1):
    """
    Returns True with a probability of {prob} / 100
    Defaults to 50/50
    """
    p_true = prob
    p_false = 100 - prob
    if times > 1:
        return any(chance(prob) for _ in range(times))

    return random.choices((True, False), weights=(p_true, p_false))[0]


def dd(input):
    """
    Die and dump because I use Laravel
    """
    pprint(input)
    quit()


def zipf(items):
    """
    Choose random item based on a zipf distribution
    """
    q = []
    c = 1
    length = len(items)
    for item in items:
        r = round(length / c * 100)
        for _ in range(r):
            q.append(item)
        c += 1
    return random.choice(q)


def get_midpoint(points):
    n = len(points)
    x_sum = y_sum = 0
    for x, y in points:
        x_sum += x
        y_sum += y
    return (x_sum / n, y_sum / n)
