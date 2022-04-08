"""Mockup base file."""

import sys
import signal
from threading import Event
from .camio import Cameras
from .serialio import Serials
from .socketSync import CustomSocketIO
from .stream import SocketStreamer


class Mockup:
    """A class for manage mutltiple cameras, multiple serial devices and socketio communications.

    Args:
        cameraSettings: settings for camera devices.
        serialSettings: settings for serial devices.
        serverSettings: settings to connect with a socketio server.
        streamSettings: settings for stream devices.
    """

    def __init__(
        self,
        cameraSettings: dict = {},
        serialSettings: dict = {},
        serverSettings: dict = {},
        streamSettings: dict = {},
        *args,
        **kwargs
    ):
        self.camera = Cameras(devices=cameraSettings)
        self.serial = Serials(devices=serialSettings)
        self.socket = CustomSocketIO(**serverSettings)
        self.streamer = SocketStreamer(
            socket=self.socket, 
            reader=self.camera.read, 
            **streamSettings
        )

        self.waitEvent = Event()
        self.waitEvent.clear()

        signal.signal(signal.SIGINT, self.softStop)
        signal.signal(signal.SIGTERM, self.softStop)  

    def __del__(self):
        self.stop()

    def start(
        self,
        camera: bool = False,
        serial: bool = False,
        socket: bool = False,
        streamer: bool = False,
        wait: bool = True,
    ):
        """It starts differents programs.

        Args:
            camera: start camera?
            serial: start serial?
            socket: start socket?
            streamer: start stream?
            wait: block the thread who calls this function?
        """
        if camera:
            self.camera.startAll()

        if serial:
            self.serial.startAll()

        if socket:
            self.socket.start()

        if streamer:
            self.streamer.start()
        
        if wait:
            self.waitEvent.wait()

    def stop(self):
        """Stops all tasks of socketio, serial, camera and streamer threads/processes."""
        self.camera.stopAll()
        self.serial.stopAll()
        self.streamer.stop()
        self.socket.stop()
        self.waitEvent.set()

    def softStop(self, sig, frame):
        """Stops mockup exectution when a system signal is emitted, ex. CTRL + C."""
        print("  Mockup:: STOPING...")
        self.stop()
        sys.exit(0)