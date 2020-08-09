from vars import *
import pygame
import random
# import sympy
import math
from pprint import pprint
from sympy.geometry import Point  # , Polygon
from scipy.spatial import Voronoi
from Language import Language, Culture
from Places import World, Region, Subregion, Settlement, Road
from perlin import NoiseMap
import copy
import time

random.seed(1)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 168, 82)
BLUE = (66, 135, 245)
DARK_BLUE = (0, 0, 139)
DARK_GREEN = (59, 85, 38)
RED = (255, 0 , 0)
ORIGIN = (0, 0)


def textbox(text, padding, fill=(0, 0, 0, 127), width=200):
    height = (len(text) + 2) * 20

    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    surface.convert_alpha()
    surface.fill(fill)
    px, py = padding

    for line in text:
        rendered_text = font.render(line, True, WHITE)
        surface.blit(rendered_text, (px, py))
        py += 20
    return surface


def random_color():
    r = random.randrange(1, 255)
    g = random.randrange(1, 255)
    b = random.randrange(1, 255)
    return (r, g, b)


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
        n_regions = int(kwargs.get('n_regions'))
        avg_geo_area = kwargs.get('avg_geo_area', 1000)  # Average geographical area of each subregion in sqkm

        regions = cls.voronoi_map(n_regions, **kwargs)
        regions = cls.clip_regions(regions)

        regions = [Region(r) for r in regions]
        for region in regions:
            if any(cls.point_is_oob(n) for n in region.points):
                region.type = 'ocean'
        non_ocean = [r for r in regions if r.type != 'ocean']

        if percent_ocean:
            n_ocean_regions = int(len(non_ocean) * percent_ocean)
            current = random.choice(non_ocean)
            ocean_regions = set([current])
            while len(ocean_regions) < n_ocean_regions:
                current.type = 'ocean'
                bordered = current.bordered(non_ocean)
                if not bordered:
                    break
                for b in bordered:
                    b.type = 'ocean'
                    ocean_regions.add(b)
                    if len(ocean_regions) > n_ocean_regions:
                        break
                current = random.choice(regions)

        n_subdivisions = kwargs.get('n_divisions') * n_regions
        subregions = cls.voronoi_map(n_subdivisions, **kwargs)
        subregions = [Subregion(r) for r in cls.clip_regions(subregions)]

        n_display_regions = n_subdivisions * 10
        display_regions = cls.voronoi_map(n_display_regions, **kwargs)
        display_regions = [Subregion(r) for r in cls.clip_regions(display_regions)]

        avg_area = sum(s.area for s in subregions) / len(subregions)

        scale = math.sqrt(avg_area) / math.sqrt(avg_geo_area)  # u / km

        heightmap = NoiseMap(width=cls.width, height=cls.height, scale=500, seed=5)
        weathermap = NoiseMap(width=cls.width, height=cls.height, seed=10)
        end = time.time()
        print("Finished in %d seconds" % (end - start))

        print('')
        print("Carving out the landscape...")
        start = time.time()
        world = World(regions=regions,
                      subregions=subregions,
                      display_regions=display_regions,
                      scale=scale,
                      heightmap=heightmap,
                      weathermap=weathermap,
                      **kwargs)
        end = time.time()
        print("Finished in %d seconds" % (end - start))

        ###############################################

        print('')
        print("Dropping people from the sky...")
        start = time.time()

        invalid = []
        for region in world.regions:
            try:
                region.populate()
            except IndexError:
                invalid.append(region)
        for i in invalid:
            world.regions.remove(i)
            del i

        end = time.time()
        print("Finished in %d seconds" % (end - start))

        ###############################################

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

        world.river_sources = random.choices(top_rainfall + top_elevation, k=20)
        for s in world.river_sources:
            s.river_count = 1

        elevation_regions = list(copy.copy(world.land))
        bottom_elevation = sorted(elevation_regions, key=lambda r: r.elevation)[0:int(n / 2)]

        elevation_regions = list(copy.copy(world.land))
        top_elevation = sorted(elevation_regions, key=lambda r: r.elevation, reverse=True)[0:int(n * 0.5)]

        # world.river_sources = random.choices([r for r in top_rainfall if r in top_elevation], k=int(n / 100))
        # world.lake_cells = random.choices(
        #     [r for r in top_rainfall if r in bottom_elevation and r.type != 'coast'],
        #     k=int(n / 100)
        # )

        # rivers = []
        # for s in river_sources:
        #     river = []
        #     current = s
        #     while True:
        #         b = s.bordered(world.subregions)
        #         next_options = sorted(b, key=lambda r: r.elevation)

        #         # for c in next_options:

        #         # river.append((current, next))

        #         # if next.rivers:
        #         #     next.rivers += 1
        #         #     break
        #         # else:
        #         #     next.rivers = 1
        #         current = next
        #     rivers.append(river)
        # world.rivers = rivers
        # world.lake_cells = lake_cells
        end = time.time()
        print("Finished in %d seconds" % (end - start))

        ###############################################

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
                    b = current.bordered(world.land)
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
        end = time.time()
        print("Finished in %d seconds" % (end - start))

        ###############################################

        # print("Populating settlements...")
        # for region in world.subregions:
        #     region.populate()

        print('')
        return world


screen_x, screen_y = 1200, 800

pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
font = pygame.font.SysFont(None, 24)

# background = pygame.Surface((screen.get_width() * 2, screen.get_height() * 2))
background = pygame.Surface(screen.get_size())
# background.fill(BLUE)
background.convert()

# Landmass
# vor_surface = pygame.Surface(screen.get_size())
# vor_surface.convert_alpha()
# vor_surface.set_colorkey(WHITE)
# vor_surface.fill(WHITE)

# world_surface = pygame.Surface((screen.get_width() * 2, screen.get_height() * 2))

world_surface = pygame.Surface((screen.get_size()))

world_surface.convert_alpha()
world_surface.set_colorkey(WHITE)
world_surface.fill(DARK_BLUE)

n_regions = 25
n_divisions = 15
world = Worldgen.new(n_regions=n_regions,
                     n_divisions=n_divisions,
                     width=screen_x,
                     height=screen_y,
                     percent_ocean=50,
                     relax_passes=2)

# player_gender = 'male'
# choices = []

# while not len(choices):
#     region = random.choice(list(world.regions))
#     s = region.settlements[0]
#     choices = [p for p in s.populace.people if 18 < p.age < 22 and p.alive and p.gender == player_gender]
# you = random.choice(choices)

# ======================


# world_offset_x = world.width / 2
# world_offset_y = world.height / 2
world_offset_x = 0
world_offset_y = 0


# Draw world
# for sr in world.sea:
#     color = DARK_BLUE
#     vertices = [(int(node.x), int(node.y)) for node in sr.nodes]
#     pygame.draw.polygon(world_surface, color, vertices)
#     pygame.draw.polygon(world_surface, BLACK, vertices, 1)

for sr in world.land:
    if sr.type == 'coast':
        color = DARK_GREEN
    else:
        color = GREEN

    if sr.subregions:
        for dr in sr.subregions:
            vertices = [(int(x), int(y)) for x, y in dr.points]
            pygame.draw.polygon(world_surface, color, vertices)
            # pygame.draw.polygon(world_surface, BLACK, vertices, 1)
    else:
        vertices = [(int(x), int(y)) for x, y in sr.points]
        pygame.draw.polygon(world_surface, color, vertices)
        # pygame.draw.polygon(world_surface, BLACK, vertices, 1)

    # vertices = [(int(node.x), int(node.y)) for node in sr.nodes]
    # pygame.draw.polygon(world_surface, BLACK, vertices, 1)

    if sr is sr.region.capital:
        x, y = sr.centroid
        pygame.draw.circle(world_surface, BLACK, (int(x), int(y)), 5, 1)

for b in world.borders:
    if 'ocean' in b.type:
        continue
    elif 'coast' in b.type or 't2' in b.type:
        weight = 1
    elif 't1' in b.type:
        weight = 3
    else:
        continue

    n1, n2 = b.nodes
    n1x, n1y = n1.coords
    n2x, n2y = n2.coords
    pygame.draw.line(world_surface, BLACK, (int(n1x), int(n1y)), (int(n2x), int(n2y)), weight)

    # if sr in world.lake_cells:
    #     pygame.draw.circle(world_surface, DARK_BLUE, sr.centroid, 5)

    # if sr in world.river_sources:
    #     pygame.draw.circle(world_surface, BLUE, sr.centroid, 5, 1)

    # if sr in low_elevation:
    #     pygame.draw.circle(world_surface, BLACK, sr.centroid, 5, 1)

    # if sr in high_elevation:
    #     pygame.draw.circle(world_surface, RED, sr.centroid, 10, 1)

# river_sources = [n for n in world.nodes if n.elevation > 0]

# nodes = list(copy.copy(world.nodes))
# n = len(river_sources)
# river_sources = sorted(river_sources, key=lambda r: r.precipitation, reverse=True)[0:int(n / 10)]

# for n in river_sources:
#     x, y = n.coords
#     pygame.draw.circle(world_surface, DARK_BLUE, (int(x), int(y)), 3)


# for n in world.nodes:
#     # if n.elevation > 0:
#     #     x, y = n.coords
#     #     pygame.draw.circle(world_surface, DARK_BLUE, (int(x), int(y)), 5, 1)


# Draw roads
# try:
for road in world.roads:
    for road_segment in road.segments:
        r1, r2 = road_segment
        r1x, r1y = r1.centroid
        r2x, r2y = r2.centroid
        pygame.draw.line(world_surface, BLACK, (int(r1x), int(r1y)), (int(r2x), int(r2y)), 3)
# except AttributeError:
#     pass

# Draw rivers
# for river in world.rivers:
#     for river_segment in river:
#         r1, r2 = river_segment
#         pygame.draw.line(world_surface, DARK_BLUE, r1.centroid, r2.centroid, 3)

for source in world.river_sources:
    x = int(source.x)
    y = int(source.y)
    pygame.draw.circle(world_surface, DARK_BLUE, (x, y), 5)

    traversed = []
    elevation = source.elevation
    current = source
    segments = []
    while elevation > 0:
        try:
            next = sorted(([n for n in current.neighbors() if n not in traversed]),
                          key=lambda r: r.elevation)[0]
            segments.append((current, next))

            if next.river_count:
                next.river_count += 1
                break

            elevation = next.elevation
            traversed.append(next)
            current = next
        except IndexError:
            break

    for p1, p2 in segments:
        x1 = int(p1.x)
        x2 = int(p2.x)
        y1 = int(p1.y)
        y2 = int(p2.y)
        pygame.draw.line(world_surface, DARK_BLUE, (x1, y1), (x2, y2), 3)


tooltip_size = (250, 100)
tooltip_anchor = ORIGIN
alt_tooltip_anchor = (screen_x - tooltip_size[0], screen_y - tooltip_size[1])

# tooltip_surface = pygame.Surface(tooltip_size, pygame.SRCALPHA, 32)
# tooltip_surface.convert_alpha()

# cursor_pos_surface = pygame.Surface((75, 50), pygame.SRCALPHA, 32)
# cursor_pos_surface.convert_alpha()

# cursor_pos_surface = pygame.Surface((75, 50), pygame.SRCALPHA, 32)
# cursor_pos_surface.convert_alpha()


running = True
while running:
    screen.blit(background, ORIGIN)
    # screen.blit(vor_surface, ORIGIN)
    off_y = ((screen_y - world.height) / 2) - world_offset_y
    off_x = ((screen_x - world.width) / 2) - world_offset_x
    off_x = 0
    off_y = 0
    screen.blit(world_surface, (int(off_x), int(off_y)))
    # screen.blit(weather_surface, (int(off_x), int(off_y)))
    # screen.blit(settlement_surface, ORIGIN)

    # cursor position
    if pygame.mouse.get_focused():
        cursor_x, cursor_y = pygame.mouse.get_pos()

        text = []

        for display_region in world.land:
            try:
                if(display_region.maybe_encloses((cursor_x, cursor_y))
                   and display_region.encloses((cursor_x, cursor_y))):
                    subregion = display_region.region
                    region = subregion.region
                    text.append(f'Region: {region.name}')
                    text.append(f'Locale: {subregion.name}')
                    # text.append(f'Region of {region.name}')
                    # text.append(f'City Population: {region.settlements[0].population}')
                    text.append(f'Population: {int(subregion.population)}; Area: {int(subregion.geo_area)} sqkm')
                    # text.append(f'Elevation: {subregion.elevation}')
                    # text.append(f'Precipitation: {subregion.precipitation}')
                    # text.append(f'Number of cities: {len(region.cities)}')
                    # text.append(f'Number of towns: {len(region.towns)}')
            except (AttributeError, IndexError) as e:
                pprint(e)

        if text:
            tooltip_surface = textbox(text, (20, 20), fill=(*BLACK, 127), width=300)

            if tooltip_surface.get_rect().collidepoint(pygame.mouse.get_pos()):
                tt_anchor = alt_tooltip_anchor
            else:
                tt_anchor = tooltip_anchor

            screen.blit(tooltip_surface, tt_anchor)

        # text = ('x: %s' % int(cursor_x / scale), 'y: %s' % int(cursor_y / scale))
        # cursor_pos_surface = textbox(cursor_pos_surface, text, (20, 5), fill=BLACK, width=75)
        # screen.blit(cursor_pos_surface, (0, screen_y - 50))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
quit()


# Here establish initial culture and landscape
#   forest 1-10
#   hills 1-10
#   metal / other resource availability (does not affect low tech societies)
#   water
#   land fertility  (affected by all the preceding)
#   leadership
#   gender_role - randomized
#   sedentism - high in areas with high resources
#   violence - high in areas with few resources
#   plants and livestock - randomized

# Roughly 50% of world is forest

# year_display_surface = pygame.Surface((75, 25), pygame.SRCALPHA, 32)
# year_display_surface.convert_alpha()
