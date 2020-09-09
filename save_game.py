from vars import *
from Worldgen import Worldgen
from Places import World
import shelve
import sys

filename = 'worlds'
d = shelve.open(filename)

try:
    w = d['world1']
    world = World.deserialize(w)
except KeyError:
    n_regions = 10
    n_divisions = 10
    n_detail = 20
    width, height = 1200, 800
    world = Worldgen.new(n_regions=n_regions,
                         n_divisions=n_divisions,
                         n_detail=n_detail,
                         width=width,
                         height=height,
                         percent_ocean=33,
                         relax_passes=2)

    serialized = world.serialize()

    # world = World.deserialize(serialized)

    # dd(world)

    # dd(world.__dict__)
    d['world1'] = serialized
    d.close()
# dd(world)
