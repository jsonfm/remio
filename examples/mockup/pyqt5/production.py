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
    """A class for manage a mockup without a local GUI."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configureSerial()
        self.configureSocket()

    def configureSerial(self):
        """Configures serial on/emit events."""
        self.serial.on("ports", self.serialPortsUpdate)
        self.serial.on("connection", self.serialConnectionStatus)
        self.serial.on("data", self.serialDataIncoming)

    def configureSocket(self):
        """Configures socket on/emit events."""
        self.socket.on("connect", self.socketConnectionStatus)
        self.socket.on("disconnect", self.socketConnectionStatus)
        self.socket.on(DATA_SERVER_CLIENT, self.setControlVariables)

    def socketConnectionStatus(self):
        """Shows the connection socket status."""
        print("socket connection status :: ", self.socket.connected)

    def serialPortsUpdate(self, ports: list):
        """Sends to the server the list of serial devices."""
        self.socket.on("serial-ports", ports)

    def serialConnectionStatus(self, status: dict = {"arduino": False}):
        """Sends to the server the serial devices connection status."""
        print(f'serial status: {status}')
        self.socket.on("serial-connection", status)

    def serialDataIncoming(self, data:str):
        """Read incoming data from the serial device."""
        data = self.serial.toJson(data)
        self.socket.on(DATA_CLIENT_SERVER, data)

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
        serial=False, 
        socket=True, 
        streamer=True, 
        wait=True
    )