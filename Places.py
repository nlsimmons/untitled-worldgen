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

    def neighbors(self):
        _neighbors = []

        for r in self.regions:
            for border in r.borders:
                if self in border.nodes:
                    _neighbors.append([n for n in border.nodes if n is not self][0])
        return _neighbors

        # _neighbors = set()
        # for r in self.regions:
        #     for n in r.nodes:
        #         if n is self:
        #             continue
        #         _neighbors.add(n)
        # return _neighbors


class Border:
    type = ''

    def __init__(self, node1, node2, world):
        self.nodes = (node1, node2)
        self.world = world

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

    def maybe_encloses(self, point):
        min_x = min(x for x, y in self.points)
        max_x = max(x for x, y in self.points)
        min_y = min(y for x, y in self.points)
        max_y = max(y for x, y in self.points)
        x, y = point

        if (min_x <= x <= max_x) and (min_y <= y <= max_y):
            return True
        return False

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
    pass
    # def __init__(self, *args, **kwargs):
    #     self.display_regions = set()
    #     super().__init__(*args, **kwargs)
    # def bordered(self, subregions, exclude_ocean=True):
    #     bordered_regions = self.region.bordered(self.world.regions)
    #     subregions = [r for r in subregions if r.region in bordered_regions]

    #     return super().bordered(subregions, exclude_ocean=exclude_ocean)


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

        _regions = kwargs.get('regions', [])
        _subregions = kwargs.get('subregions', [])
        _display_regions = kwargs.get('display_regions', [])

        for subregion in _subregions:
            might_enclose = [r for r in _regions if r.maybe_encloses(subregion.centroid)]
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
            subregion.world = self
            subregion.type = region.type
            region.subregions.add(subregion)
            self.subregions.add(subregion)

        for region in _regions:
            if region.subregions:
                region.world = self
                self.regions.add(region)

        self.display_regions = set()
        for display_region in _display_regions:
            might_enclose = [r for r in self.subregions if r.maybe_encloses(display_region.centroid)]
            if not might_enclose:
                continue
            if len(might_enclose) == 1:
                subregion = might_enclose[0]
            else:
                for r in might_enclose:
                    if r.encloses(display_region.centroid):
                        subregion = r
                        break
            display_region.region = subregion
            display_region.type = subregion.type
            display_region.world = self
            subregion.subregions.add(display_region)
            self.display_regions.add(display_region)

        for ssr in self.display_regions:
            if ssr.type == 'ocean':
                b = ssr.bordered(self.display_regions)
                for sr in b:
                    if sr.type != 'ocean':
                        sr.type = 'coast'

        # Index nodes
        for ssr in self.regions:
            ssr.index(self)
        for ssr in self.subregions:
            ssr.index(self)
        for ssr in self.display_regions:
            ssr.index(self)

        self.land = set(r for r in self.display_regions if r.type != 'ocean')
        self.sea = set(r for r in self.display_regions if r.type == 'ocean')

        # Index borders
        self.borders = set()
        for sr in self.subregions:
            for ssr in sr.subregions:
                for b in ssr.borders:
                    try:
                        b.type = set()
                        if all(r.type == 'ocean' for r in b.between):
                            b.type.add('ocean')
                        elif any(r.type == 'ocean' for r in b.between):
                            b.type.add('coast')

                        if b.between[0].region.region is not b.between[1].region.region:
                            b.type.add('t1')
                        elif b.between[0].region is not b.between[1].region:
                            b.type.add('t2')
                        else:
                            b.type.add('t3')
                    except IndexError:
                        pass

                    self.borders.add(b)

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
