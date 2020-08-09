# from vars import *
import math
import pygame
from noise import pnoise2


class NoiseMap:
    def __init__(self, **kwargs):
        self.scale = kwargs.get('scale', 200.0)
        self.octaves = kwargs.get('octaves', 2)
        self.persistence = kwargs.get('persistence', 0.5)
        self.lacunarity = kwargs.get('lacunarity', 2.0)
        self.seed = kwargs.get('seed', 1)

        val_range = set()
        for y in range(1000):
            for x in range(1000):
                val_range.add(self.noise_at(x, y, normalize=False))

        self._min = min(val_range)
        self._max = max(val_range)

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

        for x in range(width):
            for y in range(height):
                # d = distance(midpoint, (x, y)) / (width / 2)
                # dy = abs(y - mid_y)
                # dx = abs(x - mid_x)

                rgb = self.noise_at(x, y) * 255
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

# NoiseMap(scale=500).display(1200, 800)
