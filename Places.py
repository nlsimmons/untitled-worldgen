from vars import *
from Language import Language, Culture
from sympy.geometry import Point, Polygon
from Character import Person, generate_family
import random
import math

"""
village = Village(population)
village.area = population / density (randomized within a range)
village.culture = Culture()
village.name = village.culture.language.name()

village.leader = Person(culture)

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

    def __init__(self, points, **kwargs):
        world = kwargs.get('world')
        self.world = world
        self.points = points
        self.nodes = []
        self.centroid = get_midpoint(points)
        self.subregions = set()
        self.locales = set()
        self.type = ''
        self.population = 0
        self.capital = None
        # self.area = None
        self.road = None
        self.rivers = set()

        return

        self.cities = list()
        self.towns = list()
        self.villages = list()
        self.settlements = self.cities + self.towns + self.villages
        self.type = ''
        self.color = ''

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
            precipitation = self.world.weathermap.noise_at(cx, cy) * 100
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
        if(self.bounds['min_x'] > x
           or self.bounds['max_x'] < x
           or self.bounds['min_y'] > y
           or self.bounds['max_y'] < y):
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

    def populate(self):
        if self.type == 'ocean':
            return

        self.culture = Culture()
        self.name = self.culture.genName()

        for subregion in self.subregions:
            subregion.culture = self.culture
            subregion.name = subregion.culture.genName()

            try:
                geoarea = subregion.geo_area
            except AttributeError:
                subregion.geo_area = subregion.area / (self.world.scale ** 2)
                geoarea = subregion.geo_area

            subregion.density = int(subregion.precipitation * (15 / 100))
            subregion.population = int(geoarea * subregion.density)

        self.capital = sorted(self.subregions, key=lambda r: r.population, reverse=True)[0]
        return

        # if in a steppe or other arid biome, with low density (under 1-5?) pastoral nomadism
        city_population = int(self.population / 10 * random.uniform(0.8, 1.2))

        city = Settlement(population=city_population, culture=self.culture)
        towns = []

        n_satellites = random.randint(5, 7)
        n = n_satellites
        for _ in range(n_satellites):
            town_population = int(city_population / n)
            towns.append(Settlement(population=town_population, culture=self.culture))
            n += 1

        city.satellites = towns
        self.city = city
        self.towns = towns

        print(f'Region of {self.name} generated')

        """
        village.leader = Person(culture)

        Resources
        # https://en.wikipedia.org/wiki/Cereal#Production
        # wheat, barley, corn, rice, sorghum, millet, oats, rye, bananas,
        #   potatoes, cassava, soybeans, sweet potato, yam, plantain
        # tobacco, cotton, spices, coffee, rapeseed, tea,
        # https://en.wikipedia.org/wiki/Livestock#Types
        # sheep, cattle, horses, dogs, cats, donkeys, yak, buffalo, reindeer, camel, llama, alpaca, pig, rabbit

        "leadership": ("democratic", "single_elder", "multiple_elder", "chiefdom"),
        "gender_role": ("patriarchal", "matriarchal", "egalitarian"),
        "sedentism": ("full", "transhumant", "nomadic"),
        "violence": ("low", "moderate", "high")

        self.water = random.randint(0, 100) < params.get('water', 0)
        self.forest = random.randint(0, 100) < params.get('forest', 0)
        self.hills = random.randint(0, 100) < params.get('hills', 0)

        Villages have will have disputes with their neighbors
        Think of a classification scheme for these disputes
            Border dispute (this would be for larger entities)

        Figure out combat and generalship

        """

    def bordered(self, regions, exclude_ocean=True):
        _bordered = set()
        for region in regions:
            if region is self:
                continue
            if exclude_ocean and region.type == 'ocean':
                continue
            if any(point in self.points for point in region.points):
                _bordered.add(region)
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
    def __init__(self, *args, **kwargs):
        self.locales = set()
        super().__init__(*args, **kwargs)


class Locale(Region):
    pass


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

    def __init__(self, **kwargs):
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.scale = kwargs.get('scale')
        self.heightmap = kwargs.get('heightmap', [])
        self.weathermap = kwargs.get('weathermap', [])
        self.nodes = dict()

        self.regions = set()
        self.subregions = set()
        self.locales = set()

        _regions = kwargs.get('regions', [])
        _subregions = kwargs.get('subregions', [])
        _locales = kwargs.get('locales', [])

        for region in _regions:
            region.world = self
            self.regions.add(region)

        for subregion in _subregions:
            might_enclose = [r for r in self.regions if r.maybe_encloses(subregion.centroid)]
            if not might_enclose:
                continue
            if len(might_enclose) == 1:
                region = might_enclose[0]
            else:
                for r in might_enclose:
                    if r.encloses(subregion.centroid):
                        region = r
                        break
            subregion.region = region
            subregion.type = region.type

            region.subregions.add(subregion)
            subregion.world = self

            self.subregions.add(subregion)

        for locale in _locales:
            might_enclose = [r for r in self.subregions if r.maybe_encloses(locale.centroid)]
            if not might_enclose:
                continue
            if len(might_enclose) == 1:
                subregion = might_enclose[0]
            else:
                for r in might_enclose:
                    if r.encloses(locale.centroid):
                        subregion = r
                        break
            locale.subregion = subregion
            locale.type = subregion.type

            subregion.locales.add(subregion)
            locale.region = subregion.region
            locale.region.locales.add(locale)
            locale.world = self

            self.locales.add(locale)

        # print("Classifying...")
        # for locale in self.locales:
        #     if locale.type == 'ocean':
        #         b = locale.bordered(self.locales)
        #         for r in b:
        #             if r.type != 'ocean':
        #                 r.type = 'coast'

        # Index nodes
        print("Indexing...")
        for region in self.regions:
            region.index(self)
        for subregion in self.subregions:
            subregion.index(self)
        for locale in self.locales:
            locale.index(self)

        self.land = set(r for r in self.locales if r.type != 'ocean')
        self.sea = set(r for r in self.locales if r.type == 'ocean')

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
                if l1.region is not l2.region:
                    b.type.add('t1')
                elif l1.subregion is not l2.subregion:
                    b.type.add('t2')
                else:
                    b.type.add('t3')
                self.borders['t3'].add(b)

    def update(self):
        self.region_types = dict()
        for region in self.regions:
            if region.type:
                region.color = self.COLORS.get(region.type)
                try:
                    self.region_types[region.type].add(region)
                except KeyError:
                    self.region_types[region.type] = set()
                    self.region_types[region.type].add(region)


class Settlement:
    """
    Hunting, fishing, farming (how common are each)
    Other types?
    """

    def __init__(self, **kwargs):
        self.region = kwargs.get('region')
        self.population = int(kwargs.get('population'))
        self.culture = kwargs.get('culture')
        self.name = self.culture.genName()

        # http://www.lostkingdom.net/medieval-village-buildings-cottage/
        """
        ex:
            Exports: Cured Fish, Meat, Iron
            Imports: Salt, Wood, Hemp, Livestock feed, Coal, Spices
        """

    def populate(self):
        # We just need to assign the mode of governance and natural resources for the purpose of
        #   figuring out trade and other foreign affairs
        # A region may be invaded by another for various reasons and this is determined by their culture and mode
        #   of governance as well as what resources they have that someone might want to take
        # As well traders may travel to or from this settlement and it's important to note what goods are and
        #   are not available in order to drive trade
        # The primary city acts as a hub for the region so its resources can be generally thought of as representative
        #   of all resources for that region
        """
        What are the factors that decide the mode of governance?
        A land with poor fertility favors raiding and survival-of-the-fittest
        A land with high fertility may favor eldership as lifespans would be somewhat longer
        """
        # dd((self.culture.name, self.population, self.region.fertility))

        # Because I'm lazy let's just generate one family per city for now
        # Everything else requires more thought put into resources, which requires thought put into terrain

        people = []
        while(len(people) < 10):
            people += generate_family(culture=self.culture)
        self.populace = Populace(people)
        # print(f'{self.name} populated')

    def __repr__(self):
        return f'{self.name}, Population: {self.population}'


class Populace:
    def __init__(self, initial, **kwargs):
        self.people = initial

    def __repr__(self):
        return self.people
