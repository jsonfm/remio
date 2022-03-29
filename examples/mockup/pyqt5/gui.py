"""Example experiment.

author: author@example.com 
license: MIT
year: 2022

"""
import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer
from remio import Mockup
from widgets import QImageLabel
from settings import (
    serverSettings,
    streamSettings,
    cameraSettings,
    serialSettings,
)


ui_path = os.path.dirname(os.path.abspath(__file__))
ui_file = os.path.join(ui_path, 'gui.ui')


class CustomMockup(QMainWindow, Mockup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('gui.ui', self)

        self.image = QImageLabel(self.qimage)
        self.serial.on('ports-update', self.updatePortsList)
        self.pauseBtn.clicked.connect(self.updateVideoControl)
        self.streamBtn.clicked.connect(self.updateSocket)
        self.updatePortsList(self.serial.getListOfPorts())
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateVideo)
        self.timer.start(1000/20)

    def updateSocket(self, status):
        if status:
            try:
                self.socket.connect('http://localhost:5000', wait=False)
            except Exception as e:
                print("socket:: ", e)
        else:
            self.socket.disconnect()

    def updatePortsList(self, ports:list):
        self.devices.clear()
        self.devices.addItems(ports)

    def updateVideo(self):
        frame = self.camera.getFrame64Of('webcam')
        image = self.camera.getFrameOf('webcam')
        self.image.setImage(image)
        if self.socket.connected:
            self.socket.emit('stream', {'webcam': frame})

    def updateVideoControl(self, status):
        if status:
            self.camera['webcam'].pause()
        else:
            self.camera['webcam'].resume()

    def closeEvent(self, e):
        self.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    experiment = CustomMockup(
        serverSettings=serverSettings,
        streamSettings=streamSettings,
        cameraSettings=cameraSettings,
        serialSettings=serialSettings,
    )
    experiment.start(camera=True, serial=True, streamer=True)
    experiment.show()
    sys.exit(app.exec_())
