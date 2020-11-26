from colorzero import Color, Hue
from .Animation import Animation

class HueCycle(Animation):
    def __init__(self, tree):
        super().__init__(tree)
        tree.color = Color('red')
        self.name = "HueCycle"

    def loop(self, tree):
        tree.color += Hue(deg=1)