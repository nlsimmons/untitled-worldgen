from vars import *
import pygame
import random
from pprint import pprint
# from Language import Language, Culture
# from Places import World, Region, Subregion, Locale, Settlement, Road
from Places import Settlement
from Character import Person
# from perlin import NoiseMap
# import copy
# import time

from Worldgen import Worldgen

# random.seed(1)

ORIGIN = (0, 0)


def textbox(text, padding, **kwargs):
    fill = kwargs.get('fill', (0, 0, 0, 127))
    width = kwargs.get('width', 200)

    height = (len(text) + 2) * 20

    surface = kwargs.get('surface', None)
    if not surface:
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        surface.convert_alpha()
        surface.fill(fill)

    px, py = padding

    for line in text:
        rendered_text = font.render(line, True, WHITE)
        surface.blit(rendered_text, (px, py))
        py += 20
    return surface



# n_continents = 2
# n_subcontinents_continents = 2
# subcontinent_area = 50000

"""

Continents 1-3 million

A large country can be 500k in area (2 subcontinents?)

Subcontinents (primary drainage basins) are 250k

Regions 25k

Subregions are 7k

Locales are 1000 sqkm
Each has a major town supported by networks of smaller villages and hamlets

A locale has some percentage amount of forest cover, arable fields, and lakes

"""

# total_area = 10 * 1000000

width, height = 800, 600

n_subcontinents = 10
subcontinent_area = 100000  # 50,000 to 100,000 sqkm
region_area = 25000
subregion_area = 7000
locale_area = 1000

"""
247 acres / sqkm
40 acres minimum per family of 5
= 6 families per sqkm
using wheat

Arable land supports 30 people /sqkm (dependent on crop)
Subsistence foraging/gathering supports 5-10 /sqkm (dependent on.... idk something)
    aka 1/4 the amount of wheat fields
Steppe nomads / pastoralists = 1-5 /sqkm
Desert nomads = 0.1-1 /sqkm

If there is insufficient arable land and abundant forest, farmers may slash and burn (or otherwise chop down forests)
3 acres per farmer per year?

This is dependent on the nutritional value of their crops
Includes a surplus of 10%

Arable land values (Function of terrain and rainfall)
    Assuming Density = 30/arable sqkm

    14% (barren, desolate)
    Density 4

    21% (rocky, chilly)
    Density 6

    28% (cool, dry, swampy)
    Density 8

    43% (hilly, temperate)
    Density 13

    57% (abundant arable land)
    Density 17


Assigned as 100,000 sqkm subcontinental sections
need to somehow account for transition areas

Precipitation

    Very Low - Far inland, mountainous, desert
    Far inland and mountainous regions, and hot/cold deserts
    Home to nomadic bands with a density of 0.25 (1 per 4 sqkm)
    -250 mm

    Low - Steppe / Prairie
    Dry inland regions typically in mountain rainshadow
    250-500 mm

        70-100% Pasture
         0-15% Arable
         0-15% Woodland

    Average - Humid Continental ("Standard")
    "Dry" regions within tropics
    Most continental regions outside tropics
    500-1000 mm

        30-40% Arable
        30-40% Pasture
        30-40% Woodland

    High - Humid Oceanic
    Most continental regions within tropics
    Select coastal regions outside tropics
    1000-2000 mm

        20-30% Arable
        20-30% Pasture
        40-50% Woodland

    Very High - Tropical Monsoon
    Select coastal regions only within the tropics
    2000+ mm

        Lots of arable land if the terrain is favorable
        Thick rainforest
        Relatively little grassland unless created

        95% is split between Woodland/Arable depending on mountains
        5% Pasture

Lakes make up around 3.7% of the total land area
About 10% of that area is lakes larger than 100sqkm (or 1000sqkm)




"""

# n_regions = 100
# region_area = 25000
# subregion_area = 7000
# locale_area = 1000

world = Worldgen.new(n_subcontinents=n_subcontinents,
                     n_continent_seeds=10,
                     subcontinent_area=subcontinent_area,
                     region_area=region_area,
                     subregion_area=subregion_area,
                     locale_area=locale_area,
                     avg_temperature=20,
                     weathermap_scale=200,
                     width=width,
                     height=height,
                     percent_ocean=0,
                     relax_passes=2,
                     populate=True,  # Generate culture groups first, then individual cultures
                                     # Smallest cultural unit should be depdent on total amount?
                     roads=False,
                     rivers=False)


if world.cultures:
    culture = random.choice(world.cultures)
    locales = world.culture_locales(culture)
    locale = random.choice(locales)

    # Taxation starts at 10%, goes higher or lower depending on the government and other factors

    # Need to break down the culture into smaller units
    # Some will be independent, others will be ruled by yet others
    # Also need to differentiate them culturally and linguistically from each other

    # Urbanization rate somewhere between 5-10%
    # Largest settlement will contain 5-10% of that population
    # Remaining population centers follow a zipf distribution
    # Each locale gets a major town, surrounded by smaller towns and villages
    # Each smaller is supported by 5-7 of the next rank down, with a corresponding population
    # And so on as needed
    # Things to instantiate:
    #   Key people in each major city
    #   Families in the starting city
    #       1-3 friendly families, 1-3 rival families, 1-3 friendly people, 1-3 rival people (and their families)
    #       Own family (obviously)
    #   Key people and their family in the starting city
    #   What goods and services are available at what price
    #   The neighboring towns and villages to the starting city

    # Work this based on climate factors
    # Also rivers

    # LAND TYPES
    # For medieval England (oceanic climate):
    #     Arable 35%
    #     Pasture / Meadow 25%
    #     Woodland    15%
    #       May be up to 75% depending on rainfall
    #     Other 25%

    #     Meadow is pasture that is located near rivers
    #     This will vary based on the local climate, more pasture in steppe regions, more forest in wet regions, etc

    you = Person(culture=culture, gender='male', age=20)
    you.generate_family()

    # pprint([you, [(f, you.relation(f)) for f in you.family if f.alive]])

    for s in you.siblings:
        s.generate_spouse_and_family()

    # total_population = sum([r.population for r in locales])
    # urban_population = int(total_population / 10)
    # largest_town_population = int(urban_population / 10)

    locales.sort(key=lambda r: r.population, reverse=True)

    locale = locales[0]
    locale.mark = True
    locale.settle()

    town = locale.capital
    print('')
    pprint('Town Leader:')
    pprint([town.leader, [(f, town.leader.relation(f)) for f in town.leader.family if f.alive]])
    print('')

    print('')
    pprint(f'You begin in the town of {town.name}, home to the {culture.name} people')
    print('')

    # pprint(f'It is bordered by:')
    # pprint(bordered)


pygame.init()

journal = []

while True:
    show_map = False

    print('What would you like to do?')
    print('[1] Show Map')
    print('[2] Open Journal')
    print('[3] Quit')
    print('[4] Pass the time')
    print('[5] Show People')
    print('[6] Travel')
    # Travel to a different village
    # pursue a relationship
    # construct an inspiring tale
    # go on a raid

    # What to do
    """
    events
    animal attack
        hide or fight
    territorial dispute such as poaching
    attack by neighboring village or neighboring herders (for a variety of reasons)
        hide or fight, seek revenge
    internal squabble
        may arbitrate dispute, may go well or poorly based on stats

    choices
        pursue a relationship
        construct an inspiring tale
        go on a raid
        Travel to a distant land, learn their customs, and bring back the knowledge to be used how you see fit
        Install a revolutionary government
        Declare yourself a prophet
        Write a book

    Random events
        Plague (may be brought by merchants, dependent on busyness factor)
        Natural disasters (dependent on location)
        Holy vision
        Antagonized by someone
        Attacked by neighbor
        Wild animal attack
        Attacked by drunk
        Murderer in village
        Recruited for raid (if raiding culture)
        Someone dies or is injured, requests help
        Robbed/attacked at night
        Escort a traveler or merchant
        Noble passes through town
        Accident (someone dies or is injured)

    People menu
        Arbitrate a dispute
        Murder
        Kidnap
        Court
        Befriend
        Antagonize
        Sow rumors
        Challenge for right over something (property, a person, a chiefdom )

    Village menu
        People
        Merchants
        Services
        Find work/administration
        Travel
        Journal
        Practice a skill

    Decisions
        Build a house
        Start a business
        Pray (increases karma)
        Hang around bar (higher chance of meeting travelers)
        Participate in fights
        Try to learn a skill

    Jobs
        Hunt
        Farm
        Craft
        Bounties
        Chop wood
        Odd jobs
        Listen to rumors (potential hidden treasure, paranormal happening, bandits, relationships between people)
        Raid neighboring village
        Become highwayman
        Fish
        Play music

    Journal
        Lists everyone you know and your relationship with them
        Lists potential goals to aim for
            Make money
            Gain renown as a duelist
            Assert your right to rule

    """

    i = input()
    if i == '1':
        show_map = True
    elif i == '2':
        pass
        """
        Show details of your character
        Your birthplace, your name, your family, events that have occurred
        Your stats, your reputation
        Inventory
        """
    # elif i == '2':
    #     for j in journal:
    #         print(j)
    #     while i != 'q':
    #         i = input()
    #         if i != 'q':
    #             journal.append(i)
    elif i == '3':
        pass
        """
        Talk to people
        TODO:
            Establish dialogue trees
                May give friendly, unfriendly, or neutral responses
            Who are you?
            Where are we?
            Who owns these lands / Who's in charge here?
            What's going on in the world?
            What have you been doing?
            Who do you know?
            Anything I can help with?
            Along with:
                Moods (?) Like how are they feeling given current events?
                Personalities (e.g. fuck you, I ain't sayin shit)
        """
        # quit()
    elif i == '4':
        pass
        """
        Visit the shops/traders/craftsmen
        Buy things
        """
    elif i == '5':
        pass
        """
        Visit the local watering hole
        Gamble, brawl, do whatever it is that people do here
        Listen to rumors
        Might be some bounties posted outside
        """
    elif i =='6':
        """
        Travel somewhere else
        You must have sufficient supplies first
        """
        bordered = []
        for place in locale.bordered(world.locales):
            bordered.append(
                (place.names[0], f'{int(locale.distance_to(place))} km away', f'{(locale.distance_to(place) / 5):.1f} hrs away')
            )
    elif i == '7':
        pass
        """
        Choose:
            1 week
            1 month
            6 months
            1 year

            changing of dates and seasons
            production of resources
            migrations
                - anywhere between -50 to 50 per 1000 population (+/- 5% yearly) under normal circumstances
                - numbers may be larger in wartime for migrants fleeing war
                - median/average is more like +/- 3-5
            random events
            diplomatic actions
                marriage, alliances
                war
                raids
            yearly chance of death is applied to you, runs an event you may or may not survive
        """

    # Base travel speed of 5km/hr at 8 hrs a day

    # Government type?
    # Tribal chiefdom
    # Par example

    # 1 headman
    # Based on birth
    # Totally ineffectual

    # 33.00%   Single headman
    #   1 leader
    # 5.00%    2 or more headmen
    #   2 leaders
    # 45.00%   Single leader and council
    #   1 leader
    #   3-5 councilors
    # 10.00%   Council only
    #   3-5 councilors
    # 7.00%    Single leader and subordinates
    #   1 leader
    #   2-4 subordinates (close friends or family)

    # 25% - Authority figures are close kin of the primary leader
    # 25% - Authority figures are kin of the primary leader
    # 35% - Authority figures are based on qualification
    # 15% - Other?

    # 29.00%   Based on birth
    # 37.00%   Elected
    # 22.00%   Office inherited
    # 11.00%   Seniority

    # Town needs to command the resources of smaller towns and villages

    # dd([total_population, [r.population for r in locales]])

    # dd(person)
    # dd(largest_town_population)

    # settlement = Settlement(population=largest_town_population, culture=culture)

    # settlement.name

    """

    10% 500,000 people
        100,000 to 1mil
        5%-50% of all regions
    10% 50,000 people
        10,000 to 100,000
        1-10 subregions
    25% 5000 people
        1 to 10 locales
    45% 1000 people
        1 locale
    10% largest unit is the family (5-10 people)
        100 to 200 in a single locale
        50% of these are organized into trade/military alliances

    """

    if show_map:

        screen_x, screen_y = width, height
        screen = pygame.display.set_mode((screen_x, screen_y))
        font = pygame.font.SysFont(None, 24)

        background = pygame.Surface(screen.get_size())
        background.convert()

        world_surface = pygame.Surface((screen.get_size()))
        world_surface.convert_alpha()
        world_surface.set_colorkey(WHITE)
        world_surface.fill(DARK_BLUE)

        perlin_surface = pygame.Surface((screen.get_size()), pygame.SRCALPHA, 32)
        perlin_surface.convert_alpha()
        perlin_surface.set_colorkey(BLACK)
        # perlin_surface.set_alpha(50)
        # perlin_surface.fill(BLACK)
        # perlin_surface.fill(DARK_BLUE)

        for x in range(width):
            for y in range(height):
                n = world.heightmap.noise_at(x, y)
                color = (int(255 * n), int(255 * n), int(255 * n), int(255 * n))

                try:
                    perlin_surface.set_at((x, y), color)
                except TypeError:
                    print(n)
                    print(world.heightmap._min)
                    print(world.heightmap._max)

        superimpose_subcontinents = False
        superimpose_regions = False

        draw_culture_borders = True
        draw_region_borders = True

        # ======================

        for locale in world.locales:
            color = None
            if locale.type == 'ocean':
                continue
            if locale.type == '':
                continue
            if locale.type == 'lake':
                color = BLUE
            if locale.type == 'land':
                if locale.color:
                    color = locale.color
                elif locale.subregion.color:
                    color = locale.subregion.color
                elif locale.subregion.region.color:
                    color = locale.subregion.region.color
                else:
                    color = GREEN

            if not color:
                continue

            # pprint(locale.type)

            if locale.subregions:
                for dr in locale.subregions:
                    vertices = [(int(x), int(y)) for x, y in dr.points]
                    pygame.draw.polygon(world_surface, color, vertices)
                    # pygame.draw.polygon(world_surface, BLACK, vertices, 1)
            else:
                vertices = [(int(x), int(y)) for x, y in locale.points]
                pygame.draw.polygon(world_surface, color, vertices)
                # pygame.draw.polygon(world_surface, BLACK, vertices, 1)

            # vertices = [(int(node.x), int(node.y)) for node in sr.nodes]
            # pygame.draw.polygon(world_surface, BLACK, vertices, 1)

        # Draw borders
        world.index_borders()
        for b in world.borders.get('t3'):
            if 'coast' in b.type:
                weight = 1
            else:
                continue

            n1, n2 = b.nodes
            n1x, n1y = n1.coords
            n2x, n2y = n2.coords
            pygame.draw.line(world_surface, BLACK, (int(n1x), int(n1y)), (int(n2x), int(n2y)), weight)

        if draw_region_borders:
            if superimpose_subcontinents:
                for subcontinent in world.subcontinents:
                    for b in subcontinent.borders:
                        weight = 3
                        n1, n2 = b.nodes
                        n1x, n1y = n1.coords
                        n2x, n2y = n2.coords
                        pygame.draw.line(world_surface, BLACK, (int(n1x), int(n1y)), (int(n2x), int(n2y)), weight)

            if superimpose_regions:
                for region in world.regions:
                    for b in region.borders:
                        weight = 1
                        n1, n2 = b.nodes
                        n1x, n1y = n1.coords
                        n2x, n2y = n2.coords
                        pygame.draw.line(world_surface, BLACK, (int(n1x), int(n1y)), (int(n2x), int(n2y)), weight)

            if False:
                for region in world.subregions:
                    for b in region.borders:
                        weight = 3
                        n1, n2 = b.nodes
                        n1x, n1y = n1.coords
                        n2x, n2y = n2.coords
                        pygame.draw.line(world_surface, BLACK, (int(n1x), int(n1y)), (int(n2x), int(n2y)), weight)

            for b in world.borders.get('t3'):
                if 'ocean' in b.type or 'lake' in b.type:
                    continue
                elif 'coast' in b.type:
                    weight = 1
                elif 't3' in b.type:
                    weight = 0
                elif 't2' in b.type:
                    weight = 0
                elif 't1' in b.type:
                    weight = 0
                else:
                    continue

                if not weight:
                    continue

                n1, n2 = b.nodes
                n1x, n1y = n1.coords
                n2x, n2y = n2.coords
                pygame.draw.line(world_surface, BLACK, (int(n1x), int(n1y)), (int(n2x), int(n2y)), weight)

        # Draw culture borders
        if draw_culture_borders:
            world.index_culture_borders()
            for b in world.culture_borders:
                weight = 1
                n1, n2 = b.nodes
                n1x, n1y = n1.coords
                n2x, n2y = n2.coords
                pygame.draw.line(world_surface, BLACK, (int(n1x), int(n1y)), (int(n2x), int(n2y)), weight)

        # Draw roads
        for road in world.roads:
            for road_segment in road.segments:
                r1, r2 = road_segment
                r1x, r1y = r1.centroid
                r2x, r2y = r2.centroid
                pygame.draw.line(world_surface, BLACK, (int(r1x), int(r1y)), (int(r2x), int(r2y)), 1)

        # Draw rivers
        for river in world.rivers:
            source_x, source_y = river[0][0].coords

            pygame.draw.circle(world_surface, DARK_BLUE, (int(source_x), int(source_y)), 3)
            for segment in river:
                p1, p2 = segment
                x1, y1 = p1.coords
                x2, y2 = p2.coords
                pygame.draw.line(world_surface, DARK_BLUE, (int(x1), int(y1)), (int(x2), int(y2)), 2)

        # Draw other
        for locale in world.locales:
            if locale.mark:
                x, y = locale.centroid
                pygame.draw.circle(world_surface, BLACK, (int(x), int(y)), 3)
                pygame.draw.circle(world_surface, BLACK, (int(x), int(y)), 6, 1)

        tooltip_size = (250, 100)
        tooltip_anchor = ORIGIN
        alt_tooltip_anchor = (screen_x - tooltip_size[0], screen_y - tooltip_size[1])

    def cursor_tooltip(world, cursor_pos):
        cursor_x, cursor_y = cursor_pos
        text = []

        for locale in world.locales:

            if(locale.maybe_encloses((cursor_x, cursor_y))
               and locale.encloses((cursor_x, cursor_y))):

                if locale.type == 'ocean':
                    return

                try:
                    subregion = locale.subregion
                    region = subregion.region
                    culture = locale.cultures[0]
                    population = world.culture_population(culture)

                    text.append(f'Region: {region.names[0]}')
                    text.append(f'Population: {population}')
                    # text.append(f'Subregion: {subregion.names[0]}')
                    text.append(f'Temperature: {region.temperature}')
                    text.append(f'Culture: {culture.name}')
                    text.append(f'Precipitation: {locale.precipitation}')

                    area = int(sum(o.geoarea for o in world.culture_locales(culture)))
                    density = int(population / area)

                    text.append(f'Locale: {locale.names[0]}')
                    text.append(f'Population: {locale.population}')
                    text.append(f'Area: {area}; Density: {density}')

                    if locale.capital:
                        text.append('')
                        text.append(f'Settlement: {locale.capital.name}')
                        text.append(f'Population: {locale.capital.population}')

                except IndexError:
                    return

                # text.append(f'Regional Cultures: {", ".join(c.name for c in region.cultures)}')
                # text.append(f'Area: {int(region.geoarea)} sqkm')
                # text.append('')
                # # text.append(f'Cultures: {", ".join(c.name for c in region.cultures)}')
                # text.append(f'Population: {region.population}')
                # text.append('')
                # text.append(f'Subregional Cultures: {", ".join(s.name for s in subregion.cultures)}')
                # text.append(f'Local Culture: {locale.cultures[0]}')
                # text.append(f'Population: {locale.population}')

            # if subregion.population:
                #     text.append('')
                #     text.append(f'Subregion: {subregion.names[0]}')
                #     text.append(f'Population: {subregion.population}')
                # text.append(f'Subregional Area: {int(subregion.geoarea)} sqkm')
                # if locale.population:
                #     text.append('')
                #
                # text.append(f'Local area: {int(locale.geoarea)} sqkm')
                return text

    while show_map:
        screen.blit(background, ORIGIN)
        # off_y = (screen_y - world.height) / 2
        # off_x = (screen_x - world.width) / 2
        # off_x = 0
        # off_y = 0
        screen.blit(world_surface, ORIGIN)
        # screen.blit(perlin_surface, ORIGIN)

        # cursor position
        if pygame.mouse.get_focused():

            cursor_x, cursor_y = pygame.mouse.get_pos()
            text = ['x: %s' % int(cursor_x),
                    'y: %s' % int(cursor_y)]
            # text.append('a: %s' % int(world.heightmap.noise_at(cursor_x, cursor_y) * 100))

            cursor_pos_surface = pygame.Surface((75, 75), pygame.SRCALPHA, 32)
            cursor_pos_surface.convert_alpha()
            cursor_pos_surface = textbox(text, (20, 5), surface=cursor_pos_surface, fill=(*BLACK, 127), width=100)
            screen.blit(cursor_pos_surface, (0, screen_y - 75))

            text = []

            try:
                text = cursor_tooltip(world, pygame.mouse.get_pos())
            except (AttributeError, IndexError) as e:
                pprint(e)

            if text:
                tooltip_surface = textbox(text, (20, 20), fill=(*BLACK, 127), width=350)
                tt_anchor = tooltip_anchor

                # if tooltip_surface.get_rect().collidepoint(pygame.mouse.get_pos()):
                #     tt_anchor = alt_tooltip_anchor
                # else:
                #     tt_anchor = tooltip_anchor

                screen.blit(tooltip_surface, tt_anchor)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_map = False
                pygame.display.quit()
