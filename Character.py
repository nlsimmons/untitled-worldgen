from Language import *
import random
from vars import *
from pprint import pprint

"""


# reputation - the perception of others about your abilities, can be faked,
#   but will need to be backed up by subterfuge or luck
#   is tracked per location

skills
    lockpicking
    cooking
    tracking
    riding
    music
    shooting
    hand to hand
    persuasion

In general, the Major Arcana represent large turning points and the Minor Arcana represent the day-to-day insights
The Minor Arcana are believed to represent relatively mundane features of life.
The court cards represent the people whom one meets.

Pick one of:

    Nobility
        1 karma
        charisma, deduction, ingenuity
    Warrior
        2 karma
        endurance, brawn, finesse
    Merchant / Clergy
        2 karma
        charisma, finesse, deduction
    Commoner
        3 karma
        endurance, ingenuity, brawn

    draw 3 cards
    1st determines bonus
    2nd determine wealth
    3nd determines karma

    Blank           2 karma
                    draw 4 cards
                    You spawn in totally at random with no history

Latin   French      Element     Class       Faculty

Wands   Clubs       Air         Artisans    Creativity and will
Coins   Diamonds    Earth       Merchants   Material body or possessions
Cups    Hearts      Water       Clergy      Emotions and love
Swords  Spades      Fire        Nobility    Reason
1-10, Page, Knight, Queen, King

===============================

People

    Wands   Clubs       Air         Artisans    Creativity and will
    Coins   Diamonds    Earth       Merchants   Material body or possessions
    Cups    Hearts      Water       Clergy      Emotions and love
    Swords  Spades      Fire        Nobility    Reason
    1-10, Page, Knight, Queen, King

Swords - Analysts :
    INTJ (Architect) - Imaginative and strategic thinkers, with a plan for everything.
    INTP (Logician) - Innovative inventors with an unquenchable thirst for knowledge.
    ENTJ (Commander) - Bold, imaginative and strong-willed leaders, always finding a way.
    ENTP (Debater) - Smart and curious thinkers who cannot resist an intellectual challenge.
bonus deduction


Cups - Diplomats :
    INFJ (Advocate) - Quiet and mystical, yet very inspiring and tireless idealists.
    INFP (Mediator) - Poetic, kind and altruistic people, always eager to help a good cause.
    ENFJ (Protaganist) - Charismatic and inspiring leaders, able to mesmerize their listeners.
    ENFP (Campaigner) - Enthusiastic, creative and sociable free spirits, who can always find a reason to smile.
bonus charisma

Coins - Sentinels :
    ISTJ (Logistician) - Practical and fact-minded individuals, whose reliability cannot be doubted.
    ISFJ (Defender) - Very dedicated and warm protectors, always ready to defend their loved ones.
    ESTJ (Executive) - Excellent administrators, unsurpassed at managing things – or people.
    ESFJ (Consul) - Extraordinarily caring, social and popular people, always eager to help.
bonus finesse

Wands - Explorers :
    ISTP (Virtuoso) - Bold and practical experimenters, masters of all kinds of tools.
    ISFP (Adventurer) - Flexible and charming artists, always ready to explore and experience something new.
    ESTP (Entrepeneur) - Smart, energetic and very perceptive people, who truly enjoy living on the edge.
    ESFP (Entertainer) - Spontaneous, energetic and enthusiastic people – life is never boring around them.
bonus ingenuity

values in a leader
    being rewarded vs fairness
    honor vs cunning
    strength vs mercy

===============================

Characters

    The Fool -
    The Magician
    The High Priestess
        Raven - A charming, if somewhat spacey, rogue
            high charisma
            high finesse
            moderate endurance
            moderate ingenuity
            low brawn
            low deduction
    The Empress
    The Emperor
    The Hierophant
    The Lovers
    The Chariot
        The courier - Basically just the Punisher.
            high brawn
            high endurance
            moderate finesse
            moderate deduction
            low ingenuity
            low charisma
    Justice
    The Hermit
    Wheel of Fortune
    Strength
    The Hanged Man
    Death
        The shepherd (Erika?) - Once a kind-hearted soul seeking only the best for everyone and everything around her,
                now left intensely jaded by the cruelty she has witnessed. While she maintains a warm demeanor
                and always strives to help the less fortunate, it conceals a deep, burning hatred for humanity as a
                whole.
            high deduction
            high endurance
            moderate brawn
            moderate charisma
            low ingenuity
            low finesse
    Temperance
    The Devil
    The Tower
    The Star
    The Moon
    The Sun
    Judgement
    The World


===============================

The quest deck

who did it

    in terms of relation to the player

    number determines whether of lower or higher class
    Wands - an enemy
    Coins - a stranger
    Cups - a friend / lover
    Swords - a superior

    The Fool - a younger family member (same class)
    The Magician - a lover (same class)
    The High Priestess - someone cunning, ambitious, part of the community but not family
    The Empress - a kind authority figure (higher class)
    The Emperor - a cruel authority figure (higher class)
    The Hierophant - a religious authority figure (higher class)
    The Lovers - a close friend (same class)
    The Chariot - an ambitious stranger
    Strength - also an ambitious stranger
    The Hermit - a hermit (not part of the community)
    Wheel of Fortune - a random stranger
    Justice - authority figure (higher class)
    The Hanged Man - lower class
    Death - nobody, just shit luck
    Temperance - lower class
    The Devil - someone close but under coercion
    The Tower - an anarchic psycho
    The Star - a close family member
    The Moon - close family member
    The Sun - close family member
    Judgement - someone deepy religious
    The World - a town elder

what happened


Wands   Clubs       Air         Artisans    Creativity and will
Coins   Diamonds    Earth       Merchants   Material body or possessions
Cups    Hearts      Water       Clergy      Emotions and love
Swords  Spades      Fire        Nobility    Reason

murder
shame
theft
???

    number determines victim

    Wands - murder
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        page - younger sibling or cousin
        knight - older sibling or cousin
        queen - mother
        king - father
    Coins - something of great value was stolen
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        page -
        knight -
        queen - mother's necklace
        king - father's sword
    Cups - a friend or lover was betrayed
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        page
        knight
        queen
        king
    Swords - someone was shamed so that another may get ahead
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        page
        knight
        queen - mother was raped
        king -

    The Fool -
    The Magician
    The High Priestess
    The Empress
    The Emperor
    The Hierophant
    The Lovers
    The Chariot
    Justice
    The Hermit
    Wheel of Fortune
    Strength
    The Hanged Man
    Death
    Temperance
    The Devil
    The Tower
    The Star
    The Moon
    The Sun
    Judgement
    The World

why

    Wands - for passion
    Cups - for power
    Coins - for money
    Swords - for revenge


    minor
        The Fool
        The Hermit
        Wheel of Fortune
        The Lovers
        Strength
        Temperance
        The Star


    moderate
        The Magician
        The High Priestess
        The Empress
        Justice
        Death
        The Devil
        The Moon
        The Sun

    major
        The Emperor
        Judgement - a prophecy
        The World
        The Chariot
        The Hanged Man
        The Tower
        The Hierophant


=============================

The society

For a democratic-republican society, individual powers are noted, and each is assigned to a particular person


Democracy - Aristocracy - Monarchy

factors
    how many tiers
        1 - egalitarian (decisions made by one person, chosen by the group based on merit)
        1 - egalitarian (decisions made by qualified inviduals (mostly elders))
        1 - egalitarian (all decisions made as a group, only applies to bands)

        one noble family, and everyone else
        2 - decisions made by one person, chosen from among the leading families
        2 - decisions made by representatives of the leading families
        2 - decisions made collectively by the leading families

        one royal family, several noble families, and commoners
        3 - decisions made by monarch
        3 - decisions made by one person from the leading family and representatives from the lower tier families
        3 - decisions made collectively by the single leading family

        one royal family, several noble families, upper commoners (tradesmen), and lower commoners (farmers)
        4 - decisions made by monarch
        4 - decisions made by one person from the leading family and representatives from the lower tier families

    monarch succession
        hereditary
            Eldest sibling - 50%
            Eldest child - 50%
                Primogeniture - 25%
                Preference to firstborn (receives twice as much as the rest) - 25%
                Divided equally - 50%
                    not including illegitimate children - 50%
                    including illegitimate children - 50%
        elected
            chosen from royal family
            chosen from peers
    gender preference
        Agnatic - 25%
        Male-preference - 25%
        Absolute - 25%
        Matrilineal - 25%

    Partibility gender preference if partible and gender preference is male-preference

Aristocracy
    hereditary
    chosen by sovereign
    chosen by peers
    chosen by people
democracy
    by random lot
    elected representative
Monarchy
    hereditary
    elected


Monarchy
    0 - absolute monarchy
    1 - monarchy with some powers ceded to parliament
    2 - monarchy roughly equally sharing powers with parliament
    3 - parliament has most power, monarch has little
    4 - parliament has all power, monarch is figurehead

Republic
    0 - oligarchy, power entirely in hands of a few noble families
    parliament is
    parliament is selected randomly from population



society type
    Wands - nomadic/pastoral
    Cups - tribal/band
    Coins - city state
    Swords - feudal/chiefdom

religion type
    Wands - animism
    Cups - polytheism
    Coins - henotheism
    Swords - monotheism

other factors
    Parliamentary-Monarchic
    Heritibility of titles-Level of obligation

    Note: Sortition (random election) was considered a key component of democracy

    stratification
    leadership type
    authority of women
    succession type

    The Fool - small egalitarian band practicing animism
    The Magician - small chiefdom led by a chief and council, practicing henotheism
    The High Priestess - republic with freedom of religioun
    The Empress - benevolent monarch, monotheistic
    The Emperor - cruel monarch, monotheistic
    The Hierophant - theocracy led by a high priest
    The Lovers - monarchy, polytheistic
    The Chariot - highly militarized monotheistic kingdom
    Strength - militarized and highly stratified chiefdom, polytheistic
    The Hermit - isolated city state, polytheistic
    Wheel of Fortune - triumvirate, random religion
    Justice - parliament, random religion
    The Hanged Man - parliamentary monarchy
    Death
    Temperance
    The Devil
    The Tower
    The Star
    The Moon
    The Sun
    Judgement
    The World

=========================

The self

Society type
    nomadic/pastoral
    tribal/band
    city state
    feudal/chiefdom

Social class
    Nobility
        Paramount lord
        Lesser noble
        Landless noble
    Warrior
        Landed knight
        Middle
        Low
    Merchant / Clergy
        Guild leader
        Middle
        Lower
    Commoner
        Freeman
        Serf
        Slave


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
        return f'{name}, {self.age} year old {self.gender}, {"Alive" if self.alive else "Dead"}, {"Married" if self.married else "Unmarried"}'

    def __init__(self, **kwargs):
        culture = kwargs.get('culture')
        self.culture = culture
        self.name = kwargs.get('name', culture.genName())
        self.family_name = kwargs.get('family_name', culture.genName())

        spouse = kwargs.get('spouse')
        self.spouse = spouse
        if spouse:
            self.married = True
            spouse.married = True
            self.spouses = [spouse]
            if self not in spouse.spouses:
                spouse.spouses.append(self)
                spouse.spouse = self
        else:
            self.spouses = []
            self.married = False
        self.mother = kwargs.get('mother')
        self.father = kwargs.get('father')
        self.siblings = []
        self.children = []
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
            self.orientation = random.choices(
                list(ORIENTATIONS.get(self.gender).keys()),
                weights=list(ORIENTATIONS.get(self.gender).values()))[0]

        self.social_class = kwargs.get('social_class')  # random.choice(culture.social_classes))
        self.wealth = kwargs.get('wealth', random.randint(1, 3))
        self.bonuses = kwargs.get('bonus')

    def relation(self, person):
        if person in self.siblings:
            if person.gender == 'male':
                return 'brother'
            if person.gender == 'female':
                return 'sister'
        if person is self.father:
            return 'father'
        if person is self.mother:
            return 'mother'
        if person in self.children:
            if person.gender == 'male':
                return 'son'
            if person.gender == 'female':
                return 'daughter'
        return 'other'

    @property
    def family(self):
        return self.siblings + [self.mother, self.father]

    def generate_spouse_and_family(self):
        if not self.alive:
            return

        culture = self.culture
        family_name = self.family_name

        if self.married and not self.spouse:
            if self.gender == 'male':
                husband_age = self.age
                wife_age = max(husband_age - int(random.triangular(-2, 14, 3)), 12)
                self.spouse = Person(age=wife_age,
                                     spouse=self,
                                     gender='female',
                                     # family_name=family_name,
                                     culture=culture)
                baby_daddy = self
                baby_momma = self.spouse
            if self.gender == 'female':
                wife_age = self.age
                husband_age = max(wife_age + int(random.triangular(-2, 14, 3)), 12)
                self.spouse = Person(age=husband_age,
                                     spouse=self,
                                     gender='male',
                                     # family_name=family_name,
                                     culture=culture)
                baby_daddy = self.spouse
                baby_momma = self

            if self.infertile or self.spouse.infertile:
                return

            wife_age_at_marriage = int(random.triangular(12, 22, culture.avg_female_marriage_age))
            years_of_marriage = wife_age - wife_age_at_marriage

            children = []
            for age in range(0, years_of_marriage, 2):
                if chance(67):
                    children.append(Person(age=age,
                                           family_name=family_name,
                                           culture=culture))
                if chance(0.4):
                    children.append(Person(age=age,
                                           family_name=family_name,
                                           culture=culture))
            for child in children:
                child.mother = baby_momma
                child.father = baby_daddy
            self.children = children
            self.spouse.children = children

            """
            simplified # children model
            if younger than 30

            d_age = current age - age of marriage

            d_age / 2 births
            2/3 of those children are alive

            so where the age of marriage is 15 and the woman is 27 (d_age = 12)
            6 births

            2-6 children (1/3 to 3/3 of the total)

            random.choices(0, 2, 4, 6, 8, 10)

            at 30 may have
            2 to 7 children

            afterwards
            avg # fewer children once above the age of 30 = (age - 30) / 6

            min = max * 1/3
            """

            # for _ in range(max_children):
            #     pass

    def generate_family(self):
        """
        Generate siblings and parents for this character
        """
        culture = self.culture
        family_name = self.family_name
        # The way this is adopted is culture dependent. Think about it later

        if not self.mother and not self.father and not self.siblings:
            mother_age_at_marriage = int(random.triangular(12, 22, culture.avg_female_marriage_age))
            # On average, 2-4 years older
            father_age_at_marriage = clamp(mother_age_at_marriage + int(random.triangular(-2, 14, 3)), 12, 30)

            mother = Person(age=mother_age_at_marriage, gender='female', family_name=family_name, culture=culture)
            mother.infertile = False
            father = Person(age=father_age_at_marriage, gender='male', family_name=family_name, culture=culture)
            father.infertile = False
            self.mother = mother
            self.father = father

            family_kwargs = {
                'family_name': family_name,
                'culture': culture,
                'mother': mother,
                'father': father
            }

            mother_age_at_birth = random.randint(mother_age_at_marriage, 45)

            # Need to account for widows, widowers, and polygamy

            # total children
            children = []
            # w is the wait time between possible pregnancies, this is culture-dependent and variable based on chance
            w = 2
            # Older siblings
            while mother.age < mother_age_at_birth:
                if chance(pregnancy_chance(mother.age)):  # birth a child
                    if chance(67):  # child survives
                        child = Person(age=0, **family_kwargs)
                        children.append(child)
                    if chance(0.4):  # child is twins
                        if chance(67):  # second child survives
                            child = Person(age=0, **family_kwargs)
                            children.append(child)

                # Age all children
                for child in children:
                    if child is self or not child.alive:
                        continue
                    if chance(death_chance(child.age), 2):
                        child.alive = False
                    else:
                        child.age += 2
                mother.age += 2
                father.age += 2

            if chance(0.4) and chance(67):  # Chance of this person having a twin
                child = Person(age=0, **family_kwargs)
                children.append(child)
            children.append(self)
            sim_age = 0 + (self.age % 2)

            # Chance parents died when or soon after you were born
            if chance(death_chance(mother.age), 2) or chance(childbirth_death_chance(mother_age_at_birth)):
                mother.alive = False
            else:
                mother.age += 2
                # if father.age < 50 and chance(50):  # father remarries
            if chance(death_chance(father.age), 2):  # father dies
                father.alive = False
            else:
                father.age += 2
                # if mother.age < 35 and chance(50):  # Father remarries

            # Younger siblings
            while sim_age < self.age:
                if mother.alive and father.alive and chance(pregnancy_chance(mother.age)):  # birth a child
                    if chance(0.4):  # child is twins
                        if chance(67):  # child survives
                            child = Person(age=0, **family_kwargs)
                            children.append(child)
                        if chance(67):  # child survives
                            child = Person(age=0, **family_kwargs)
                            children.append(child)
                        if chance(childbirth_death_chance(mother.age) * 2):  # Mother dies in childbirth
                            mother.alive = False
                    else:
                        if chance(67):  # child survives
                            child = Person(age=0, **family_kwargs)
                            children.append(child)
                        if chance(childbirth_death_chance(mother.age)):  # Mother dies in childbirth
                            mother.alive = False

                # Age all children
                for child in children:
                    if child is self or not child.alive:
                        continue
                    if chance(death_chance(child.age), 2):
                        child.alive = False
                    else:
                        child.age += 2
                sim_age += 2

                if mother.alive:
                    if chance(death_chance(mother.age), 2):  # mother dies
                        mother.alive = False
                        # print(f'Mother died when you were {sim_age}')
                    else:
                        mother.age += 2
                    # if father.age < 50 and chance(50):  # father remarries
                if father.alive:
                    if chance(death_chance(father.age), 2):  # father dies
                        father.alive = False
                        # print(f'Father died when you were {sim_age}')
                    else:
                        father.age += 2
                    # if mother.age < 35 and chance(50):  # Father remarries

            children.sort(key=lambda r: r.age)
            for child in children:
                child.siblings = [c for c in children if c is not child]
                child.married = False

                # Is or is not married
                if child.alive and child.gender == 'male':
                    if child.age > random.triangular(12, 30, child.culture.avg_male_marriage_age):
                        child.married = True
                if child.alive and child.gender == 'female':
                    if child.age > random.triangular(12, 22, child.culture.avg_female_marriage_age):
                        child.married = True


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
