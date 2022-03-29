from .camio import Cameras
from .serialio import Serials
from .socketSync import CustomSocketIO
from .stream import SocketStreamer


class Mockup:
    """A class to manage communication.

    Args:
        cameraSettings:
        serialSettings:
        streamSettings: 
    """
    def __init__(self, 
            cameraSettings: dict = {},
            serialSettings: dict = {},
            serverSettings: dict = {},
            streamSettings: dict = {},
            *args, 
            **kwargs):
        self.camera = Cameras(devices=cameraSettings)
        self.serial = Serials(devices=serialSettings)
        self.socket = CustomSocketIO(**serverSettings)
        self.streamer = SocketStreamer(socket=self.socket, reader=self.camera.read, **streamSettings)

    def start(self, camera: bool = False, serial: bool = False, socket: bool = False, streamer: bool = False):
        """It starts differents programs.

        Args:
            camera: start camera?
            serial: start serial?
            socket: start socket?
            streamer: start stream?
        """
        if camera:
            self.camera.startAll()

        if serial:
            self.serial.startAll()

        if socket:
            self.socket.start()

        if streamer:
            self.streamer.start()

    def stop(self):
        """It stops all tasks."""
        self.socket.stop()
        self.streamer.stop()
        self.camera.stopAll()
        self.serial.stopAll()
