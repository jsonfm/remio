"""Example experiment.

author: author@example.com 
license: MIT
year: 2022

"""
import sys
import signal
from remio import Mockup
from settings import (
    serverSettings,
    streamSettings,
    cameraSettings,
    serialSettings,
)
from utils import RepeatTimer


class CustomMockup(Mockup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configureSerial()

    def configureSerial(self):
        self.serial.on("ports-update", lambda ports: print("serial - ports: ", ports))
        self.serial.on(
            "connection-status", lambda status: print(f"serial connected: {status}")
        )


def handler(sig, num):
    experiment.stop()
    sys.exit(0)


if __name__ == "__main__":
    experiment = CustomMockup(
        serverSettings=serverSettings,
        streamSettings=streamSettings,
        cameraSettings=cameraSettings,
        serialSettings=serialSettings,
    )
    experiment.start(camera=True, serial=True, socket=True, streamer=True)
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
