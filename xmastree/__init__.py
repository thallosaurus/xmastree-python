from flask import Flask, send_from_directory, make_response, render_template
#from tree import RGBXmasTree
#from debugTree import FakeTree
from .tree import RGBXmasTree
from .debugTree import FakeTree
import json
#from gevent.pywsgi import WSGIServer

tree = None

def create_app():
    app = Flask(__name__)

    config = {
      "useRealTree": False
    }

    print(__name__)

    app.config.update(config)


    global tree
    if app.config["useRealTree"] == True:
      tree = RGBXmasTree()
    else:
      tree = FakeTree()

    @app.route("/")
    def get_index():
        return render_template('index.html')

    @app.route("/off/")
    def off():
        tree.off()
        return json_r(get_status())

    @app.route("/on/")
    def on():
        tree.on()
        return json_r(get_status())

    #@app.route("/<path:path>")
    #def send(path):
    #    return send_from_directory('client', path)

    @app.route('/status/')
    def status():
        return json_r(get_status())

    @app.route('/set/color/<color>/')
    def set_color(color):
        try:
            tree.color = hex_to_rgb(color)
            return json_r(get_status())
        except ValueError:
            return json_r(get_error("Not a Hex-Number"))

    @app.route('/set/brightness/<intensity>/')
    def set_brightness(intensity):
        tree.brightness = int(intensity) / 100
        return json_r(get_status())

    return app

# @app.after_request
# def add_header(response):
#  response.headers['Content-type'] = 'application/json'
#  return response


def json_r(status):
    resp = make_response(status)
    resp.headers['Content-Type'] = "application/json"
    return resp


def hex_to_rgb(value):
    # value = value.lstrip('#')
    lv = len(value)
    v = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    normalized = (v[0] / 255, v[1] / 255, v[2] / 255)
    print(normalized)
    return normalized


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def get_status():
    return json.dumps({'status': 0, 'brightness': tree.brightness, 'color': tree.color})


def get_error(msg):
    return json.dumps({'status': 1, 'msg': msg})