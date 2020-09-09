from vars import *
from Language import Language, Culture
from Character import Person
import random
import math

random.seed(1)

"""

Resources
# https://en.wikipedia.org/wiki/Cereal#Production
# wheat, barley, corn, rice, sorghum, millet, oats, rye, bananas,
#   potatoes, cassava, soybeans, sweet potato, yam, plantain
# tobacco, cotton, spices, coffee, rapeseed, tea,
# https://en.wikipedia.org/wiki/Livestock#Types
# sheep, cattle, horses, dogs, cats, donkeys, yak, buffalo, reindeer, camel, llama, alpaca, pig, rabbit


self.water = random.randint(0, 100) < params.get('water', 0)
self.forest = random.randint(0, 100) < params.get('forest', 0)
self.hills = random.randint(0, 100) < params.get('hills', 0)

Villages have will have disputes with their neighbors
Think of a classification scheme for these disputes
    Border dispute (this would be for larger entities)

Figure out combat and generalship

# reputation - the perception of others about your abilities, can be faked,
#   but will need to be backed up by subterfuge or luck
#   is tracked per location
"""

"""
TODO:
    Economics
    Leaders,
    Power structure
        "leadership": ("democratic", "single_elder", "multiple_elder", "chiefdom"),
    Role of women
        patriarchal, matriarchal, egalitarian, other?
    Succession
        Matrilineal / Patrilineal / Cognatic
    Native plants, animals, other resources
    Sedentism
        full, transhumant, nomadic
    Violence - Dependent on local availability of resources
        low, moderate, high
"""


class Node:
    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __init__(self, point, world):
        self.x, self.y = point
        self.coords = point
        self.world = world
        self.regions = set()
        self.borders = set()
        self.river_count = 0

    @property
    def elevation(self):
        try:
            return self._elevation
        except AttributeError:
            if any(r.type == 'ocean' for r in self.regions):
                elevation = 0
            else:
                elevation = int(sum(r.elevation for r in self.regions) / len(self.regions))
            self._elevation = elevation
            return elevation

    @property
    def precipitation(self):
        try:
            return self._precipitation
        except AttributeError:
            precipitation = int(sum(r.precipitation for r in self.regions) / len(self.regions))
            self._precipitation = precipitation
            return precipitation

    def neighbors(self, type=None):
        _neighbors = []
        for b in self.borders:
            if type and type not in b.type:
                continue
            for n in b.nodes:
                if n is not self:
                    _neighbors.append(n)
        if type and not _neighbors:
            return self.neighbors()
        return _neighbors


class Border:
    def __init__(self, node1, node2, world):
        self.nodes = (node1, node2)
        node1.borders.add(self)
        node2.borders.add(self)
        self.world = world
        self.type = ''

    @property
    def between(self):
        try:
            return self._between
        except AttributeError:
            node1, node2 = self.nodes
            self._between = [r for r in node1.regions if r in node2.regions]
            return self._between


class Road:
    def __init__(self, segments, connects):
        self.segments = set(segments)
        self.connects = set(connects)

        for r1, r2 in segments:
            r1.road = self
            r2.road = self
            self.connects.add(r1)
            self.connects.add(r2)

    def add(self, segments):
        for r1, r2 in segments:
            r1.road = self
            r2.road = self
            self.connects.add(r1)
            self.connects.add(r2)


class Region:
    def index(self, world):
        for p in self.points:
            node = world.node_at(p)
            node.regions.add(self)
            self.nodes.append(node)

    def flood_select(self, regions, types, result_set=[]):
        """
        Get the flood-fill set of regions of the same type as the input
        """
        result_set.append(self)
        regions = [r for r in regions if r not in result_set]
        bordered = self.bordered(regions, exclude_ocean=False)
        for b in bordered:
            if b in result_set:
                continue
            if b.type in types:
                # pprint([r.centroid for r in result_set])
                # # pprint(types)
                result_set.append(b)
                result_set += b.flood_select(regions, types, result_set)
        return list(set(result_set))

    def __init__(self, points, **kwargs):
        world = kwargs.get('world')
        self.world = world
        self.populace = None
        self._populated = False
        self.population_allotment = 0

        self.points = points
        self.nodes = []
        self.centroid = get_midpoint(points)
        self.subregions = set()
        self.type = ''
        self.rivers = set()

        self.cultures = []
        self.names = []

        self.color = None
        self.bound = False

    def populate(self, population, culture):
        """
        Populate region
        """
        if self.type == 'ocean':
            return
        self._populated = True

        population_pool = population
        # if this region is empty and can be filled entirely by the population pool, do that
        if not self.population and population_pool >= self.population_allotment:
            # Assume this culture just fills up the entire region
            #   so specifics aren't calculated until necessary
            self.color = culture.color
            self.cultures.append(culture)
            self.names.append(culture.genName())
            for s in self.subregions:
                s.populate(s.population_allotment, culture)
            self.populace = Populace(culture=culture, population=self.population_allotment)
            return

        while population_pool > 0:
            # include in occupied subregions the subregions that are occupied externally to the current region
            occupied_subregions = self.world.culture_subregions(culture)

            # get all subregions that are not fully populated
            if occupied_subregions:
                unfilled_subregions = []
                for subregion in occupied_subregions:
                    unfilled_subregions += [
                        r for r in subregion.bordered(self.subregions) if r.population < r.population_allotment
                    ]

                if len(unfilled_subregions) > 1:
                    bordered_count = [[r, unfilled_subregions.count(r)] for r in set(unfilled_subregions)]
                    max_bordered = max(r[1] for r in bordered_count)
                    most_bordered = [r[0] for r in bordered_count if r[1] == max_bordered]
                    unfilled_subregions = most_bordered

            else:
                unfilled_subregions = [
                    r for r in self.subregions if r.type == 'land' and r.population < r.population_allotment
                ]

            # if there are none, finish prematurely
            if not unfilled_subregions:
                return

            # select one at random
            current_subregion = random.choice(unfilled_subregions)

            # populate
            allotment_remaining = current_subregion.population_allotment - current_subregion.population
            pop = min(allotment_remaining, population_pool)
            population_pool -= pop
            current_subregion.populate(pop, culture)

            # if population was successful
            if culture in current_subregion.cultures and culture not in self.cultures:
                # add to the list of occupied subregions
                self.cultures.append(culture)
                self.names.append(culture.genName())

    @property
    def population(self):
        if not self._populated:
            return 0
        if self.populace:
            return self.populace.population
        else:
            # check population of constituent regions
            return sum(r.population for r in self.subregions)

    @property
    def elevation(self):
        try:
            return self._elevation
        except AttributeError:
            if self.type == 'ocean':
                elevation = 0
            else:
                cx, cy = self.centroid
                elevation = self.world.heightmap.noise_at(cx, cy) * 100
                if self.type == 'coast':
                    elevation /= 2
            self._elevation = int(elevation)
            return self._elevation

    @property
    def precipitation(self):
        """
        Elevation scale should be 0 to 3000 m with mode 300-400
        Precipitation scale should be 0-2000(mm/yr) with mode 500(?)
        How do I make Perlin noise do this?
        """
        try:
            return self._precipitation
        except AttributeError:
            cx, cy = self.centroid
            precipitation = self.world.weathermap.noise_at(cx, cy) * 2000
            # if precipitation > 1800:
            #     precipitation = 1800 + ((precipitation - 1800) / (200 / 2200))
            self._precipitation = int(precipitation)
            return self._precipitation

    @property
    def borders(self):
        try:
            return self._borders
        except AttributeError:
            _borders = []
            for j in range(len(self.nodes)):
                i = j - 1
                _borders.append(Border(self.nodes[i], self.nodes[j], world=self.world))
            self._borders = _borders
            return _borders

    @property
    def bounds(self):
        try:
            return self._bounds
        except AttributeError:
            min_x = min(x for x, y in self.points)
            max_x = max(x for x, y in self.points)
            min_y = min(y for x, y in self.points)
            max_y = max(y for x, y in self.points)
            self._bounds = {
                'min_x': min_x,
                'max_x': max_x,
                'min_y': min_y,
                'max_y': max_y,
            }
            return self._bounds

    def maybe_encloses(self, point):
        x, y = point
        if(x < self.bounds['min_x']
           or x > self.bounds['max_x']
           or y < self.bounds['min_y']
           or y > self.bounds['max_y']):
            return False
        return True

    def encloses(self, point):
        point_x, point_y = point
        """
        Y-value of our target point is within the range [verty[j], verty[i]).
        X-value of our target point is below the linear line connecting the point j and i.
        """
        n = len(self.points)
        c = False
        for j in range(n):
            i = j - 1
            x1, y1 = self.points[i]
            x2, y2 = self.points[j]

            if(((y1 > point_y) != (y2 > point_y))
               and point_x < ((x2 - x1) * (point_y - y1) / (y2 - y1) + x1)):
                c = not c
        return c

    @property
    def area(self):
        try:
            return self._area
        except AttributeError:
            corners = self.points

            n = len(corners)
            area = 0.0
            for i in range(n):
                j = (i + 1) % n
                area += corners[i][0] * corners[j][1]
                area -= corners[j][0] * corners[i][1]
            area = abs(area) / 2.0
            self._area = area
            return area

    @property
    def geoarea(self):
        return self.area / (self.world.scale ** 2)

    def bordered(self, regions, exclude_ocean=True):
        _bordered = []
        for region in regions:
            if region is self or region in _bordered:
                continue
            if exclude_ocean and region.type == 'ocean':
                continue
            matches = 0
            for point in region.points:
                if point in self.points:
                    matches += 1
                    if matches >= 2:
                        _bordered.append(region)
                        break
        return _bordered

    def distance_to(self, region):
        """
        Calculates distance between the centroid of this region and the input region
        in units of km
        """
        x0, y0 = self.centroid
        x1, y1 = region.centroid
        return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2) / self.world.scale


class Subregion(Region):
    """
    Representation of a region with an area of about 1000 sqkm
    """

    def __init__(self, *args, **kwargs):
        self.locales = set()
        super().__init__(*args, **kwargs)

    def populate(self, population, culture):
        """
        Populate subregion
        """
        if self.type == 'ocean':
            return
        self._populated = True

        population_pool = population

        if not self.population and population_pool >= self.population_allotment:
            # Assume this culture just fills up the entire region
            #   so specifics aren't calculated until necessary
            self.color = culture.color
            self.cultures.append(culture)
            self.names.append(culture.genName())

            for o in self.locales:
                o.populate(o.population_allotment, culture)
            self.populace = Populace(culture=culture, population=self.population_allotment)
            return

        while population_pool > 0:
            # include in occupied locales the locales that are occupied externally to the current subregion
            occupied_locales = self.world.culture_locales(culture)

            # get all locales that are not fully populated
            if occupied_locales:
                unfilled_locales = []
                for locale in occupied_locales:
                    unfilled_locales += [
                        o for o in locale.bordered(self.locales) if not o.population
                    ]

                if len(unfilled_locales) > 1:
                    bordered_count = [[r, unfilled_locales.count(r)] for r in set(unfilled_locales)]
                    max_bordered = max(r[1] for r in bordered_count)
                    most_bordered = [r[0] for r in bordered_count if r[1] == max_bordered]
                    unfilled_locales = most_bordered

            else:
                unfilled_locales = [o for o in self.locales if o.type == 'land' and not o.population]

            # if there are none, finish prematurely
            if not unfilled_locales:
                return

            # select one at random
            current_locale = random.choice(unfilled_locales)

            # attempt to populate
            pop = current_locale.population_allotment
            # allotment_remaining = current_locale.population_allotment - current_locale.population
            # pop = min(allotment_remaining, population_pool)
            population_pool -= pop
            current_locale.populate(pop, culture)

            # if population was successful
            if culture in current_locale.cultures and culture not in self.cultures:
                # add to the list of occupied locales
                self.cultures.append(culture)
                self.names.append(culture.genName())

    @property
    def population(self):
        if not self._populated:
            return 0
        if self.populace:
            return self.populace.population
        else:
            # check population of constituent regions
            return sum(r.population for r in self.locales)


class Locale(Region):
    """
    Representation of a region with an area of about 100sqkm
    A locale may contain several settlements, forests, lakes, or other features, but is
        not otherwise subdivided
    """

    def __init__(self, *args, **kwargs):
        self.settlements = []
        self.capital = None
        self.mark = False
        super().__init__(*args, **kwargs)

    def populate(self, population, culture):
        """
        Populate locale
        """
        if self.type in ('ocean', 'lake'):
            return
        self._populated = True

        self.color = culture.color
        self.cultures.append(culture)
        self.populace = Populace(culture=culture, population=population)
        self.names.append(culture.genName())

    def is_border(self):
        bordered = self.bordered(self.world.locales, exclude_ocean=False)
        if any(b.subregion is not self.subregion for b in bordered):
            return True
        return False

    def settle(self):
        """
        Generate settlements for this locale
        """
        # urbanization between 5-10 percent
        # largest
        population = int(self.population / 10)
        self.capital = Settlement(populace=self.populace.split(population), coords=self.centroid)
        self.capital.leader = Person(culture=self.cultures[0], age=40)
        self.capital.leader.generate_family()

    @property
    def population(self):
        if not self._populated:
            return 0
        # if self.populace:
        else:
            return self.populace.population
        # else:
        #     # check population of constituent regions
        #     return sum(r.population for r in self.settlements)


class Settlement:
    def __init__(self, **kwargs):
        populace = kwargs.get('populace')
        if populace:
            self.populace = populace
            self.culture = populace.culture
        else:
            population = kwargs.get('population')
            culture = kwargs.get('culture')

            self.culture = culture
            self.populace = Populace(culture=culture, population=population)

        self.locale = kwargs.get('locale')
        self.coords = kwargs.get('coords')
        self.name = self.culture.genName()

        # http://www.lostkingdom.net/medieval-village-buildings-cottage/
        """
        ex:
            Exports: Cured Fish, Meat, Iron
            Imports: Salt, Wood, Hemp, Livestock feed, Coal, Spices
        """

    @property
    def population(self):
        return self.populace.population

    # def populate(self):
    #     people = []
    #     while(len(people) < 10):
    #         people += generate_family(culture=self.culture)
    #     self.populace = Populace(people)
    #     # print(f'{self.name} populated')

    def __repr__(self):
        return f'{self.name}, Population: {self.population}'


class Continent(Region):
    pass


class World:
    def node_at(self, point):
        x, y = point
        index = f'{int(x * 100)},{int(y * 100)}'
        node = self.nodes.get(index)
        if not node:
            node = Node(point, world=self)
            self.nodes[index] = node
        return node

    def region_at(self, point):
        for region in self.regions:
            if region.maybe_encloses(point) and region.encloses(point):
                return region

    def __init__(self, **kwargs):
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.scale = kwargs.get('scale')
        self.heightmap = kwargs.get('heightmap', [])
        self.weathermap = kwargs.get('weathermap', [])
        self.nodes = dict()

        self.cultures = []
        self.continents = set()
        self.subcontinents = set()
        self.regions = set()
        self.subregions = set()
        self.locales = set()
        self.settlements = set()

        _regions = kwargs.get('regions', [])
        _subregions = kwargs.get('subregions', [])
        _locales = kwargs.get('locales', [])

        self.subcontinents = kwargs.get('subcontinents', [])

        self.avg_temperature = kwargs.get('avg_temperature')

        for region in _regions:
            region.world = self
            cx, cy = region.centroid
            dl = ((cy - (self.height / 2)) * self.scale) / 1500
            dt = dl * 10.8
            region.temperature = int(dt + self.avg_temperature)
            self.regions.add(region)

        for subregion in _subregions:
            subregion.world = self
            region = None

            might_enclose = [r for r in self.regions if r.maybe_encloses(subregion.centroid)]
            if not might_enclose:
                continue
            for r in might_enclose:
                if r.encloses(subregion.centroid):
                    region = r
                    break
            if region is None:
                continue

            subregion.region = region
            subregion.type = region.type

            cx, cy = subregion.centroid
            region.subregions.add(subregion)
            self.subregions.add(subregion)

        for locale in _locales:
            locale.world = self
            subregion = None

            # region_might_enclose = [r for r in self.regions if r.maybe_encloses(locale.centroid)]
            # if not region_might_enclose:
            #     continue
            # if len(region_might_enclose) == 1:
            #     region = region_might_enclose[0]
            # else:
            #     for r in region_might_enclose:
            #         if r.encloses(locale.centroid):
            #             region = r
            #             break

            might_enclose = [r for r in self.subregions if r.maybe_encloses(locale.centroid)]
            if not might_enclose:
                continue
            for r in might_enclose:
                if r.encloses(locale.centroid):
                    subregion = r
                    break
            if subregion is None:
                continue

            locale.subregion = subregion
            locale.type = subregion.type

            cx, cy = locale.centroid
            density = int(locale.precipitation * (20 / 2000))
            locale.population_allotment = int(density * locale.geoarea)

            subregion.locales.add(locale)
            self.locales.add(locale)

        for subregion in self.subregions:
            subregion.population_allotment = 0
            for locale in subregion.locales:
                subregion.population_allotment += locale.population_allotment

        for region in self.regions:
            region.population_allotment = 0
            for subregion in region.subregions:
                region.population_allotment += subregion.population_allotment

        # print("Classifying...")
        # for locale in self.locales:
        #     if locale.type == 'ocean':
        #         b = locale.bordered(self.locales)
        #         for r in b:
        #             if r.type != 'ocean':
        #                 r.type = 'coast'

        # Index nodes
        print("Indexing...")
        for continent in self.continents:
            continent.index(self)
        for subcontinent in self.subcontinents:
            subcontinent.index(self)
        for region in self.regions:
            region.index(self)
        for subregion in self.subregions:
            subregion.index(self)
        for locale in self.locales:
            locale.index(self)

        self.land = set(r for r in self.locales if r.type == 'land')
        self.sea = set(r for r in self.locales if r.type != 'land')

    def index_borders(self):
        # Index borders
        self.borders = {
            't1': set(),
            't2': set(),
            't3': set()
        }

        for region in self.regions:
            for b in region.borders:
                try:
                    l1, l2 = b.between
                except (IndexError, ValueError):
                    continue
                b.type = set()
                if l1.type == 'ocean' and l2.type == 'ocean':
                    b.type.add('ocean')
                elif l1.type == 'ocean' or l2.type == 'ocean':
                    b.type.add('coast')

                if l1.type == 'lake' and l2.type == 'lake':
                    b.type.add('lake')
                elif l1.type == 'lake' or l2.type == 'lake':
                    b.type.add('coast')
                b.type.add('t1')
                self.borders['t1'].add(b)

        for subregion in self.subregions:
            for b in subregion.borders:
                try:
                    l1, l2 = b.between
                except (IndexError, ValueError):
                    continue
                b.type = set()
                if l1.type == 'ocean' and l2.type == 'ocean':
                    b.type.add('ocean')
                elif l1.type == 'ocean' or l2.type == 'ocean':
                    b.type.add('coast')

                if l1.type == 'lake' and l2.type == 'lake':
                    b.type.add('lake')
                elif l1.type == 'lake' or l2.type == 'lake':
                    b.type.add('coast')

                if l1.region is not l2.region:
                    b.type.add('t1')
                else:
                    b.type.add('t2')
                self.borders['t2'].add(b)

        for locale in self.locales:
            for b in locale.borders:
                try:
                    l1, l2 = b.between
                except (IndexError, ValueError):
                    continue
                b.type = set()
                if l1.type == 'ocean' and l2.type == 'ocean':
                    b.type.add('ocean')
                elif l1.type == 'ocean' or l2.type == 'ocean':
                    b.type.add('coast')

                if l1.type == 'lake' and l2.type == 'lake':
                    b.type.add('ocean')
                elif l1.type == 'lake' or l2.type == 'lake':
                    b.type.add('coast')

                if l1.subregion.region is not l2.subregion.region:
                    b.type.add('t1')
                elif l1.subregion is not l2.subregion:
                    b.type.add('t2')
                else:
                    b.type.add('t3')
                self.borders['t3'].add(b)

    def index_culture_borders(self):
        # Index borders
        self.culture_borders = set()
        for locale in self.locales:
            for b in locale.borders:
                try:
                    l1, l2 = b.between
                    if l1.cultures[0] not in l2.cultures:
                        self.culture_borders.add(b)
                except (IndexError, ValueError):
                    continue

    def populate(self, population, culture):
        """
        Populate world with a new culture
        """
        population_pool = population

        while population_pool > 0:
            occupied_regions = self.culture_regions(culture)

            # get all regions that are not fully populated
            if occupied_regions:
                unfilled_regions = []
                for region in occupied_regions:
                    unfilled_regions += [
                        r for r in region.bordered(self.regions) if r.population < r.population_allotment
                    ]

                if len(unfilled_regions) > 1:
                    bordered_count = [[r, unfilled_regions.count(r)] for r in set(unfilled_regions)]
                    max_bordered = max(r[1] for r in bordered_count)
                    most_bordered = [r[0] for r in bordered_count if r[1] == max_bordered]
                    unfilled_regions = most_bordered

            else:
                unfilled_regions = [
                    r for r in self.regions if r.type == 'land' and r.population < r.population_allotment
                ]

            # if there are none, finish prematurely
            if not unfilled_regions:
                return

            # select one at random
            current_region = random.choice(unfilled_regions)

            # populate
            allotment_remaining = current_region.population_allotment - current_region.population
            pop = min(allotment_remaining, population_pool)
            population_pool -= pop
            current_region.populate(pop, culture)

    @staticmethod
    def bordered(subject_regions, candidate_regions, most_bordered_only=True):
        """
        Finds regions bordering a group of regions
        Sort by the number of subject regions bordering each candidate region
        """
        _bordered = []
        for region in subject_regions:
            for r in region.bordered(candidate_regions):
                if r not in subject_regions:
                    _bordered.append(r)
        if len(_bordered) <= 1 or not most_bordered_only:
            return _bordered

        bordered_count = [[r, _bordered.count(r)] for r in set(_bordered)]
        max_bordered = max(r[1] for r in bordered_count)
        most_bordered = [r[0] for r in bordered_count if r[1] == max_bordered]

        return most_bordered

    def culture_settlements(self, culture):
        _settlements = []
        for settlement in self.settlements:
            if culture is settlement.culture:
                _settlements.append(settlement)
        return _settlements

    def culture_locales(self, culture):
        """
        Get the set of locales occupied by this culture
        """
        _locales = []
        for locale in self.locales:
            if culture in locale.cultures:
                _locales.append(locale)
        return _locales

    def culture_subregions(self, culture):
        """
        Get the set of subregions occupied by this culture
        """
        _subregions = []
        for subregion in self.subregions:
            if culture in subregion.cultures:
                _subregions.append(subregion)
        return _subregions

    def culture_regions(self, culture):
        """
        Get the set of regions occupied by this culture
        """
        _regions = []
        for region in self.regions:
            if culture in region.cultures:
                _regions.append(region)
        return _regions

    def culture_population(self, culture):
        population = 0
        population += sum(o.population for o in self.culture_locales(culture))

        return population

    @staticmethod
    def deserialize(data):
        regions = data.get('regions')
        rivers = data.get('rivers')

        heightmap = NoiseMap(width=cls.width, height=cls.height, scale=500, seed=5)
        weathermap = NoiseMap(width=cls.width, height=cls.height, seed=10)

        regions = []
        rivers = self.rivers

        for region in self.regions:
            _region = dict()
            _region['culture'] = region.culture
            _region['subregions'] = []

            for subregion in region.subregions:
                _subregion = dict()
                _subregion['population'] = subregion.population
                _subregion['locales'] = []

                for locale in subregion.locales:
                    _locale = dict()
                    _locale['points'] = locale.points
                    _subregion['locales'].append(_locale)

                _region['subregions'].append(_subregion)

            regions.append(_region)

    def serialize(self):
        regions = []
        rivers = []
        heightmap = {
            'scale': self.heightmap.scale,
            'octaves': self.heightmap.octaves,
            'persistence': self.heightmap.persistence,
            'lacunarity': self.heightmap.lacunarity,
            'seed': self.heightmap.seed,
        }
        weathermap = {
            'scale': self.weathermap.scale,
            'octaves': self.weathermap.octaves,
            'persistence': self.weathermap.persistence,
            'lacunarity': self.weathermap.lacunarity,
            'seed': self.weathermap.seed,
        }

        for region in self.regions:
            _region = dict()
            _region['culture'] = region.culture
            _region['subregions'] = []

            for subregion in region.subregions:
                _subregion = dict()
                _subregion['population'] = subregion.population
                _subregion['locales'] = []

                for locale in subregion.locales:
                    _locale = dict()
                    _locale['points'] = locale.points
                    _subregion['locales'].append(_locale)

                _region['subregions'].append(_subregion)

            regions.append(_region)

        for river in self.rivers:
            _river = []
            for segment in river:
                p1, p2 = segment
                _river.append((p1.coords, p2.coords))
            rivers.append(_river)

        return {
            'regions': regions,
            'rivers': rivers,
            'heightmap': heightmap,
            'weathermap': weathermap,
        }


class Populace:
    """
    A set number of people of one culture in one location
    """

    ages = AGES
    """
    The percentage of the population comprising each age group
    Male and female is going to need to be incorporated here as well
    For general population growth this will form the basis of birth rates

    'age':  0, 'weight': 22
    'age': 10, 'weight': 17
    'age': 20, 'weight': 18
    'age': 30, 'weight': 16
    'age': 40, 'weight': 12
    'age': 50, 'weight': 9
    'age': 60, 'weight': 6
    'age': 70, 'weight': 2
    """

    def __init__(self, **kwargs):
        self.culture = kwargs.get('culture', Culture())
        self.population = kwargs.get('population')

    def split(self, population):
        """
        Splits off a number of people to form a new populace unit
        """
        self.population -= population
        return Populace(culture=self.culture, population=population)

    def recalculate(self):
        """
        Recalculate age weights based on any demographic changes
        """
        pass
