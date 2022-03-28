"""Example experiment.

author: author@example.com 
license: MIT
year: 2022

"""
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
        self.timer = RepeatTimer(1, self.updateVideo)
        self.timer.start()

    def updateVideo(self):
        frame = self.camera.getFrameOf('webcam')


if __name__ == "__main__":
    experiment = CustomMockup(
        serverSettings=serverSettings,
        streamServer=streamSettings,
        cameraSettings=cameraSettings,
        serial=serialSettings,
    )
    experiment.start(camera=True)