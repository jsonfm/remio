"""Example experiment.

author: Jason Francisco Macas Mora
email: franciscomacas3@gmail.com
license: Apache 2.0
year: 2022

"""
from remio import Mockup
from routes import *
from settings import (
    serverSettings,
    streamSettings,
    cameraSettings,
    serialSettings,
)


class CustomMockup(Mockup):
    """A class for manage a mockup."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configureSerial()
        self.configureSocket()

    def configureSerial(self):
        """Configures serial on/emit events."""
        self.serial.on("ports-update", self.serialPortsUpdate)
        self.serial.on("connection-status", self.serialConnectionStatus)
        self.serial.on("data-incoming", self.serialDataIncoming)

    def configureSocket(self):
        """Configures socket on/emit events."""
        self.socket.on("connect", self.socketConnectionStatus)
        self.socket.on("disconnect", self.socketConnectionStatus)
        self.socket.on(RECEIVE_DATA_FROM_SERVER, self.setControlVariables)

    def socketConnectionStatus(self, status: bool):
        """Shows the connection socket status."""
        print("socket connection status :: ", status)

    def serialPortsUpdate(self, ports: list):
        """Sends to the server the list of serial devices."""
        self.socket.on("serial-ports-update", ports)

    def serialConnectionStatus(self, status: dict = {"arduino": False}):
        """Sends to the server the serial devices connection status."""
        print(f'serial status: {status}')
        self.socket.on("serial-connection-status", status)

    def serialDataIncoming(self, data:str):
        """Read incoming data from the serial device."""
        data = self.serial.toJson(data)
        self.socket.on(SEND_DATA_TO_SERVER, data)

    def setControlVariables(self, data: dict = {"arduino": {}}):
        """Writes data coming from   the server to the serial device."""
        self.serial.write(message=data, asJson=True)


if __name__ == "__main__":
    experiment = CustomMockup(
        serverSettings=serverSettings,
        streamSettings=streamSettings,
        cameraSettings=cameraSettings,
        serialSettings=serialSettings,
    )  
    experiment.start(
        camera=True, 
        serial=True, 
        socket=True, 
        streamer=False, 
        wait=True
    )