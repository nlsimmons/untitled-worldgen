# from vars import *
import math
import pygame
from noise import pnoise2


class NoiseMap:
    def __init__(self, **kwargs):
        scale = kwargs.get('scale')
        if not scale:
            self.scale = 200.0
        else:
            self.scale = scale
        self.octaves = kwargs.get('octaves', 4)
        self.persistence = kwargs.get('persistence', 0.2)
        self.lacunarity = kwargs.get('lacunarity', 2.0)
        self.seed = kwargs.get('seed', 1)

        vals = []
        for x in range(kwargs.get('width')):
            for y in range(kwargs.get('height')):
                v = self.noise_at(x, y, normalize=False)
                vals.append(v)

        self._min = min(vals)
        self._max = max(vals)

    def noise_at(self, x, y, normalize=True):
        n = pnoise2(x / self.scale,
                    y / self.scale,
                    octaves=self.octaves,
                    persistence=self.persistence,
                    lacunarity=self.lacunarity,
                    base=self.seed)
        if normalize:
            return self.normalize(n)
        else:
            return n

    def normalize(self, val):
        """
        Normalize values to fit between 0 and 1
        """
        v = val - self._min
        v /= (self._max - self._min)
        return v

    def display(self, width=256, height=256):
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        background = pygame.Surface((width, height))
        background.convert()

        vals = []
        for x in range(width):
            for y in range(height):
                rgb = self.noise_at(x, y, normalize=False)
                vals.append(rgb)
                # color = (rgb, rgb, rgb)
                # background.set_at((x, y), color)

        self._min = min(vals)
        self._max = max(vals)

        for x in range(width):
            for y in range(height):

                rgb = int(self.noise_at(x, y) * 255)
                color = (rgb, rgb, rgb)
                background.set_at((x, y), color)

        running = True
        while running:
            screen.blit(background, (0, 0))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
        quit()

    def distance(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# NoiseMap(scale=200).display(1200, 800)

