"""Example experiment with GUI."""
import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer
from remio import Mockup
from widgets import QImageLabel
from routes import *
from settings import (
    serverSettings,
    streamSettings,
    cameraSettings,
    serialSettings,
)
from utils import Variables, CountTimer


ui_path = os.path.dirname(os.path.abspath(__file__))
ui_file = os.path.join(ui_path, "gui.ui")


class CustomMockup(QMainWindow, Mockup):
    """A class for manage a mockup with a local GUI."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gui.ui", self)
        self.configureGUI()
        self.configureControlButtons()
        self.configureSerial()
        self.configureSocket()
        self.configureTimers()
        self.variables = Variables({
            "btn1": False,
            "btn2": False,
            "btn3": False,
        })
        # self.taskTimer = CountTimer(self, 1)

    def configureGUI(self):
        """Configures buttons events."""
        self.image = QImageLabel(self.qimage)
        self.pauseBtn.clicked.connect(lambda value: self.updateVideoPauseState(value))
        self.streamBtn.clicked.connect(lambda value: self.streamer.setPause(value))
        self.ledSerial.clicked.connect(lambda value: self.reconnectSerial(value))
        self.ledSocket.clicked.connect(lambda value: self.reconnectSocket(value))

    def configureControlButtons(self):
        """Configures the control buttons."""
        self.btn1.clicked.connect(lambda value: self.updateVariables("btn1", value))
        self.btn2.clicked.connect(lambda value: self.updateVariables("btn2", value))
        self.btn3.clicked.connect(lambda value: self.updateVariables("btn3", value))

    def configureSerial(self):
        """Configures serial on/emit events."""
        self.serial.on("connection", self.serialConnectionStatus)
        self.serial.on("ports", self.serialPortsUpdate)
        self.serial.on("data", self.serialDataIncoming)
        self.serialPortsUpdate(self.serial.ports())

    def configureSocket(self):
        """Configures socket on/emit events."""
        self.socket.on("connection", self.socketConnectionStatus)
        self.socket.on(DATA_SERVER_CLIENT, self.setVariables)

    def configureTimers(self):
        """Configures some timers."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateVideo)
        self.timer.start(1000 // 10)  # 1000 // FPS

    def socketConnectionStatus(self):
        """Shows the connection socket status."""
        status = self.socket.isConnected()
        self.ledSocket.setChecked(status)
        if status:
            self.socket.emit(JOIN_ROOM_CLIENT, "room-x")

    def serialPortsUpdate(self, ports: list):
        """Sends to the server the list of serial devices."""
        event = {"serial": {"ports": ports}}
        self.socket.emit(EVENT_CLIENT_SERVER, event)
        self.devices.clear()
        self.devices.addItems(ports)

    def serialConnectionStatus(self, status: dict = {"arduino": False}):
        """Sends to the server the serial devices connection status."""
        self.ledSerial.setChecked(status.get("arduino", False))

    def serialDataIncoming(self, data: str):
        """Reads incoming data from the serial device."""
        data = self.serial.toJson(data)
        self.socket.on(DATA_CLIENT_SERVER, data)

    def setVariables(self, data: dict = {}):
        """Writes data coming from the server to the serial device."""
        self.btn1.setChecked(data["btn1"])
        self.btn2.setChecked(data["btn2"])
        self.btn3.setChecked(data["btn3"])

        # Say to the server the data were received (OK)
        self.socket.emit(DATA_OK_CLIENT_SERVER) 
        print("data: ", data)

    def reconnectSerial(self, value: bool):
        """Updates the serial port."""
        if value:
            self.serial["arduino"].setPort(self.devices.currentText())
        else:
            self.serial["arduino"].disconnect()
        self.ledSerial.setChecked(self.serial["arduino"].isConnected())

    def reconnectSocket(self, value: bool = True):
        """Updates the socketio connection."""
        self.socket.toogle(value)
        self.ledSocket.setChecked(self.socket.isConnected())

    def updateVideo(self):
        """Updates video image."""
        image = self.camera.getFrameOf("webcam")
        self.image.setImage(image, 400, 300)
        self.streamer.stream({"webcam": image})

    def updateVideoPauseState(self, status: bool):
        """Updates video pause status."""
        self.camera["webcam"].setPause(status)
        self.streamer.setPause(status)

    def checkVariablesSet(self):
        if not self.variables.updated:
            self.setVariables(self.variables.values())

    def updateVariables(self, key: str, value: None):
        """When a GUI event ocurrs, it updates the corresponding variables."""
        self.variables.set(key, value)

        # Send changes to the server
        self.socket.emit(DATA_CLIENT_SERVER, self.variables.json())

    def closeEvent(self, e):
        """Stops running threads/processes when close the window."""
        self.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    experiment = CustomMockup(
        serverSettings=serverSettings,
        streamSettings=streamSettings,
        cameraSettings=cameraSettings,
        serialSettings=serialSettings,
    )
    experiment.start(
        camera=True, 
        serial=False, 
        socket=True, 
        streamer=False, 
        wait=False
    )
    experiment.show()
    sys.exit(app.exec_())
