from math import sqrt
from vars import *
import random

CONSTS = ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r',
          's', 't', 'v', 'w', 'x', 'y', 'z', 'ng', 'th', 'zh', 'sh', 'ch', 'gh',
          'ts', )
VOWELS = ('a', 'e', 'i', 'o', 'u',)

valid_syllables = ('cvc', 'vcv', 'cv', 'vc', 'v', 'c',)

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


class Language:
    def __init__(self, **kwargs):
        self.CONSTS = kwargs.get('CONSTS', random.sample(CONSTS, 20))
        self.VOWELS = kwargs.get('VOWELS', random.sample(VOWELS, 5))
        self.valid_syllables = kwargs.get('valid_syllables',
                                          random.sample(valid_syllables, random.randint(2, 6)))
        self.max_word_length = int(rand_high(1, 6))  # Max number of syllables per word

        # word genders

        self.words = dict()
        for word in SWADESH:
            new_word = None
            while new_word is None or new_word in self.words:
                new_word = self.word(max_word_length=2)
            self.words[word] = new_word

    def word(self, **kwargs):
        _word = ''
        max_length = kwargs.get('max_length', self.max_word_length)
        if max_length == 1:
            syllables = 1
        else:
            syllables = kwargs.get('syllables', int(rand_high(1, max_length)))
        for _ in range(syllables):
            syl_struct = random.choice(self.valid_syllables)
            for part in syl_struct:
                if part == 'c':
                    letter = zipf(self.CONSTS)
                    while len(_word) > 0 and letter == _word[-1]:
                        letter = zipf(self.CONSTS)
                    _word += letter
                if part == 'v':
                    letter = zipf(self.VOWELS)
                    while len(_word) > 0 and letter == _word[-1]:
                        letter = zipf(self.VOWELS)
                    _word += letter

        if len(_word) > 2 and all(v not in _word for v in VOWELS):
            # Words longer than 2 letters need VOWELS
            return self.word(**kwargs)

        return _word

    # def mutate(self):
    #     # Todo - add addition of consonant
    #     # randomly change one consonant to something else
    #     old = new = ''
    #     while not old:
    #         old = random.choice(self.CONSTS)
    #     while not new or new == old:
    #         new = random.choice(CONSTS)

    #     # replace all instances in word list
    #     self.words = [w.replace(old, new) for w in self.words]
    #     new_CONSTS = [new if c == old else c for c in self.CONSTS]
    #     self.CONSTS = list()
    #     for c in new_CONSTS:
    #         if c not in self.CONSTS:
    #             self.CONSTS.append(c)

    # def getPhoneme(self):
    #     pl = [zipf(self.CONSTS), zipf(self.VOWELS)]
    #     random.shuffle(pl)
    #     return ''.join(pl)

    # def newWord(self):
    #     w = ''
    #     ll = self.wordlen - 1
    #     ul = self.wordlen + 1
    #     for _ in range(random.randrange(ll, ul)):
    #         w += self.getPhoneme()

    #     return w

    # def getWord(self):
    #     return random.choice(self.words)

    def name(self):
        word = self.word()
        while len(word) < 2 or all(v not in word for v in VOWELS):
            word += self.word()

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
    Cuisine
    Personality Biases ?
    Family name first/last, and how are names passed down
    Age of marriage (tends to be low unless there's something else at play)
    # traditional crafts (specialty goods)
    # Partible paternity

    The higher the average polygyny rate, the greater the element of gerontocracy and social stratification
    Polyandry is believed to be more likely in societies with scarce environmental resources
    Where polygyny is permitted: incidence of 1/3 to 1/2


    """
    social_classes = []

    def __init__(self, language=None):
        if language:
            self.language = language
        else:
            self.language = Language()
        self.name = self.genName()

        self.family_name_first = random.choice([True, False])
        """

        Some factors influence the marriage rate and age of marriage

        Decision-making
            Absolute
            Joint
            Elder council
            Popular council

        Stratification
            Egalitarian
            Meritocratic (warrior society)
            Hereditary (through wealth)
            Flexible caste
            Strict caste

        Authority of women
            Superior
            Equivalent
            Subservient

        Balance of power between ruler and council
            Absolute monarchy
            Absolute republic (?)

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
            Required to render service and taxes (to various degrees)
            Dictates marriage and other things

        Heritibility of granted titles

        Religion
            0 - animistic - spiritualism
            1 - polytheistic - worship of many gods
            2 - henotheistic - worship of many gods with preference for one
            3 - monolatristic - acknowledgement of many gods but worship of one
            4 - monotheistic - worship of one god alone

        Marriage
            Endogamic
            Exogamic
            Neither?
        Polyandry
            0 - Women may have only one man
            1 - Women may have one primary man and several others
            2 - Women may have multiple men and treat them equally
        Polygyny
            0 - Men may have only one woman
            1 - Men may have one primary woman and several others
            2 - Men may have multiple women and treat them equally
        Honor killing
        Prevalence of serfs and slaves (affected by population)

        """

    def genName(self):
        return self.language.name()
