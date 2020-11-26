import threading
import time
import random

exitFlag = 0

class Animation(threading.Thread):
    def __init__(self, t):
        threading.Thread.__init__(self)
        #self.threadID = threadID
        self.name = "Animation Thread"

        self.tree = t
        # print(tree)
        self.playing = True

    def run(self):
        print("Starting " + self.name)
        while self.playing:
            self.loop(self.tree)

        print("Exiting " + self.name)

    def stop(self):
        self.playing = False

    def loop(self, tree):
        pass
