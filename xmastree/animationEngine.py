from .tree import RGBXmasTree
import random
import _thread
from xmastree.animations.RandomColor import RandomColor
from xmastree.animations.OneByOne import OneByOne
from xmastree.animations.HueCycle import HueCycle
from xmastree.animations.XMasVibes import XMasVibes
import threading

#tree = RGBXmasTree()

animations = {
    "random": RandomColor,
    "onebyone": OneByOne,
    "huecycle": HueCycle,
    "xmasvibes": XMasVibes
}

thread = None
animName = ""

def stopAnimation():
    global thread
    if thread != None:
        if thread.is_alive():
            thread.stop()
            thread = None
            global animName
            animName = ""

def playAnimation(tree, name):
    stopAnimation()
    print("playing " + name)
    global animName
    animName = name
    # print(globals()[name])
    global thread
    a = getAnimationFromList(name)
    if a != False:
        thread = a(tree)
        thread.start()

def getAnimationState():
    global thread
    return {
        "playing": thread != None,
        "name": animName or "Not Playing"
    }

def getAnimationFromList(tag):
    global animations
    if tag in animations:
        return animations[tag]
    else:
        return False

def getThreadingInfos():
    # print(threading.enumerate())
    a = []
    for i in threading.enumerate():
        a.append({
            'name': i.name,
            'is_alive': i.is_alive()
        })
    return list(a)
