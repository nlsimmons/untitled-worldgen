from vars import *
import pygame
import random
import math
from pprint import pprint


width, height = 800, 600

screen_x, screen_y = width, height
screen = pygame.display.set_mode((screen_x, screen_y))

population = 100
households = int(population / 5.5)

households = 50

background = pygame.Surface(screen.get_size())
background.fill(WHITE)
background.convert()

points = []
for _ in range(households):
    x = random.uniform(0, width)
    y = random.uniform(0, height)

    vx = random.uniform(-1, 1)
    vy = random.uniform(-1, 1)

    # vx, vy = 0, 0

    points.append((int(x), int(y), (vx, vy)))

line0 = (int(random.uniform(0, width)), int(random.uniform(0, height)))
line1 = (int(width / 2), int(height / 2))

"""
draw a random line down the middle

each dot moves closer to the line and to the other dots

where they bunch up a road will be drawn

if they bunch up too much another road will be drawn

"""


def distance(point1, point2):
    """
    Calculates distance between the centroid of this region and the input region
    in units of km
    """
    x0, y0 = point1
    x1, y1 = point2
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


while True:
    point_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    point_surface.fill(WHITE)
    point_surface.set_colorkey(WHITE)
    point_surface.convert_alpha()

    pygame.draw.line(point_surface, BLACK, line0, line1)


    for p in points:
        x, y, v = p
        p = (int(x), int(y))
        pygame.draw.circle(point_surface, BLACK, p, 5)

    screen.blit(background, ORIGIN)
    # screen.blit(point_surface, ORIGIN)
    # pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()

    _points = []

    background.blit(point_surface, ORIGIN)
    pygame.display.flip()
    input()

    for p1 in points:
        _x, _y, (dx, dy) = p1
        pos1 = (_x, _y)

        sum_dx = dx
        sum_dy = dy

        for p2 in points:
            if p1 is p2:
                continue

            pos2 = (p2[0], p2[1])

            gravity = 0.001 / (distance(pos1, pos2) ** 1)

            if distance(pos1, pos2) < 15:
                sum_dx = 0
                sum_dy = 0
                # gravity = gravity * -1
                break

            dx = p1[0] - p2[0]
            dy = p1[1] - p2[1]

            sum_dx -= dx * gravity
            sum_dy -= dy * gravity

        dxc = _x - (width / 2)
        dyc = _y - (height / 2)

        new_x = _x + sum_dx
        new_y = _y + sum_dy
        v = (sum_dx, sum_dy)

        new_point = tuple((new_x, new_y, v))
        _points.append(new_point)

    points = _points
