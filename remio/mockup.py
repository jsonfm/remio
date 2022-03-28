from typing import Callable
from .camio import Cameras
from .serialio import Serials
from .socketSync import CustomSocketIO


class Mockup:
    """A class to manage communication.


    Args:
        identifier: name of the current machine.
        cameraDevices: a dict with camera names and sources. (ex. {'cam1': 0, 'cam2': 'http://whatever'} )
        cameraOptions: config params for cameras.
        cameraInParallel: run camera program in another cpu core / process ?
        serialDevices: a list with serial devices.
        serialOptions: options for serial devices.
        serialInParallel: run serial program in another cpu core/ process?
        socketioOptions: options for socketIO.
    """
    def __init__(self, 
            cameraSettings: dict = {},
            serialSettings: dict = {},
            serverSettings: dict = {},
            streamSettings: dict = {},
            *args, 
            **kwargs):

        self.identifier = None
        self.camera = Cameras(devices=cameraSettings)
        self.serial = Serials(devices=serialSettings)
        self.socket = CustomSocketIO()

    def startCamera(self):
        self.camera.startAll()
    
    def startSerial(self):
        self.serial.startAll()
    
    def startSocket(self):
        self.socket.start()

    def start(self, camera: bool = False, serial: bool = False, socket: bool = False):
        """It starts differents programs.

        Args:
            camera: start camera?
            serial: start serial?
            socket: start socket?
        """
        if camera:
            self.startCamera()

        if serial:
            self.startSerial()

        if socket:
            self.startSocket()

        # if camera or serial or socket:
        #     self.running.set() 
        #     self.thread.start()  

    def checkCameraEvents(self):
        if self.camera.connectionEvent.is_set():
            self.localEvents.emit('camera-on')

    def checkSerialEvents(self):
        if self.serial.connectionEvent.is_set():
            self.localEvents.emit('serial-connection-event', self.serial.isConnected())
            self.serial.connectionEvent.clear()

        if self.serial.incomingData.is_set():
            self.localEvents.emit('serial-incoming-data')
            self.serial.incomingData.clear()

    def checkSocketEvents(self):
        if self.socket.connectionEvent.is_set():
            self.localEvents.emit('socket-connection-event', self.socket.isConnected())
            self.socket.connectionEvent.clear()

        if self.socket.incomingData.is_set():
            self.localEvents.emit('socket-incoming-data', self.socket.getData())
            self.socket.incomingData.clear()

    def run(self):
        """It checks."""
        pass

    def stop(self):
        """It stops all tasks."""
        # if self.running.is_set():
        self.camera.stopAll()
        self.serial.stopAll()

    def writeToSocket(self, event: str = None, data = None):
        """It writes some data through the socketio.

        event: event
        data: some data
        """
        self.socket.write(event, data)

    def writeToSerial(self, data):
        """It writes."""
        self.serial.write(data)

    def on(self, event: str, callback: Callable):
        """It setup .
        """

        eventFiltered = event.split('-')[1:]
        eventFiltered = '-'.join(eventFiltered)

        if 'serial' in event:
            self.serial.on(eventFiltered, callback)

        if 'socket' in event:
            self.socket.on(eventFiltered, callback)

        if 'camera' in event:
            self.camera.on(eventFiltered, callback)