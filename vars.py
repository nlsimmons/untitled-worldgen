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

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 168, 82)
BLUE = (66, 135, 245)
DARK_BLUE = (0, 0, 139)
DARK_GREEN = (59, 85, 38)
RED = (255, 0, 0)

ORIGIN = (0, 0)

GLOBAL_NATURAL_DEATH_RATE = 0.0243
GLOBAL_NATURAL_FERTILITY_RATE = 0.0665
GLOBAL_NATURAL_GROWTH_RATE = 0.0421  # GLOBAL_NATURAL_FERTILITY_RATE - GLOBAL_NATURAL_DEATH_RATE


def rand_low(min, max):
    """
    Random number biased towards lower values
    """
    return random.triangular(min, max, min)


def rand_lower(min, max):
    """
    Random number with stronger bias towards lower values
    """
    return math.sqrt(rand_low(min, max) * rand_low(min, max))


def rand_high(min, max):
    """
    Random number biased towards higher values
    """
    return random.triangular(min, max, max)


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


def zipf(items, c=1):
    """
    Choose random item based on a zipf distribution
    Relative frequency of first item based on C
        c=1 - 25%
        c=2 - 17%
        c=3 - 12%
        c=4 - 11%?
              10
              8.5
              7
              8
    """
    q = []
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


def random_color():
    r = random.randrange(1, 255)
    g = random.randrange(1, 255)
    b = random.randrange(1, 255)
    return (r, g, b)
