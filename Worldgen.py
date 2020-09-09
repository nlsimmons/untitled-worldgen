from vars import *
import random
import math
from scipy.spatial import Voronoi
from Places import World, Region, Subregion, Locale, Road
from Language import Culture
from Resources import STAPLE_CROPS
from perlin import NoiseMap
import copy
import time

# random.seed(1)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 168, 82)
BLUE = (66, 135, 245)
DARK_BLUE = (0, 0, 139)
DARK_GREEN = (59, 85, 38)
RED = (255, 0 , 0)
ORIGIN = (0, 0)


class Worldgen:
    @classmethod
    def make_regions(cls, points, n_relax=0):
        def relax(regions):
            relaxed_points = []
            for region in regions:
                centroid = get_midpoint(region)
                relaxed_points.append(centroid)
            return cls.make_regions(relaxed_points)

        vor = Voronoi(points)
        vor_regions = [r for r in vor.regions if -1 not in r]

        regions = []
        for indexed_region in vor_regions:
            if not indexed_region:
                continue
            region = [tuple(vor.vertices[vertex_index]) for vertex_index in indexed_region]
            regions.append(region)

        for _ in range(n_relax):
            regions = relax(regions)
        return regions

    @classmethod
    def point_is_oob(cls, point):
        x, y = point
        max_x = cls.width
        max_y = cls.height
        if max_x and (x < 0 or x > max_x):
            return True
        if max_y and (y < 0 or y > max_y):
            return True
        return False

    @classmethod
    def distance_from_edge(cls, point):
        x, y = point
        max_x = cls.width
        max_y = cls.height

        return min(
            x - 0,
            max_x - x,
            y - 0,
            max_y - y)

    @classmethod
    def clip_regions(cls, regions, clip_any=False):
        """
        Removes regions that lie entirely outside intended world map
        """
        clipped_regions = []
        for region in regions:
            if all(cls.point_is_oob(point) for point in region):
                continue
            if clip_any and any(cls.point_is_oob(point) for point in region):
                continue
            clipped_regions.append(region)
        return clipped_regions

    @classmethod
    def voronoi_map(cls, n_points, **kwargs):
        points = []
        for _ in range(n_points * 9):
            x = random.uniform(cls.width * -1, cls.width * 2)
            y = random.uniform(cls.height * -1, cls.height * 2)
            x = int(x)
            y = int(y)
            points.append((x, y))

        # points += [(x + screen_x, y) for x, y in points] + [(x - screen_x, y) for x, y in points]
        # points += [(x, y + screen_y) for x, y in points] + [(x, y - screen_y) for x, y in points]

        relax_passes = kwargs.get('relax_passes', 0)
        regions = cls.make_regions(points, relax_passes)
        return regions

    @classmethod
    def new(cls, **kwargs):
        print('')
        print("Shaping world...")
        start = time.time()
        cls.width = kwargs.get('width')
        cls.height = kwargs.get('height')
        percent_ocean = kwargs.get('percent_ocean') / 100

        n_subcontinents = int(kwargs.get('n_subcontinents'))

        subcontinent_area = kwargs.get('subcontinent_area')
        region_area = kwargs.get('region_area')
        n_regions = int(n_subcontinents * (subcontinent_area / region_area))

        subcontinents = cls.voronoi_map(n_subcontinents, **kwargs)
        subcontinents = [Region(r) for r in cls.clip_regions(subcontinents)]

        regions = cls.voronoi_map(n_regions, **kwargs)
        regions = cls.clip_regions(regions)
        regions = [Region(r) for r in regions]

        for region in regions:
            if any(cls.point_is_oob(p) for p in region.points):
                # Regions that touch map edges are ocean
                region.bound = True
                region.type = 'ocean'
            if any((cls.distance_from_edge(p) < (cls.height * 0.05)) for p in region.points):
                # Regions that come within 5% of the edge of the map are ocean
                region.bound = True
                region.type = 'ocean'

        options = [r for r in regions if not r.bound]
        random.shuffle(options)

        n_land = int((1 - percent_ocean) * len(options))
        k = kwargs.get('n_continent_seeds')
        continents = random.choices(options, k=k)
        for c in continents:
            c.type = 'land'

        # Generate continents
        while len(continents) < n_land:
            options = [r for r in regions if r.type == '']
            c = random.choice(continents)
            bordered = c.bordered(options, False)
            if not bordered:
                continue
            for b in bordered:
                if b in continents:
                    continue
                b.type = 'land'
                continents.append(b)
                if len(continents) > n_land:
                    break

        # Assign remaining unassigned regions to either ocean or lakes
        #   These are large inland seas/lakes like the Caspian or Great Lakes
        ocean = [r for r in regions if r.type == 'ocean'][0]
        oceans = ocean.flood_select(regions, ['ocean', ''])

        for r in oceans:
            r.type = 'ocean'
        for r in regions:
            if r.type == '':
                r.type = 'lake'

        region_area = kwargs.get('region_area')
        subregion_area = kwargs.get('subregion_area')
        locale_area = kwargs.get('locale_area')

        n_subregions = int(n_regions * (region_area / subregion_area))
        subregions = cls.voronoi_map(n_subregions, **kwargs)
        subregions = [Subregion(r) for r in cls.clip_regions(subregions)]

        n_locales = int(n_subregions * (subregion_area / locale_area))
        locales = cls.voronoi_map(n_locales, **kwargs)
        locales = [Locale(r) for r in cls.clip_regions(locales)]

        avg_area = sum(s.area for s in subregions) / len(subregions)

        scale = math.sqrt(avg_area) / math.sqrt(subregion_area)  # u / km

        heightmap_scale = kwargs.get('heightmap_scale')
        weathermap_scale = kwargs.get('weathermap_scale')

        heightmap = NoiseMap(width=cls.width, height=cls.height, scale=heightmap_scale, seed=5)
        weathermap = NoiseMap(width=cls.width, height=cls.height, scale=weathermap_scale, seed=10)
        end = time.time()
        print("Finished in %d seconds" % (end - start))

        print('')
        print("Carving out the landscape...")
        start = time.time()
        world = World(subcontinents=subcontinents,
                      regions=regions,  # Large scale regions
                      subregions=subregions,  # Areas 7000sqkm in size
                      locales=locales,  # Areas 1000sqkm in size
                      scale=scale,
                      heightmap=heightmap,
                      weathermap=weathermap,
                      **kwargs)
        end = time.time()
        print("Finished in %d seconds" % (end - start))

        n_regions = len([r for r in world.regions if r.type != 'ocean'])
        n_subregions = len([r for r in world.subregions if r.type != 'ocean'])

        print(f"Map dimensions: {int(cls.width / scale)} km x {int(cls.height / scale)} km")
        print(f"Total map area: {int(cls.width * cls.height / (scale ** 2))} sqkm")
        print(f"Total land area: {int(sum(r.geoarea for r in world.locales if r.type != 'ocean'))} sqkm")
        print(f"Total number of regions : {n_regions}")
        print(f"Total number of subregions : {n_subregions}")

        ###############################################

        # Generate resources, calculate rainfall, draw rivers etc
        """
        Resources such as iron, copper, tin, silver, gold, salt
        What crops are grown, what animals are available
        Cash crops such as tobacco, sugar, flax, cocoa, coca, poppy, cannabis/hemp, tea, silk, other shit
        Fish-plentiful areas (is this a thing?)
        Honey, grapes, beer, other alcohol production
        """

        ###############################################

        if kwargs.get('populate'):
            print('')
            print("Dropping people from the sky...")
            print()
            start = time.time()

            # Generate culture groups
            #   These are the groups that share a parent culture and will be subdivided into different ethnic
            #   nation-states
            total_area = sum(r.geoarea for r in world.locales if r.type != 'ocean')
            average_density = 5
            total_population = total_area * average_density
            total_cultures = 0

            # population_pool = total_population
            attempts = 100
            while attempts > 0:
                culture = Culture()
                culture.staples = random.choices(list(STAPLE_CROPS.keys()), k=3)
                pop = int(total_population / 10)
                # int(random.uniform(10000, 100000))
                # pop = min(pop, population_pool)
                world.populate(pop, culture)
                culture_pop = world.culture_population(culture)
                if not culture_pop:
                    attempts -= 1
                    continue
                world.cultures.append(culture)
                # print(f'Culture group {culture.name} generated')
                # print(f'Total population: {culture_pop}')
                # print()
                # population_pool -= culture_pop
                total_cultures += 1

            # To keep things simple just divvy the largest nation-states in each culture group
            #     pop = int(random.uniform(100000, 1000000))

            # 10% 100k to 1 mil
            #   10% will contain an autonomous minority comprising 5-15% of the total
            #       and some number of other minority groups, either from neighboring regions
            #       or independently generated somehow
            # 10% 500,000 people
            #   10% will contain an autonomous minority comprising 5-15% of the total
            # 10% 50,000 people
            #   10% will contain an autonomous minority comprising 5-15% of the total
            # 25% 5000 people
            # 45% 1000 people
            # 10% largest unit is the family (5-10 people)
            #     50% of these are organized into trade/military alliances

            # while True:
            #     culture = Culture()
            #     world.populate(200000, culture)
            #     culture_pop = world.culture_population(culture)
            #     if not culture_pop:
            #         break
            #     print(f'Culture {culture.name} generated')
            #     print(f'Total population: {culture_pop}')
            #     print()

            # for _ in range(20):
            #     culture = Culture()
            #     world.populate(10000, culture)
            #     world.cultures.append(culture)
            #     print(f'Culture {culture.name} generated')
            #     culture_pop = world.culture_population(culture)
            #     print(f'Total population: {culture_pop}')
            #     print()

            # culture = Culture()
            # world.populate(500000, culture)
            # world.cultures.append(culture)
            # print(f'Culture {culture.name} generated')
            # print(f'Total population: {sum(r.population for r in world.culture_regions(culture))}')
            # print()

            end = time.time()
            print("Finished in %d seconds" % (end - start))
            print(f"Total cultures generated: {total_cultures}")

        ###############################################

        if kwargs.get('rivers'):
            n_rivers = kwargs.get('rivers')
            print('')
            print("Making it rain...")
            start = time.time()

            n = len(world.land)
            # rainfall_regions = list(copy.copy(world.land))
            # rainfall_regions.sort(key=lambda r: r.precipitation, reverse=True)
            # top_rainfall = rainfall_regions[0:int(n * 0.5)]

            nodes = [n for n in world.nodes.values() if n.elevation > 0]

            elevation_nodes = copy.copy(nodes)
            top_elevation = sorted(elevation_nodes, key=lambda r: r.elevation, reverse=True)[0:int(n / 2)]

            rainfall_nodes = copy.copy(nodes)
            top_rainfall = sorted(rainfall_nodes, key=lambda r: r.precipitation, reverse=True)[0:int(n / 2)]

            rivers = []
            while len(rivers) < n_rivers:
                source = random.choice(world.nodes)

                traversed = []
                elevation = source.elevation
                current = source
                river_segments = []
                while elevation > 0:
                    try:
                        traversed.append(current)
                        next = sorted(([n for n in current.neighbors('t2') if n not in traversed]),
                                      key=lambda r: r.elevation)[0]
                        river_segments.append((current, next))

                        if next.river_count:
                            next.river_count += 1
                            break

                        elevation = next.elevation
                        current = next
                    except IndexError:
                        break
                if len(river_segments) < 30:
                    continue
                rivers.append(river_segments)
            world.rivers = rivers
            end = time.time()
            print("Finished in %d seconds" % (end - start))
        else:
            world.rivers = []

        ###############################################

        if kwargs.get('roads'):
            print('')
            print("Digging roads...")
            start = time.time()
            roads = set()
            capitals = [r.capital for r in world.regions if r.capital]
            for c in capitals:
                for d in capitals:
                    if d is c:
                        # Obviously we are not building roads from a cell to itself
                        continue
                    if c.road and d in c.road.connects:
                        # Don't need to build the same road twice
                        continue
                    if c.distance_to(d) > 250:
                        # Only construct roads when the distance between two points is
                        #   less than 250
                        continue

                    destination = d
                    current = c
                    road = []
                    traversed = set()

                    while True:
                        b = current.bordered(world.subregions)
                        if not b:
                            break
                        next = sorted(b, key=lambda r: r.distance_to(d))[0]
                        if next in traversed:
                            # Means the road is doubling back, which means something went wrong, which means bail out
                            break

                        segment = (current, next)
                        road.append(segment)

                        if next is destination:
                            new_road = Road(segments=road, connects=(c, d))
                            roads.add(new_road)
                            next.road = new_road
                            break

                        if next.road and destination in next.road.connects:
                            next.road.add(road)
                            break

                        traversed.add(next)
                        current = next
            world.roads = roads
            world.capitals = capitals
            end = time.time()
            print("Finished in %d seconds" % (end - start))
        else:
            world.roads = []

        print('')
        return world
