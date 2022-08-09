import numpy as np
import unittest
import time
from remio import Camera


class TestCamera(unittest.TestCase):
    def setUp(self):
        self.camera = Camera(src=0)

    def test_read_camera(self):
        # time.sleep(1)
        frame = self.camera.read()
        # time.sleep(1)

    def test_single_camera(self):
        assert (
            self.camera.isConnected() == False
        ), "Couldn't connect with the camera device."


    def test_is_threaded(self):
        """Checks if camera is threaded or not."""
        assert self.camera.isThreaded() == False, "Camera is not threaded"

    def test_create_background(self):
        assert type(self.camera.createBackground()) == np.ndarray, "Camera is not creating a numpy background"

    def test_set_processing(self):
        callback = lambda: print('callback')
        self.camera.setProcessing(callback)

    def test_stop_camera(self):
        self.camera.stop()
