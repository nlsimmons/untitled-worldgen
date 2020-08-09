import random
from Language import Language


# character = generate_character

"""
'Your name is {name}. You inhabit {village.name}, a small village of {village.population} people.'
'Life is difficult, and boring. Your father is a {}, your mother a {}, but you feel like you were destined for more.'
''



"""

# Generate base world map

# Generate starting village

# Generate nearest large town

# Generate neighboring villages

# These are all of the same culture

# Generate nearest major city

# May be a different culture

# Generate all major cities for the world (There should only be a few)

# These will all have different cultures


"""
A region has its local set of resources, which are concentrated in certain settlements
"""


class Village:
    def __init__(self):
        self.population = Population(150)
        self.culture
        self.name


class Person:
    def __init__(self, **kwargs):
        self.age = kwargs.get('age')
        self.name = kwargs.get('name')

    def __repr__(self):
        return f'{self.name}, {self.age}'


class Population:
    # http://uregina.ca/~gingrich/mar1298.htm
    # http://womenofhistory.blogspot.com/2007/08/medieval-marriage-childbirth.html
    # Noblewomen are married around 15
    # Peasants between 20-25
    # 1-2.5% chance of death during childbirth (higher with age)

    """
    Let's just make it every 2-4 years on average, if married, between 15-45
    Age of marriage is what will actually be variable

    r = random.range(2.0, 4.0)
    t = age - age_of_marriage (default=15)
    number_of_births = t / r

    1/3 children die in infancy

    Average to 5 or more live births per woman

    A married woman of a given age will have given birth X times:
    20-30   1-2 plus 0.25 per year
    30-40   8-10 plus 0.225 per year
    40-50   14-17 plus 0.08 per year
    50+     16-20
            Multiply by 2/3 because infant death

    33.33% chance of death at birth
     2.33% between 1-10
     1.03% between 10-20
     1.32% between 20-30
     1.65% between 30-40
     2.10% between 40-50
     3.05% between 50-60
     7.00% between 60-70
    17.27% between 70-80
    33.33% 80 and up

    in a 10 year span
     23.3% between 1-10
     10.3% between 10-20
     13.2% between 20-30
     16.5% between 30-40
     21.0% between 40-50
     30.5% between 50-60
     70.0% between 60-70
    100.0% between 70-80
    """

    ages = (0, 10, 20, 30, 40, 50, 60, 70, )
    age_probability = (22, 17, 18, 16, 12, 9, 6, 2, )
    language = Language()

    def __init__(self, **kwargs):
        self.size = kwargs.get('size')
        self.cultures = kwargs.get('cultures')
        self.generated = []

    def random(self):
        age = random.choices(self.ages, weights=self.age_probability)[0]
        age += random.randint(0, 9)
        name = self.language.genName()
        family_size = random.randint(0, 5)
        person = Person(age=age, name=name, family_size=family_size)
        self.generated.append(person)
        return person


class Culture:
    pass
    # factors
    #   language
    #   mono/polygyny
    #   mono/polyandry
    #   marriage or not
    #   values
    #       strength, face, ?
    #   inheiritance customs
    #   traditional crafts (specialty goods)
