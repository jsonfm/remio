"""Simple socketio server for test socketio client."""
import eventlet
import socketio

# Initialize server app
sio = socketio.Server()
app = socketio.WSGIApp(sio)

# Define events
@sio.event
def connect(sid, environ):
    print(f"-> connect: {sid}")


# Receive a message from the client, and response to it
@sio.event
def message(sid, data):
    print(f"-> message from {sid}: {data}")
    sio.emit("message", "Welcome.")


# If some client disconnect
@sio.event
def disconnect(sid):
    print("disconnect: ", sid)


if __name__ == "__main__":
    # export EVENTLET_HUB=poll -> export this if you have some trouble starting server
    eventlet.wsgi.server(eventlet.listen(("", 5000)), app)
