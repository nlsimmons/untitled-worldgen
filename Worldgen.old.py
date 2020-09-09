import pygame
import random
from scipy.spatial import Voronoi

random.seed(1)


def chance(prob):
    p_true = prob
    p_false = 100 - prob
    return random.choices((True, False), weights=(p_true, p_false))[0]


class Worldgen:
    def __init__(self):
        for _ in range(100):
            pass
            # x = random float
            # y = random float

            # population = random range(100, 10000)

        """
        // func worldgen
        settlement = random point
        culture = culture
        settlement.population = random range(100, 1000?)
        settlement.culture = culture
        settlement.features = random choice(river, forest, hills, coast)

        if settlement.population > 200
            number_of_satellites = round down(settlement.population/10)

        for number_of_satellites
            satellite = random point near settlement
            satellite.population = random range(50, 150)
            satellite.culture = culture

        worldgen() x random range (10, 100)?
        """


screen_x, screen_y = 1200, 600

pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
# font = pygame.font.SysFont(None, 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 168, 82)
BLUE = (66, 135, 245)
ORIGIN = (0, 0)

background = pygame.Surface(screen.get_size())
background.fill(GREEN)
background.convert()

# Landmass
vor_surface = pygame.Surface(screen.get_size())
vor_surface.convert_alpha()
vor_surface.set_colorkey(WHITE)
vor_surface.fill(WHITE)

n_points = 100
points = []
for _ in range(n_points):
    x = int(random.random() * screen_x)
    y = int(random.random() * screen_y)
    points.append((x, y))

for x, y in points:
    if chance(40):
        color = BLUE
    else:
        color = BLACK
    # pygame.draw.circle(vor_surface, color, (x, y), 8)
    pygame.draw.circle(vor_surface, BLACK, (x, y), 5)

vor = Voronoi(points)
vor.vertices
array([[0.5, 0.5],
       [0.5, 1.5],
       [1.5, 0.5],
       [1.5, 1.5]])


# # Population centers
# settlement_surface = pygame.Surface(screen.get_size())
# settlement_surface.convert_alpha()
# settlement_surface.set_colorkey(WHITE)
# settlement_surface.fill(WHITE)

# number_of_settlements = 50
# settlements = []
# for _ in range(number_of_settlements):
#     x = int(random.random() * screen_x)
#     y = int(random.random() * screen_y)
#     settlements.append((x, y))

# for x, y in settlements:
#     if chance(40):
#         color = BLUE
#     else:
#         color = BLACK
#     pygame.draw.circle(settlement_surface, color, (x, y), 8)
#     pygame.draw.circle(settlement_surface, BLACK, (x, y), 8, 1)


running = True
while running:
    screen.blit(background, ORIGIN)
    screen.blit(vor_surface, ORIGIN)
    # screen.blit(settlement_surface, ORIGIN)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
quit()

# Landmasses
# continent_surface = pygame.Surface(screen.get_size())
# continent_surface.set_colorkey((0, 0, 0))
# continent_surface = continent_surface.convert_alpha()

# Colored territory of each polity
# territory_surface = pygame.Surface(screen.get_size())
# territory_surface.convert_alpha()
# territory_surface.set_colorkey((0, 0, 0))


for settlement in entities:
    break
    scaled_region = [(int(x * scale), int(y * scale)) for x, y in settlement.region.points]
    settlement.scaled_region = scaled_region
    scaled_x = int(settlement.x * scale)
    scaled_y = int(settlement.y * scale)

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

    settlement.region.rect = pygame.draw.polygon(territory_surface, settlement.color, scaled_region)
    # settlement.region.rect = pygame.draw.aalines(territory_surface, settlement.color, True, scaled_region)
    pygame.draw.circle(territory_surface, BLACK, (scaled_x, scaled_y), 3)
    label_surfaces.append((settlement.name, scaled_x + 5, scaled_y + 5))

# tooltip_size = (150, 100)
# tooltip_anchor = ORIGIN
# alt_tooltip_anchor = (screen_x - tooltip_size[0], screen_y - tooltip_size[1])

# tooltip_surface = pygame.Surface(tooltip_size, pygame.SRCALPHA, 32)
# tooltip_surface.convert_alpha()

# year_display_surface = pygame.Surface((75, 25), pygame.SRCALPHA, 32)
# year_display_surface.convert_alpha()
