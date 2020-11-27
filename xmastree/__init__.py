from flask import Flask, send_from_directory, make_response, render_template
#from tree import RGBXmasTree
#from debugTree import FakeTree
from .tree import RGBXmasTree
from .debugTree import FakeTree
from .animationEngine import playAnimation, stopAnimation, animations, getThreadingInfos, getAnimationState
from .socketConnection import initSocket, sendToClients

import json
import os
#from gevent.pywsgi import WSGIServer

tree = None
isOn = False
lastColor = None

def create_app():
    app = Flask(__name__)
    initSocket(app)

    try:
        useTree = os.environ["TREE"]
    except KeyError:
        useTree = "Real"

    print(__name__)

    global tree
    if useTree == "Fake":
      tree = FakeTree()
    else:
      tree = RGBXmasTree(brightness=0.1)

    tree.on()
    global isOn
    isOn = True

    @app.route("/")
    def get_index():
        return render_template('index.html', anims=animations, keys=animations.keys())

    @app.route("/off/")
    def off():
        stopAnimation()
        global isOn
        isOn = False
        tree.off()
        return json_r(get_status())

    @app.route("/on/")
    def on():
        global isOn
        isOn = True

        #global lastColor
        #if lastColor == None:
        tree.on()
        #    lastColor = tree.color
        #else:
        #    tree.color = lastColor
        
        return json_r(get_status())

    @app.route('/status/')
    def status():

        return json_r(get_status())

    @app.route('/set/color/<color>/')
    def set_color(color):
        stopAnimation()
        try:
            col = hex_to_rgb(color)
            print(col)
            if col == (0.0,0.0,0.0):
                off()
            else:
                global isOn
                isOn = True
                tree.color = col
            # socketio.emit("status", get_status("socket"), broadcast=True)
            return json_r(get_status())
        except ValueError:
            return json_r(get_error("Not a Hex-Number"))

    @app.route('/set/brightness/<intensity>/')
    def set_brightness(intensity):
        tree.brightness = int(intensity) / 100
        return json_r(get_status())

    @app.route('/play/<name>')
    def play_animation(name):
        #global lastColor
        #global tree
        #lastColor = tree.color
        playAnimation(tree, name)
        return json_r(get_status())

    return app

def json_r(status):
    resp = make_response(status)
    resp.headers['Content-Type'] = "application/json"
    return resp


def hex_to_rgb(value):
    lv = len(value)
    v = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    normalized = (v[0] / 255, v[1] / 255, v[2] / 255)
    print(normalized)
    return normalized


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def get_status():
    global isOn
    s = json.dumps({
        'status': 0,
        'brightness': tree.brightness,
        'color': tree.color,
        'threads': getThreadingInfos(),
        'animation': getAnimationState(),
        'on': isOn
    })
    sendToClients(s)
    return s


def get_error(msg):
    return json.dumps({'status': 1, 'msg': msg})
