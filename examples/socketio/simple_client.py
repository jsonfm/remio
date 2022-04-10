"""Simple socketio client."""
import time
from remio import CustomSocketIO

# Intialize the socketio client
socket = CustomSocketIO(address="http://localhost:5000")

# Define routes
socket.on("connection", lambda: print(f"-> connected: {socket.isConnected()}"))
socket.on("message", lambda response: print(f"- server says: {response}"))

# run the socketio client
socket.start()

# Emit some message to the server
time.sleep(1)
message = "Hi, I'm a python socketio client."
print(f"- client says: {message}")
socket.emit("message", message)
