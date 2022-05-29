"""Example experiment."""
from remio import Mockup
from routes import *
from settings import (
    serverSettings,
    streamSettings,
    cameraSettings,
    serialSettings,
)
from utils import Variables, PausableTimer


MOCKUP_ROOM = "room-x"


class CustomMockup(Mockup):
    """A class for manage a mockup without a local GUI."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configureSerial()
        self.configureSocket()
        self.configureTimers()
        self.configureVariables()

    def configureSerial(self):
        """Configures serial on/emit events."""
        self.serial.on("data", self.serialDataIncoming)

    def configureSocket(self):
        """Configures socket on/emit events."""
        self.socket.on("connection", self.socketConnectionStatus)
        self.socket.on(DATA_SERVER_CLIENT, self.receiveVariables)
        self.socket.on(DATA_OK_SERVER_CLIENT, self.streamVariablesOK)

    def configureTimers(self):
        """Configures some timers."""
        self.variablesTimer = PausableTimer(3, self.superviseVariablesStreaming)

    def configureVariables(self):
        """Configures control variables."""
        self.variables = Variables({
            "btn1": False,
            "btn2": False,
            "btn3": False,
        })

    def serialDataIncoming(self, data: str):
        """Reads incoming data from the serial device."""
        message = data["arduino"]
        if "$" in message:
            print("message: ", message)
        else:
            self.variables.update(message)
            self.variables.setUpdated(False)
            self.streamVariables()

    def socketConnectionStatus(self):
        """Shows the connection socket status."""
        if self.socket.isConnected(): 
            self.socket.emit(JOIN_ROOM_CLIENT, MOCKUP_ROOM)

    def superviseVariablesStreaming(self):
        """"Checks the variables updated status and restores the backup if necessary."""
        # If variables not reached the web then restore the backup
        if not self.variables.updated():
            self.variables.restore()
        
        # Reset updated variables status and unlock the GUI
        self.variables.setUpdated(False)
        self.variablesTimer.pause(reset=True)

    # Variables
    def receiveVariables(self, data: dict = {}):
        """Receives variables coming from the server."""
        print("--> received: ", data)
        self.variables.update(data)
        self.serial["arduino"].write(self.variables.json())
        
        # Say to the server the data were received (OK)
        self.socket.emit(DATA_OK_CLIENT_SERVER)

    def streamVariables(self):
        """Streams variables to the web."""
        # Send changes to the server
        self.socket.emit(DATA_CLIENT_SERVER, self.variables.json())

        # Lock the GUI a wait for a response
        self.variablesTimer.resume(now=False) 

    def streamVariablesOK(self):
        """It's called when the server notifies variables were received correctly."""
        self.variables.setUpdated(True)
        self.variablesTimer.resume(now=True)


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
        streamer=True, 
        wait=True
    )
