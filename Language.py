from vars import *
from copy import copy
import random

CONSTS = ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r',
          's', 't', 'v', 'w', 'x', 'y', 'z', 'ng', 'th', 'zh', 'sh', 'ch', 'gh',
          'ts', 'dh', )
VOWELS = ('a', 'i', 'o', 'u', 'e', 'y',)

SWADESH = {
    "I", "you", "this", "who", "what", "one", "two", "fish", "dog", "louse",
    "blood", "bone", "egg", "horn", "tail", "ear", "eye", "nose", "tooth",
    "tongue", "hand", "know", "die", "give", "sun", "moon", "water", "salt",
    "stone", "wind", "fire", "year", "full", "new", "name",
}

random.seed(1)

# https://en.wikipedia.org/wiki/Dolgopolsky_list
# https://en.wikipedia.org/wiki/Glottochronology

# Brevity law
# the more frequently a word is used, the ‘shorter’ that word tends to be

"""
Different morphemes for certain contexts
Place, person, plural

sov 45%/ 30%
svo 42%/ 30%
vso 9%/  15%
vso 3%/  15%
osv 1%/  5%
osv 0%/  5%

has long/short VOWELS
has diphthongs
"""


class Phoeneme:
    pass


class Syllable:
    pass


"""
Evolution of languages:
    vowel shifts
    vowel-breaking

"""


class Language:
    """
    15% chance a language does not contain diphthongs
        If it does, number is a triangular distribution of min 1, max 20? with mode 5
        No visible correlation between number of vowels and number of diphthongs

    Frequency of letters as the beginning of a word is also subject to zipf's law
    Preference for fewer vowels (triangular)
    Triangular distribution for number of consonants, midpoint mode

    """

    def __init__(self, **kwargs):
        # Synthesis (avg number of morphemes per word) between 1 and 3
        vowels = []
        n_vowels = int(rand_low(3, len(VOWELS)))
        while len(vowels) < n_vowels:
            i = int(rand_low(0, len(VOWELS)))
            v = VOWELS[i]
            if v not in vowels:
                vowels.append(v)
        self.vowels = vowels

        consts = []
        n_consts = int(rand_low(10, len(CONSTS)))
        while len(consts) < n_consts:
            c = random.choice(CONSTS)
            if c not in consts:
                consts.append(c)
        self.consts = consts

        # self.initial_vowels = copy(self.vowels)
        # random.shuffle(self.initial_vowels)
        # self.initial_consts = copy(self.consts)
        # random.shuffle(self.initial_consts)

        # self.initial_letters = self.vowels + self.consts
        # random.shuffle(self.initial_letters)

        self.has_diphthongs = chance(85)  # Do something similar for consonants as well
        if self.has_diphthongs:
            if len(self.vowels) < 4:
                max_diphthongs = 6
            else:
                max_diphthongs = 20
            n_diphthongs = int(random.triangular(1, max_diphthongs, 5))
            potential_dipthongs = []
            for v1 in self.vowels:
                for v2 in self.vowels:
                    if v1 == v2:
                        continue
                    potential_dipthongs.append(v1 + v2)
            diphthongs = random.choices(potential_dipthongs, k=n_diphthongs)
            self.vowels += diphthongs

        # Syllable types
        self.syllable_types = random.choices(['CVC', 'VC', 'CV', 'V'], k=random.randint(1, 4))

        """
        Genders
        masc, fem, neuter
        or
        animate, inanimate
        """

        # self.max_len_onset = random.randint(1, 3)
        # self.max_len_coda = random.randint(1, 3)

        # word genders

        # self.words = dict()
        # for word in SWADESH:
        #     new_word = None
        #     while new_word is None or new_word in self.words:
        #         new_word = self.word(max_word_length=2)
        #     self.words[word] = new_word

    def word(self, **kwargs):
        # if structure[-1] == 'C':
        #     _word = zipf(self.initial_consts)
        # elif structure[-1] == 'V':
        #     _word = zipf(self.initial_vowels)

        min_syllables = kwargs.get('min_syllables', 1)
        max_syllables = kwargs.get('min_syllables', 5)
        n_syllables = kwargs.get('syllables', int(rand_low(min_syllables, max_syllables)))

        # if len(_word) == 2 or _word[-1] in self.consts:
        #     # add vowels
        #     _word += zipf(self.vowels)
        # else:
        #     # add consts
        #     _word += zipf(self.consts)

        _word = ''

        for _ in range(n_syllables):
            _syllable = ''
            structure = zipf(self.syllable_types)
            # https://en.wikipedia.org/wiki/Syllable#Nucleus

            for s in structure:
                if s == 'C' and len(_syllable) == 0:
                    len_onset = int(rand_lower(0, 2))
                    for _ in range(len_onset):
                        _letter = zipf(self.consts)
                        while len(_syllable) and _syllable[-1] == _letter:
                            _letter = zipf(self.consts)
                        _syllable += _letter
                elif s == 'C':
                    len_coda = int(rand_lower(0, 2))
                    for _ in range(len_coda):
                        _letter = zipf(self.consts)
                        while len(_syllable) and _syllable[-1] == _letter:
                            _letter = zipf(self.consts)
                        _syllable += _letter
                elif s == 'V':
                    _letter = zipf(self.vowels)
                    _syllable += _letter

            _word += _syllable

        return _word

    # def mutate(self):
    #     # Todo - add addition of consonant
    #     # randomly change one consonant to something else
    #     old = new = ''
    #     while not old:
    #         old = random.choice(self.consts)
    #     while not new or new == old:
    #         new = random.choice(CONSTS)

    #     # replace all instances in word list
    #     self.words = [w.replace(old, new) for w in self.words]
    #     new_CONSTS = [new if c == old else c for c in self.consts]
    #     self.consts = list()
    #     for c in new_CONSTS:
    #         if c not in self.consts:
    #             self.consts.append(c)

    def name(self):
        word = self.word(min_syllables=3)
        # while len(word) < 2 or all(v not in word for v in VOWELS):
        #     word += self.word()

        return word.title()


class Culture:
    """
    Band
        20-50 people (a few families)
        Egalitarian
        May be "ruled" by one or several based on merit
    Tribe
        50-150 people
        Controlled by one or several families or elders, based on merit
    Chiefdom
        One or several villages (tribes)
        Controlled by a chief, based on kinship
        Has codified succession and at least 2 social ranks
        A single lineage/family of the elite class becomes the ruling elite of the chiefdom
        Centralized power
        May have lower subservient chiefdoms (would have to follow the 90-10 rule)
        complex social hierarchy consisting of kings, a warrior aristocracy, common freemen, serfs and slaves.

    Nobility
    Priests - 10%? (1% total)
    Warriors

    Tattoos

    Language
    Religion
    Native climate - Determines food
        Desert
        Arid (steppe?)
        Semiarid
        subhumid
        tropical savanna
        tropical rainforest

    Cuisine
        Primary carbohydrates and proteins
        Wheat grows in temperate regions
        Rice - lowland tropical
        Corn - both temperate and tropical
        Millet, sorghum - semiarid desert

    Cash Crops (if any)
        sugar
        coffee
        cocoa
        tobacco
        oil palm
        tea
        cotton
        nuts

    Family name first/last, and how are names passed down
    Age of marriage (tends to be low unless there's something else at play)
    # traditional crafts (specialty goods)
    # Partible paternity

    The higher the average polygyny rate, the greater the element of gerontocracy and social stratification
    Polyandry is believed to be more likely in societies with scarce environmental resources
    Where polygyny is permitted: incidence of 1/3 to 1/2


    """
    social_classes = []

    def __str__(self):
        return self.name

    def __init__(self, **kwargs):
        self.language = kwargs.get('language', Language())
        self.color = kwargs.get('color', random_color())
        self.name = self.genName()

        self.family_name_first = chance(33)

        # Actual age is anywhere between 12 and 25
        self.avg_female_marriage_age = int(random.triangular(12, 22, 15))

        # Actual age is anywhere between 12 and 30
        self.avg_male_marriage_age = int(random.triangular(12, 30, 20))

    def genName(self):
        # Generate a set of common names
        return self.language.name()

        """
        Age difference
        On average, 2-4 years older
        More widely, between -2 and 14 years older

        Some factors influence the marriage rate and age of marriage

        Stratification
            50% - Egalitarian
            20% - Wealth distinction is socially important but does not form distinct social classes
            20% - Distinction between 2 classes of hereditary nobility and commoners
            10% - Caste system
                63% - One or more occupations are viewed as outcastes and strictly endogamous (smiths, leatherworkers)
                20% - Ethnic stratification
                17% - Occupation and ethnicity are linked together into a rigid caste hierarchy

        Political vs Religious leaders
            25% - Much overlap
            37% - Some overlap
            37% - Distinct

        Leaders may be
            85% - Only men
            15% - Also women

        Leadership at local level
            10% - No central leadership (probably just for low population villages)

            33% - Single headman
            5% - 2 or more headmen
            45% - Single leader and council
            10% - Council only
            7% - Single leader and subordinates

        Nepotism
            25% - Authority figures are close kin of the primary leader
            25% - Authority figures are kin of the primary leader
            35% - Authority figures are based on qualification
            15% - Other?

        Perception of leadership
            25% - Purely self-interest
            20% - Neutral
            55% - Basically benevolent

        Checks on leaders' power
            22% - Community backing is highly important
            44% - Secures substantial support before taking action
            28% - Checks exist to discourage tyranny
            6% - Little to no checks

        How are poor leaders deposed?
            20% - No formal leadership structure, power is lost when support is lost

                20% - Rebellion only
                30% - Institutions exist, usually by elites
                50% - Not removed but lose influence and are ignored

        How leaders use their authority
            28% - Frequently act independently
            30% - Occasionally act independently
            42% - Pursues organized and structured group action

        Leadership in battle
            45% - Official battle authority exists
            45% - Informal leader followed purely of respect
            10% - None

        Size of largest political unit
            10% - Family heads do not acknowledge any higher authority
                50% - Part of an organization maintaining peace through trade or military alliance
            45% - Autonomous communities less than 1500
                10% - Part of an organization maintaining peace through trade or military alliance
            25% - Minimal states between 1500 and 10,000
            10% - Little states between 10,000 and 100,000
            10% - Large states more than 100,000 in size

            10% - Forms an autonomous region of another state

        Number of regions per culture
            10% 500,000 people
                2-20 regions
            10% 50,000 people
                1-10 subregions
            25% 5000 people
                1 to 10 locales
            45% 1000 people
                1 locale
            10% largest unit is the family (5-10 people)
                100 to 200 in a single locale
                50% of these are organized into trade/military alliances

        Land area of cultures
            10% 10 regions @ 6k sqkm/region
            10% 1 region @ 6k sqkm/region
            25% 0.5 of a subregion (2 in a subregion) @ 12k sqkm/subregion
            40% 0.10 or less of a subregion @ 12k sqkm/subregion
            10% family units only

        Female authority
            8% - No more than standard

            7% - More authority in marriage
            17% - Females have economic power
            30% - Females have political power

        Primary source of political power
            50% - Control of the means of production
            50% - Other

        Hunter-gatherer communities =========================

        Power of shamans relative to laymen
            35% - Exclusive to shaman/priests/etc
            22% - Greater magnitude of power
            5% - Greater power due to experience
            33% - Greater power and wider range of powers
            5% - Different but not greater powers, shamans are just specialists

        Crime and punishment
            15% - No arbitration
            57% - Third party arbitration
            28% - Village leadership punishes crimes

        Nomadic?
            30% - Sedentary
            70% - Some form of nomadic/seminomadic/pastoral

        Density
            50% - 5-100    /sqkm
            35% - 100-500  /sqkm
            10% - 500-1000 /sqkm
             5% - 1000-5000/sqkm

        Family/Household size
            Mode 7
            Min 3
            Max 20

        Use of money
            70% - No
            10% - Rarely
            20% - Common

        10% - The largest settlement is a religious center
        90% - No significantly large settlements

        Below a mean temperature of 0 C, population density is limited to under 0.5 /sqkm (500/1000sqkm)

        Local head of authority
            17% - Senior male
            50% - Meritocratic
            30% - Formal council with a council head
            3% - Neighborhood level organization

        Relation to neighboring groups
            72% - Autonomous, neighbors also autonomous
            10% - Autonomous, but part of more complex hunter-gatherer system
            18% - Component of larger non-hunter-gatherer system

        Hunter-gatherer band class distinction
            67% - Egalitarian
            25% - Only wealth distinction
            8%  - Hereditary classes

        Typology
            8% - Mounted hunters
            5% - Agriculturalists
            8% - Mutualists
            40% - Egalitarian, no leadership
            7% - Egalitarian, with leadership
            23% - Ranked wealth
            8% - Ranked elites

        Permanent community structures
            72% - None
            11% - None, ceremonies performed in host's residence
            6% - Sweat lodge
            7% - Dance house
            4% - Dance house and sweat lodge

        Prerogatives of leadership
            56% - No special treatment
            18% - Messengers only
            13% - Messengers and personal speaker (talking chief)
            10% - Some relief from subsistence, gifts from the people, preference given to wife
            3% - Complete relief from subsistence, visible symbols, permanent guard, other benefits

        Trade
            30% - Does not import food
            50% - 90% or more of food is grown locally
            20% - 50% or more of food is grown locally

        Gathering as a proportion of food supply
            10% - None
            65% - < 10 pct food supply
            25% - < 50 pct , and less than any other single source, incl. trade

        Gathered food sources
            10% - Wild Animal products
            10% - Wild Herbs, Leaves, Blossoms
            5% - Tree Pith, e.g., Sago
            5% - Wild Roots or Tubers
            35% - Wild Fruit, seeds, nuts, berries
            35% - Two or more of the above

        Arranged marriages
            34% - Wife must consent
            38% - Wife is consulted
            28% - Wife is not consulted

            43% - Husband must consent
            40% - Husband is consulted
            17% - Husband is not consulted

        Authority in marriage decisions
            5% - Only groom may initiate or refuse
            34% - Groom has more say
            58% - Both have equal say
            4% - Bride has more say

        Mourning period for widows
            10% - Remarry ASAP
            10% - 1 to 2 weeks
            20% - 2 months to 1 year
            45% - More than 1 year
            15% - No remarriage

        Degree of marriage celebration
            7% - None
            28% - Minor celebration, gift exchange
            26% - Moderate celebration
            38% - Large celebration

        On average, in a polygynous society, 20% of men will have multiple wives,
            and 30% of women will be in a polygynous marriage

        Marriage payments (check against others)
            7% - Woman exchange
            47% - Large bride price
            13% - Bride service
            13% - Token bride price
            13% - Gift exchange
            8% - Dowry

        Polygyny (check against others)
            24% - Over 20% of marriages are polygynous
            40% - Under 20% (more than 0) marriages are polygynous
            37% - Monogamous

        Reaction to premarital pregnancy
            15% - No bad consequences
            30% - Disapproval, possibly forced into marriage
            40% - Significant disapproval, less support
            15% - Ostracization, permanent loss of support

        Where children sleep
            60% - Entire family together
            12% - Separate bedroom
             5% - Near but outside parents' house
            23% - Separate house

        Segregation by sexes of children
            72% - Sleep in same room/bed
            26% - Separate rooms/beds
             2% - Separate houses

        Segregation by sexes of teens
            36% - Sleep in same room/bed
            34% - Separate rooms/beds
            30% - Separate houses

        Wifesharing
            60% - None
            4% - For any reason
            10% - Only for specific groups
            5% - Only for specific men
            7% - Occasionally for graitification
            3% - For economic benefit (payment for wife?)
            11% - For other reasons

        Acceptance of rape
            23% - Accepted/ignored
            10% - Ridiculed
            20% - Mildly disapproved
            46% - Strongly disapproved

        Sexual aggression of men
            8% - Shy
            50% - Forward verbally
            17% - Forward physically
            10% - Forward, occasionally hostile
            15% - Forward, typically hostile

        General levels of aggression by gender
            40% - Roughly equal
            30% - Men more aggressive
            30% - Men much more aggressive

        55% - Widows are not isolated
        45% - Widows are isolated

        91% - Widows are marked
         9% - Widows are not marked

        65% - Widowers are not isolated
        35% - Widowers are isolated

        13% - Widowers are not marked
        87% - Widowers are marked

        Fear of ghosts
            17% - Absent
            83% - Present
                 5% - Very low
                20% - Low
                15% - Moderate
                38% - High
                22% - Very high

        Amount of property of the deceased destroyed
            20% - None
            30% - Little
            20% - Some
            25% - Much
             5% - Most/all

        Name taboo for deceased
            50% - None
            25% - Taboo exists
            25% - Taboo exists and is very strong

        Succession - May always be contested, may include appanage
            Elective - 50%
            Hereditary - 50%
                Primary heir
                    Eldest sibling - 50%
                    Eldest child - 50%
                        Partibility
                            Primogeniture - 25%
                            Preference to firstborn - 25%
                            Divided equally - 50%
                                including illegitimate children
                        Partibility gender preference (?)
                Gender Preference
                    Agnatic - 25%
                    Male-preference - 25%
                    Absolute - 25%
                    Matrilineal - 25%

        Level of obligation to one's liege
            None, fully revokable
            Gifts are exchanged in both directions
            Only tribute
            Required to render service and taxes (to various degrees)
            Dictates marriage and other things

        Heritibility of granted titles

        Religion
            0 - animistic - spiritualism
            1 - polytheistic - worship of many gods
            2 - henotheistic - worship of many gods with preference for one
            3 - monotheistic - worship of one god alone

        Bride price (primary)
            50% - Significant bride price in the form of livestock, goods, or money
            10% - Significant bride price in the form of labor
            5%  - Symbolic bride price only
            5%  - Exchange of gifts between families
            5%  - Exchange of another woman
            20% - No significant exchange, only gifts
            5%  - Property given from bride's family (dowry, more common in patrilineal societies)

            20% - Alternate bride price is possible
                12% - Goods or money
                50% - Labor
                15% - Symbolic only
                8% - Exchange of another woman
                3% - None
                12% - Dowry

        Bride price (alternate)
            2% - Wealth
            10% - Labor
            3% - Token

        Marital residence
            65% - Patrilocal (with or near husband's family)
            10% - Matrilocal (with or near wife's family)
            15% - Ambilocal (optionally either)
            5% - Neolocal (apart from both)

        In gatherer societies, between 1 and 5 families may live in the same building (?)

        Trance belief
            20% - No belief in trance or possession
            80% - Belief in trance or possession
                75% - Belief in possession
                25% - Belief in trance, but none in posession

        Premarital sex (female)
            46% - Universal
            17% - Moderate
            14% - Occasional
            21% - Uncommon

        Premarital sex (male)
            58% - Universal
            17% - Moderate
            10% - Occasional
            12% - Uncommon

        Initiator of premarital sex
            16% - Women always
            30% - Both equally
            16% - Men > Women
            36% - Men always

        Opinion of extramarital sex
            11% - Permitted
            44% - Husband only
            22% - Forbidden but women punished more
            22% - Forbidden

        Opinion of homosexuality
            22% - Accepted/ignored
            10% - None
            15% - Ridiculed, no punishment
            10% - Mildly disapproved
            42% - Strongly disapproved

        Cousin marriage
            40% - Any cousin permitted
            33% - First cousin forbidden, second cousin permitted
            27% - First and second cousin forbidden

        Post partum sex taboo
            22% - Less than 1 month
            33% - 1 month to 6 months
            10% - 6 months to 1 year
            20% - 1 year to 2 years
            15% - More than 2 years (Up to 4? Idk)

        Severity of incest taboo
            69% - Only affects offenders
                40% - None or mild, such as a fine
                15% - Moderate, sickness or bad luck
                45% - Severe, death or exile
            31% - Punishment affects entire kin group

        Political succession
            10% - Acephalous
            90% - Other

            50% - Nonhereditary
                10% - Seniority
                15% - By status
                75% - Election or other consensus
            50% - Hereditary
                75% - Patrilineal
                    75% - Son
                    25% - Brother
                25% - Matrilineal
                    50% - Sister's son
                    50% - Younger brother

        Polygyny
            15% - Monogyny
            85% - Polygyny
                Incidence
                    45% - Polygyny (permitted, under 25% incidence)
                    15% - Polygyny (sororal, wives cohabitate)
                    85% - Polygyny (non-sororal, do not cohabitate)
        Polyandry
            Yes - 10%

        Maximum number of wives/concubines
            40% - 3 or less
            38% - 4-10
            13% - 11-100
             8% - More than 100

        Despotism (The degree to which the head of the social hierarchy is immune from scrutiny)
            85% - Absent
            15% - Present

        Warfare =============================================

        Frequency overall
            25% - Absent or rare
            12% - Once every 3-10 years
            12% - Once every 2 years
            12% - Once a year, but seasonal
            38% - Constantly

        Internal warfare
            42%  - Absent or rare
            12% - Once every 3-10 years
            9% - Once every 2 years
            11% - Once a year, but seasonal
            25%  - Constantly

            Outcomes
                44% - Defeated remain in their territory
                10% - Defeated sometimes remain, land is rarely used
                26% - Defeated sometimes remain, land is sometimes used
                3% - Defeated usually do not remain, land is sometimes used
                16% - Defeated usually do not remain, land is usually used

        External warfare
            36% - Absent or rare
            15% - Once every 3-10 years
            11% - Once every 2 years
            8% - Once a year, but seasonal
            32% - Constantly

        Forms of tribute
            35% - None
            65% - Some
                6% - Corvee labor
                31% - Money
                12% - Mobile goods
                50% - Several of the above

        Burden of demanded tribute
            9% - Sporadic, not burdensome
            32% - Regular, not burdensome
            59% - Regular, burdensome

        Male superiority ideology
            57% - None
            10% - Weak factor
            33% - Strong factor in all gender relations

        Trust inculcated in children
            32% - General mistrust
            40% - Mistrust restricted to certain groups
            28% - General trust

        Importance of honesty in children
            4% - Dishonesty generally accepted
            4% - Dishonesty accepted depending on towards whom
            19% - Honesty is valued
            73% - Honesty is valued, dishonesty is punished

        Legitimacy of power
            29% - Based on birth
            37% - Elected
            22% - Office inherited
            11% - Seniority

        Raiding - A raiding party has a leader and from as few as five to as many as 50 people.
             5% - Raids do not occur
            35% - 0-1 times per year
            30% - 2-4 times per year
            30% - 4 or more times per year

        Raiding Frequency
            1-10
            once a year to once a month
            People are more likely to join a raid if they are poor and it has been a long time since the last raid
                (least likely if there has been a raid in the last month, most likely if more than a year)

            These are correlated with each other, and the relative magnitudes can be thought of as a
            quality of the aggression (?) of that society

            Defending (unsure of what to do with this information)
                15% - Rarely or never raided
                50% - Raided 2-4 times per year
                35% - Raided 4 or more times per year

            Ceremony
                20% - None
                5% - Only for preparation
                30% - Only afterwards
                45% - Both before and after

            Justifications
                60% - Wife stealing
                50% - For loot
                30% - For slaves
                35% - For prestige
                15% - For visions / dreams
                100% - Avenging the death of a fallen warrior
                65% - Avenging poaching (hunting on someone else's land)

        House and corpse
            5% - Dying person removed from house before death
            68% - Corpse removed from house after death
            24% - Corpse removed immediately after death
            2% - Corpse and house are burned

        House after death
            2% - No special treatment
            49% - Destroyed, burned, or abandoned permanently
            6% - Torn down and moved
            44% - Abandoned temporarily

        Sacrifice at death
            54% - No special treatment
            30% - Dogs and other domesticated killed or given away
            13% - Slaves killed or freed
            3% - Both

        Punishment for extramarital sex (for the woman)
            9% - None or mild (fine or warning)
            5% - None or mild and she may be killed
            11% - Moderate (beating or jail)
            26% - Moderate and she may be killed
            15% - Divorce
            9% - Divorce and she may be killed
            15% - Severe punishment (permanent damage) and she may be killed
            9% - Death penalty

        Overlap between religious and political power (at highest governmental level)
            25% - None
            25% - Religious heads participate in decision making
            50% - Heads of government are religious heads

        Higher population density
            Higher levels of inequality
            Higher levels of sedentism
            Higher reliance on agriculture

        Agriculture
            55% - Cereal grains
            20% - None
            20% - Roots, tubers
            5%  - Tree fruits

        Primary crops
            25% - No agriculture
            75% - Agriculture
                3.33% - Barley
                16.67% - Maize
                13.33% - Millet
                5.00% - Dry rice
                11.67% - Wet rice
                8.33% - Wheat
                1.67% - Breadfruit
                8.33% - Cassava
                3.33% - Potato
                1.67% - Sweet potato
                6.67% - Taro
                8.33% - Yams
                3.33% - Plantains
                1.67% - Dates
                3.33% - Coconut
                3.33% - Animal fodder
            30% use irrigation
            70% do not

        Average village size
            22% - Less than 50
            22% - Between 50 and 100
            20% - Between 100 and 200
            15% - 200-400
            12% - 400-1000
            10% - 1000+

        Primary settlement type
            7% - Nomadic
            25% - Seminomadic (nomadic, seasonally settles for winter)
            13% - Neighborhoods, dispersed family dwellings
            10% - Small hamlets (Under 50 people)
            45% - Compact, permanent villages

        Games
            25% - Physical skill only
            55% - Strategy only
            10% - Both
            10% - Both, and games of chance

        High gods
            35% - No high god
            35% - High god unconcerned with humans
            5% - High god concerned with humans but not with morality
            25% - High god concerned with human morality

        Levels of organization
            45% - 0 i.e. Autonomous bands and villages only (about 50% chance for these to be rigid/flexible)
            30% - 1 i.e. Petty chiefdom (1 subregion)
            15% - 2 i.e. Larger chiefdom (1 region)
            7%  - 3 i.e. Structured state
            3%  - 4 i.e. Large state

        Highest level of community organization
            32% - Independent family
            55% - Extended family
            13% - Clan-barrio

        Plow animals
            85% - None
            15% - Yes

        Livestock
            25% - None, only small animals like dogs and fowl
            10% - Only pigs
            15% - Sheeps, goats, maybe pigs?
            5%  - Horses, donkeys
            2%  - Deer
            2%  - Camels, alpacas
            40% - Bovines

        Milking
            32% - Yes
            68% - No

        Dominant food source
            9% - Gathering
            10% - Fishing
            6% - Hunting
            6% - Pastoralism
            55% - Extensive agriculture (over a large area)
            12% - Intensive agriculture

        Exogamous clans
            80% - No exogamous clans
            20% - Exogamous clans
                80% - Not segmented into barrios (subclans?)
                20% - Segmented into barrios

        Endogamy
            25% - Endogamic
            60% - Exogamic
            15% - Agamous

        Descent
            45% - Patrilineal
            40% - Bilineal
            15% - Matrilineal

        Honor killing
        Prevalence of serfs and slaves (affected by population)
        concept of face, mutual obligation, utang na loob, guanxi

        Slavery
            50% - Yes
                35% - Children of slaves are born free
                65% - Children of slaves are born slaves
            50% - No

        Belief in reincarnation
            63% - None
            20% - Some
            17% - Strong

        Funerals held in groups
            66% - No
            34% - Yes

        In the hypothetical presence of a strong, worldwide monotheistic religion
            67% - Indigenous beliefs
            14% - Adoption of that religion
            18% - Superficial adoption

        Ceremonies
            40% - Predominantly sacred
            14% - Predominantly profane
            46% - Can be either

        Professions ========================================

        Hunting - Almost always exclusively men, occasionally women may participate (2%)
            10% - Birds only
            20% - Small mammals only
            40% - Large game only
            30% - Varied

        Metalworking
            50% - Absent or unimportant
            50% - Performed by specialists (men only)

        Weaving
            50% - Absent or unimportant
            50% - Exists
                15% - Performed by specialists
                85% - Practiced by everybody
                    30% - Men only
                    2% - Men more than women
                    27% - both
                    2% - Women more than men
                    58% - Women only

        Leatherworking
            25% - Absent or unimportant
            75% - Exists
                15% - Performed by specialists
                85% - Practiced by everybody
                    46% - Men only
                     2% - Men more than women
                     6% - Both
                     5% - Women more than men
                    40% - Women only

        Potterymaking
            35% - Absent or unimportant
            65% - Exists
                15% - Performed by specialists
                85% - Practiced by everybody
                    10% - Men only
                    1% - Men more than women
                    3% - Both
                    3% - Women more than men
                    83% - Women only

        Boat building
            38% - Absent or unimportant
            62% - Exists
                10% - Performed by specialists
                90% - Practiced by everybody
                    93% - Men only
                    3% - Men more than women
                    2% - Men and women equally
                    1% - Women only

        House building
            7% - Performed by specialists
            93% - Performed by everybody
                63% - Men only
                13% - Men more than women
                10% - Men and women equally
                 2% - Women more than men
                12% - Women only

        Gathering
            25% - Absent or unimportant
            75% - Performed by everyone
                4% - Men only
                3% - Men more than women
                12% - Men and women equally
                27% - Women more than men
                53% - Women only

        Hunting
            9% - Absent or unimportant
            91% - Present
                3% - Specialists
                97% - Everyone
                    98% - Men only
                     2% - Men more than women

        Fishing
            21% - Absent or unimportant
            79% - Present
                4% - Specialists
                96% - Everybody
                    48% - Men only
                    32% - Men more than women
                    14% - Men and women equally
                     3% - Women more than men
                     3% - Women only

        Animal husbandry
            40% - Absent or unimportant
            60% - Present
                40% - Men only
                23% - Men more than women
                23% - Men and women equally
                 4% - Women more than men
                 9% - Women only

        Agriculture
            25% - Absent
            75% - Present
                10% - Only men
                23% - More work by men
                32% - Equal
                31% - More work by women
                 4% - Only women


        """
