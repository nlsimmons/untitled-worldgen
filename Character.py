from Language import *
import random
from vars import *
from pprint import pprint

"""

Honesty-Humility (H):
    Facets: Sincerity, Fairness, Greed Avoidance, Modesty

    Sincere, honest, faithful, loyal, modest/unassuming
    versus
    sly, deceitful, greedy, pretentious, hypocritical, boastful, pompous
Emotionality (E):
    Facets: Fearfulness, Anxiety, Dependence, Sentimentality

    Emotional, oversensitive, sentimental, fearful, anxious, vulnerable
    versus
    brave, tough, independent, self-assured, stable
Extraversion (X):
    Facets: Social Self-Esteem, Social Boldness, Sociability, Liveliness

    Outgoing, lively, extraverted, sociable, talkative, cheerful, active
    versus
    shy, passive, withdrawn, introverted, quiet, reserved
Agreeableness (A):
    Friendly/Optimistic <-> Critical/Aggressive

    Facets: Forgivingness, Gentleness, Flexibility, Patience

    patient, tolerant, peaceful, mild, agreeable, lenient, gentle
    versus
    ill-tempered, quarrelsome, stubborn, choleric
Conscientiousness (C):
    Careful/Diligent <-> Impulsive/Disorganized

    Facets: Organization, Diligence, Perfectionism, Prudence

    organized, disciplined, diligent, careful
    versus
    reckless, lazy, absent-minded
Openness to Experience / Imagination (O):
    Conventional <-> Experimental

    Facets: Aesthetic Appreciation, Inquisitiveness, Creativity, Unconventionality

    intellectual, creative, innovative
    versus
    unimaginative, conventional


    # Fitness? Physical (brawn, endurance)
    #   Strength
    #   Endurance
    # Reasoning? Intellectual (conceiving what is, and what things could be)
    #   Deduction? Book smarts
    #   Imagination? Creativity? Street smarts
    # Empathy? Social (how to befriend, and how to manipulate) (or rather, natural charisma, and unnatural)
    #   Diplomacy? Charisma?
    #   Cunning (?)
    #       or, Charisma and Diplomacy
    # Finesse? (being fast, and being skillful)
    #   Quickness? Speed?
    #   Deftness? Manipulation?
    # Luck (not sure if this should be included)
    # reputation - the perception of others about your abilities, can be faked,
    #   but will need to be backed up by subterfuge or luck
    #   is tracked per location
    # Other: Ambition/Contentedness(is this important?)
"""

"""
skills
    lockpicking
    cooking
    tracking
    riding
    music
    shooting
    hand to hand
    persuasion

"""

"""
In general, the Major Arcana represent large turning points and the Minor Arcana represent the day-to-day insights
The Minor Arcana are believed to represent relatively mundane features of life.
The court cards represent the people whom one meets.

Latin   French      Element     Class       Faculty

Wands   Clubs       Air         Artisans    Creativity and will
Coins   Diamonds    Earth       Merchants   Material body or possessions
Cups    Hearts      Water       Clergy      Emotions and love
Swords  Spades      Fire        Nobility    Reason
1-10, Page, Knight, Queen, King


Pick one of:
    Nobility        1 karma
                    bonus: charisma, deduction, ingenuity
    Priests         2 karma
                    bonus: deduction, charisma, brawn
    Warriors        2 karma
                    bonus: brawn, endurance, finesse
    Commoners       3 karma
                    bonus: endurance, ingenuity, finesse

                    draw 3 cards
                    1st determines bonus
                    2nd determine wealth
                    3nd determines karma

    Blank           2 karma
                    draw 4 cards
                    You spawn in totally at random with no history


The Fool
bonus charisma, wealth 1, karma 3

The Magician
bonus finesse, wealth 1, karma 2

The High Priestess
bonus charisma, wealth 3, karma 2

The Empress
bonus endurance, wealth 3, karma 2

The Emperor
bonus brawn, wealth 3, karma 1

The Hierophant
bonus with religious characters, wealth 2, karma 3

The Lovers
bonus to seduction, wealth 1, karma 2

The Chariot
bonus brawn, wealth 1, karma 2

Justice
bonus deduction, wealth 2, karma 3

The Hermit
bonus finesse, wealth 1, karma 2

Wheel of Fortune
bonus to random stat, random wealth, random karma

Strength
bonus deduction, wealth 2, karma 1

The Hanged Man
bonus endurance, wealth 1, karma 1

Death
bonus brawn, wealth 3, karma 1

Temperance
bonus ingenuity, wealth 2, karma 3

The Devil
bonus finesse, wealth 2, karma 1

The Tower
a natural disaster will strike, wealth 2, karma 1

The Star
bonus charisma, wealth 1, karma 2

The Moon
bonus deduction, wealth 2, karma 1

The Sun
bonus ingenuity, wealth 3, karma 3

Judgement
bonus endurance, wealth 3, karma 3

The World
bonus ingenuity, wealth 3, karma 3


Pick male/female

"""

# random.seed(1)

STATS = [
    'charisma', 'deduction', 'endurance', 'finesse', 'ingenuity', 'brawn'
]

class CharacterCreation:

    DECK = {
        'fool': {
            'bonus': 'charisma',
            'wealth': 1,
            'karma': 3
        },
        'magician': {
            'bonus': 'finesse',
            'wealth': 1,
            'karma': 2
        },
        'high_priestess': {
            'bonus': 'charisma',
            'wealth': 3,
            'karma': 2
        },
        'empress': {
            'bonus': 'endurance',
            'wealth': 3,
            'karma': 2
        },
        'emperor': {
            'bonus': 'brawn',
            'wealth': 3,
            'karma': 1
        },
        'hierophant': {
            'bonus': 'hierophant',
            'wealth': 2,
            'karma': 3
        },
        'lovers': {
            'bonus': 'lovers',
            'wealth': 1,
            'karma': 2
        },
        'chariot': {
            'bonus': 'brawn',
            'wealth': 1,
            'karma': 2
        },
        'justice': {
            'bonus': 'deduction',
            'wealth': 2,
            'karma': 3,
        },
        'hermit': {
            'bonus': 'finesse',
            'wealth': 1,
            'karma': 2
        }, 'wheel_of_fortune': {
            'bonus': 'wheel',
            'wealth': 'wheel',
            'karma': 'wheel'
        },
        'brawn': {
            'bonus': 'deduction',
            'wealth': 2,
            'karma': 1
        },
        'hanged_man': {
            'bonus': 'endurance',
            'wealth': 1,
            'karma': 1
        },
        'death': {
            'bonus': 'brawn',
            'wealth': 3,
            'karma': 1
        },
        'temperance': {
            'bonus': 'ingenuity',
            'wealth': 2,
            'karma': 3
        },
        'devil': {
            'bonus': 'finesse',
            'wealth': 2,
            'karma': 1
        },
        'tower': {
            'bonus': 'tower',
            'wealth': 2,
            'karma': 1
        },
        'star': {
            'bonus': 'charisma',
            'wealth': 1,
            'karma': 2,
        },
        'moon': {
            'bonus': 'deduction',
            'wealth': 2,
            'karma': 1,
        },
        'sun': {
            'bonus': 'ingenuity',
            'wealth': 3,
            'karma': 3,
        },
        'judgement': {
            'bonus': 'endurance',
            'wealth': 3,
            'karma': 3,
        },
        'world': {
            'bonus': 'ingenuity',
            'wealth': 3,
            'karma': 3,
        },
    }

    @classmethod
    def create_character(cls):
        language = Language()
        # gender = input('M/F: ')
        # age = input('age: ')

        print('')
        character_class = input('[1]: Nobility; [2]: Priesthood; [3]: Warriors; [4]: Commoners; [5]: Blank : ')

        if character_class == '5':
            social_class = None
            bonus = []
            wealth = 0
            karma = 0
            cards = random.sample(cls.DECK.keys(), 4)
            for card in cards:
                card_bonus = cls.DECK[card].get('bonus')
                card_wealth = cls.DECK[card].get('wealth')
                card_karma = cls.DECK[card].get('karma')

                if card_bonus == 'wheel':
                    bonus.append(random.choice(list(STATS)))
                else:
                    bonus.append(card_bonus)

                if card_wealth == 'wheel':
                    wealth += random.randint(1, 3)
                else:
                    wealth += card_wealth

                if card_karma == 'wheel':
                    karma += random.randint(1, 3)
                else:
                    karma += card_karma

            karma = round(karma / 4)
            wealth = round(wealth / 4)

        else:
            if character_class == '1':
                social_class = 'Nobility'
                karma = 1
                bonus = ['charisma', 'deduction', 'ingenuity']
            if character_class == '2':
                social_class = 'Clergy'
                karma = 2
                bonus = ['deduction', 'charisma', 'brawn']
            if character_class == '3':
                social_class = 'Warriors'
                karma = 2
                bonus = ['brawn', 'endurance', 'finesse']
            if character_class == '4':
                social_class = 'Commoner'
                karma = 3
                bonus = ['endurance', 'ingenuity', 'finesse']

            cards = random.sample(cls.DECK.keys(), 3)
            card_bonus = cls.DECK[cards[0]].get('bonus')
            card_wealth = cls.DECK[cards[1]].get('wealth')
            card_karma = cls.DECK[cards[2]].get('karma')

            if card_bonus == 'wheel':
                bonus.append(random.choice(STATS))
            else:
                bonus.append(card_bonus)

            if card_wealth == 'wheel':
                wealth = random.randint(1, 3)
            else:
                wealth = card_wealth

            if card_karma == 'wheel':
                karma += random.randint(1, 3)
            else:
                karma += card_karma
        age = 18

        # karma and wealth each have a max of 6
        name = language.name()
        print('')
        print(f'Name: {name}, Age: {age}')
        print(f'Karma: {karma}')
        print(f'Wealth: {wealth}')
        print(f'Cards: {", ".join(cards)}')
        print(f'Bonuses: {", ".join(bonus)}')
        print('')

        stats = {
            'brawn': int(rand_high(2, 10)),
            'charisma': int(rand_high(2, 10)),
            'deduction': int(rand_high(2, 10)),
            'endurance': int(rand_high(2, 10)),
            'finesse': int(rand_high(2, 10)),
            'ingenuity': int(rand_high(2, 10)),
        }

        character = Person(age=age,
                           bonus=bonus,
                           social_class=social_class)
        character.gen_stats(**stats)
        return character


class Person:
    alive = True
    infertile = chance(8)  # 8% chance of a man or woman being totally infertile

    def __repr__(self):
        if self.culture.family_name_first:
            name = self.family_name + ' ' + self.name
        else:
            name = self.name + ' ' + self.family_name
        return f'Name: {name}; Age: {self.age}; Alive: {"Yes" if self.alive else "No"}'

    def __init__(self, **kwargs):
        culture = kwargs.get('culture', Culture())
        self.culture = culture
        self.name = kwargs.get('name', culture.language.name())
        self.family_name = kwargs.get('family_name')

        spouse = kwargs.get('spouse')
        if spouse:
            self.spouses = [spouse]
            if self not in spouse.spouses:
                spouse.spouses.append(self)
        else:
            self.spouses = []
        self.mother = kwargs.get('mother')
        self.father = kwargs.get('father')
        self.siblings = []
        # karma
        # wealth

        _age = kwargs.get('age')
        if _age is None:
            ages = [a['age'] for a in AGES]
            age_weights = [a['weight'] for a in AGES]

            _age = random.choices(ages, weights=age_weights)[0]
            _age += random.randint(0, 9)
        self.age = _age

        self.gender = kwargs.get('gender')
        if not self.gender:
            self.gender = random.choice(('male', 'female'))
        self.orientation = kwargs.get('orientation')
        if not self.orientation:
            self.orientation = random.choices(list(ORIENTATIONS.get(self.gender).keys()),
                                              weights=list(ORIENTATIONS.get(self.gender).values()))[0]

        self.social_class = kwargs.get('social_class')  # random.choice(culture.social_classes))
        self.wealth = kwargs.get('wealth', random.randint(1, 3))
        self.bonuses = kwargs.get('bonus')

    def gen_stats(self, **kwargs):
        # Stats
        self.brawn = kwargs.get('brawn', int(rand_mid(2, 10)))
        self.charisma = kwargs.get('charisma', int(rand_mid(2, 10)))
        self.deduction = kwargs.get('deduction', int(rand_mid(2, 10)))
        self.endurance = kwargs.get('endurance', int(rand_mid(2, 10)))
        self.finesse = kwargs.get('finesse', int(rand_mid(2, 10)))
        self.ingenuity = kwargs.get('ingenuity', int(rand_mid(2, 10)))

        _bonus = set()
        for b in self.bonuses:
            if b in STATS:
                setattr(self, b, getattr(self, b) + 2)
            else:
                _bonus.add(b)
        self.bonuses = _bonus

    @property
    def stats(self):
        return {
            'brawn': self.brawn,
            'charisma': self.charisma,
            'deduction': self.deduction,
            'endurance': self.endurance,
            'finesse': self.finesse,
            'ingenuity': self.ingenuity,
        }

"""

Preference wife 15 years younger
Half age plus 7

average age difference between husband and wife was three years

3 yrs to 15 yrs

20 - 17
30 - 22
40 - 27
50 - 32

ideal reproductive match is for a man to marry a woman six years his junior

"""


def generate_family(**kwargs):
    culture = kwargs.get('culture')
    family_name = culture.genName()  # The way this is adopted is culture dependent. Think about it later
    min_marriage_age, max_marriage_age = 15, 25  # Culture-dependent
    mother_age_start = int(rand_mid(min_marriage_age, max_marriage_age))
    father_age_start = clamp(mother_age_start + random.randint(-5, 5),
                             min_marriage_age, max_marriage_age)
    children = []
    current_age = kwargs.get('current_age')  # The age at which to terminate birthing simulation
    if current_age is None:
        current_age = random.randint(mother_age_start + 15, mother_age_start + 50)

    mother = Person(age=mother_age_start, family_name=family_name, culture=culture)
    father = Person(age=father_age_start, family_name=family_name, culture=culture)
    father.spouses = [mother]
    mother.spouses = [father]

    while mother.age < current_age and father.age < current_age:

        mother.age += 2
        father.age += 2
        for c in children:
            if not c.alive:
                continue
            if chance(death_chance(c.age), 2):
                c.alive = False
            else:
                c.age += 2

        if not mother.infertile and not father.infertile and chance(pregnancy_chance(mother.age)):
            # birth a child
            if chance(0.4):
                # child is twins
                if chance(67):
                    # child survives
                    children.append(Person(age=0,
                                           family_name=family_name,
                                           culture=culture,
                                           mother=mother,
                                           father=father))
                if chance(67):
                    # child survives
                    children.append(Person(age=0,
                                           family_name=family_name,
                                           culture=culture,
                                           mother=mother,
                                           father=father))
                if chance(childbirth_death_chance(mother.age) * 2):
                    # double chance of mother dying although this should probably be higher
                    mother.alive = False
                    if father.age < 50 and chance(50):
                        # father remarries
                        mother = Person(gender='female',
                                        family_name=family_name,
                                        age=random.randint(min_marriage_age, max_marriage_age),
                                        culture=culture,
                                        spouse=father)
                    else:
                        break
            else:
                if chance(67):
                    # child survives
                    children.append(Person(age=0,
                                           family_name=family_name,
                                           culture=culture,
                                           mother=mother,
                                           father=father))
                if chance(childbirth_death_chance(mother.age)):
                    # mother dies
                    mother.alive = False
                    if father.age < 50 and chance(50):
                        # father remarries
                        mother = Person(gender='female',
                                        family_name=family_name,
                                        age=random.randint(min_marriage_age, max_marriage_age),
                                        culture=culture,
                                        spouse=father)
                    else:
                        break

        if chance(death_chance(mother.age), 2):
            # mother dies
            mother.alive = False
            if father.age < 50 and chance(50):
                # father remarries
                mother = Person(gender='female',
                                family_name=family_name,
                                age=random.randint(min_marriage_age, max_marriage_age),
                                culture=culture,
                                spouse=father)
            else:
                break

        if chance(death_chance(father.age), 2):
            # father dies
            father.alive = False
            if mother.age < 35 and chance(50):
                father = Person(gender='male',
                                family_name=family_name,
                                age=random.randint(min_marriage_age, max_marriage_age),
                                culture=culture,
                                spouse=mother)
            else:
                break

    for c in children:
        c.siblings = [s for s in children if c is not s]

    return [mother, father] + children


def pregnancy_chance(age):
    if age < 30:
        return 99.5
    fertility_loss = ((age - 30) ** 2) / 3
    if fertility_loss < 0:
        return 0.05
    return 100 - fertility_loss


def death_chance(age):
    # Chance of someone dying for any reason
    if 0 <= age < 10:
        return 2.33
    if 10 <= age < 20:
        return 1.03
    if 20 <= age < 30:
        return 1.32
    if 30 <= age < 40:
        return 1.65
    if 40 <= age < 50:
        return 2.10
    if 50 <= age < 60:
        return 3.05
    if 60 <= age < 70:
        return 7.00
    if 70 <= age < 80:
        return 17.27
    # 80+
    return 33.33


def childbirth_death_chance(age):
    # Chance of a woman dying in childbirth
    return (0.05 * age) + 0.25
