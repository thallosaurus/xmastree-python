from flask_socketio import SocketIO, emit
#from xmastree import get_status

socketio = None

def initSocket(app):
    global socketio
    socketio = SocketIO(app)
    socketio.run(app)

    @socketio.on('connect')
    def connect():
        print("Someone connected")

def sendToClients(data):
    global socketio
    socketio.emit("status", data, broadcast=True)
#     socketio.emit("status", s, broadcast=True)