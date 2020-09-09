from vars import *
import pygame
import random
from pprint import pprint
from Places import Settlement
from Character import Person
from Language import Culture


culture = Culture()
you = Person(culture=culture, gender='male', age=40)
you.generate_family()

for s in you.siblings:
    if not s.alive:
        continue
    s.generate_spouse_and_family()
    pprint((s, s.spouse))
    pprint(s.children)
    print('')

quit()
