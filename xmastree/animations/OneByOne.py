import time
import random
from .Animation import Animation
from colorzero import Color

class OneByOne(Animation):
    def __init__(self, tree):
        super().__init__(tree)
        self.name = "OneByOne"
        self.colors = colors = [Color('red'), Color('green'), Color('blue')]

    def loop(self, tree):
        for color in self.colors:
            for pixel in tree:
                pixel.color = color