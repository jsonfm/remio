"""Example experiment.

author: Jason Francisco Macas Mora
email: franciscomacas3@gmail.com
license: Apache 2.0
year: 2022

"""
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


ui_path = os.path.dirname(os.path.abspath(__file__))
ui_file = os.path.join(ui_path, "gui.ui")


class CustomMockup(QMainWindow, Mockup):
    """A class for manage a mockup."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gui.ui", self)
        self.configureGUI()
        self.configureSerial()
        self.configureSocket()

    def configureGUI(self):
        """Configures buttons events."""
        self.image = QImageLabel(self.qimage)
        self.pauseBtn.clicked.connect(lambda value: self.updateVideoPauseState(value))
        self.ledSerial.clicked.connect(lambda value: self.updateSerialPort(value))

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateVideo)
        self.timer.start(1000 // 12) # 1000 / FPS

    def configureSerial(self):
        """Configures serial on/emit events."""
        self.serial.on("ports-update", self.serialPortsUpdate)
        self.serial.on("connection-status", self.serialConnectionStatus)
        self.serial.on("data-incoming", self.serialDataIncoming)
        self.serialPortsUpdate(self.serial.getListOfPorts())

    def configureSocket(self):
        """Configures socket on/emit events."""
        self.socket.on("connect", self.socketConnectionStatus)
        self.socket.on("disconnect", self.socketConnectionStatus)
        self.socket.on(RECEIVE_DATA_FROM_SERVER, self.setControlVariables)

    def socketConnectionStatus(self, status: bool):
        """Shows the connection socket status."""
        self.ledSocket.setChecked(status)

    def serialPortsUpdate(self, ports: list):
        """Sends to the server the list of serial devices."""
        self.socket.on("serial-ports-update", ports)
        self.devices.clear()
        self.devices.addItems(ports)

    def serialConnectionStatus(self, status: dict = {"arduino": False}):
        """Sends to the server the serial devices connection status."""
        self.socket.on("serial-connection-status", status)
        self.ledSerial.setChecked(status["arduino"])

    def serialDataIncoming(self, data:str):
        """Read incoming data from the serial device."""
        data = self.serial.toJson(data)
        self.socket.on(SEND_DATA_TO_SERVER, data)

    def setControlVariables(self, data: dict = {"arduino": {}}):
        """Writes data coming from   the server to the serial device."""
        self.serial.write(message=data, asJson=True)

    def updateSerialPort(self, value: bool):
        if value:
            port = self.devices.currentText()
            self.serial["arduino"].port = port
            self.serial["arduino"].connect()
        else:
            self.serial["arduino"].disconnect()
        self.ledSerial.setChecked(self.serial["arduino"].isConnected())

    def updateVideo(self):
        """Updates video image."""
        frame = self.camera.getFrame64Of("webcam")
        image = self.camera.getFrameOf("webcam")
        self.image.setImage(image, 400, 300)
        self.streamer.stream({"webcam": frame})

    def updateVideoPauseState(self, status):
        """Update video pause status."""
        self.camera["webcam"].setPause(status)

    def closeEvent(self, e):
        """stops running threads/processes when close the windows."""
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
        serial=True, 
        streamer=False, 
        wait=False
    )
    experiment.show()
    sys.exit(app.exec_())
