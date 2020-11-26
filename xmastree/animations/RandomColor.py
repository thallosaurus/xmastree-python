import time
import random
from .Animation import Animation

class RandomColor(Animation):
    def __init__(self, tree):
        super().__init__(tree)
        self.name = "RandomColor"

    def loop(self, tree):
        #print(self.tree)
        # print(tree)
        pixel = random.choice(tree)
        pixel.color = self.random_color()

    def random_color(self):
        r = random.random()
        g = random.random()
        b = random.random()
        return (r, g, b)