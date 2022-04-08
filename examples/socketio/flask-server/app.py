import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from numpy import broadcast


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def connect(ssid):
    print("Bienvenido: ", ssid)


@socketio.on("disconnect")
def disconnect():
    print("Desconectando...")


@socketio.on("stream")
def stream(frame):
    emit("stream", frame, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)
