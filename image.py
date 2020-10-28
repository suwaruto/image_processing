import pygame
import math
import random

def _dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) 

class image(object):

    def __init__(self, image_path):
        self._surface = pygame.image.load(image_path)
        
    def get_surface(self):
        return self._surface

    def _filter(func):
        def wrapper(self, *args):
            trt = pygame.Surface((self._surface.get_width(),
            self._surface.get_height()))
            pxarr_trt = pygame.PixelArray(trt)
            x_c = pxarr_trt.shape[0] // 2
            y_c = pxarr_trt.shape[1] // 2
            s_width = self._surface.get_width()
            s_height = self._surface.get_height()
            for y in range(pxarr_trt.shape[1]):
                for x in range(pxarr_trt.shape[0]):
                    x_src, y_src = func(self, x, y, x_c, y_c, *args)                  
                    if x_src < s_width and y_src < s_height \
                        and x_src >= 0 and y_src >= 0:
                            pxarr_trt[x, y] = self._surface.get_at((x_src, y_src))
            pxarr_trt.close()
            self._surface = trt 

        return wrapper

    @_filter
    def rotate(self, x, y, x_c, y_c, angle = math.radians(30)):
        return (int((x - x_c) * math.cos(angle) +
                    (y - y_c) * math.sin(angle) + x_c),
                    int(-(x - x_c) * math.sin(angle) + 
                    (y - y_c) * math.cos(angle) + y_c))

    @_filter
    def swirl(self, x, y, x_c, y_c):
       angle = _dist(x, y, x_c, y_c) * math.pi / 256 
       return (int((x - x_c) * math.cos(angle) +
                    (y - y_c) * math.sin(angle) + x_c),
                    int(-(x - x_c) * math.sin(angle) + 
                    (y - y_c) * math.cos(angle) + y_c))

    @_filter
    def wave(self, x, y, x_c, y_c, amplitude = 20, frequency = 64):
        return (x, int(y + amplitude * math.sin(2 * math.pi * x / frequency)))

    @_filter
    def glass(self, x, y, x_c, y_c):
        return (random.randint(-4, 4) + x, random.randint(-4, 4) + y)

    def tile(self, cols = 100, rows = 100):
        s_height = self._surface.get_height()
        s_width = self._surface.get_width()
        for y in range(0, s_height, s_height // rows):
            for x in range(0, s_width, s_width // cols):
                pygame.draw.line(self._surface, (0, 0, 0), (0, y), (s_width, y))
                pygame.draw.line(self._surface, (0, 0, 0), (x, 0), (x, s_height))

    def scale(self, width, height):
        trt = pygame.Surface((width, height))
        pxarr_trt = pygame.PixelArray(trt)
        s_width = self._surface.get_width()
        s_height = self._surface.get_height()
        for y in range(pxarr_trt.shape[1]):
            for x in range(pxarr_trt.shape[0]):
                x_src, y_src = (x * s_width // width, y * s_height // height)                  
                if x_src < s_width and y_src < s_height \
                    and x_src >= 0 and y_src >= 0:
                        pxarr_trt[x, y] = self._surface.get_at((x_src, y_src))
        pxarr_trt.close()
        self._surface = trt 

    def random_filter(self):
        seq = [self.swirl, self.wave, self.rotate, self.glass, self.tile]
        return random.choice(seq)
