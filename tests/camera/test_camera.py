import numpy as np
import unittest
import time
from remio import Camera, Cameras


class TestCameras(unittest.TestCase):
    def setUp(self):
        self.camera = Camera(src=0)

    def test_read_camera(self):
        assert 3 == 3, "Error"

    def test_single_camera(self):
        assert (
            self.camera.isConnected() == False
        ), "Couldn't connect with the camera device."

    def test_stop_camera(self):
        self.camera.stop()
