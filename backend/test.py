import socketio
import eventlet

sio = socketio.Client()

@sio.event
def connect():
    print("connected")

sio.connect("http://localhost:5000")