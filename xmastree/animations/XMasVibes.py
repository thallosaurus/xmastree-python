import time
from time import sleep
import random
from .Animation import Animation

class XMasVibes(Animation):
    def __init__(self, tree):
        super().__init__(tree)
        self.name = "XMasVibes"

    def loop(self, tree):
      i = 0
      for x in tree:
        i += 1
        x.color = (0,1,0) if (i&0b01 == random.randint(0,1)) else (1,0,0)
      sleep(1)
