import numpy as np
import unittest
import pytest
import time
from remio import Camera


class TestCamera(unittest.TestCase):
    def setUp(self):
        self.camera = Camera(src=0)

    def test_get_name(self):
        name = self.camera.getName()
        assert name == "default", "default name is not being applied correctly"

    def test_read_camera(self):
        frame = self.camera.read()
        assert not self.camera.isConnected(), "Camera should not be open"
        assert frame is None, "camera should not read any frame when it's off"

    def test_jpeg(self):
        jpeg = self.camera.jpeg()
        assert jpeg is None, "jpeg method not returning None when camera is off"

    def test_single_camera(self):
        assert (
            self.camera.isConnected() == False
        ), "Couldn't connect with the camera device."


    def test_is_threaded(self):
        """Checks if camera is threaded or not."""
        assert self.camera.isThreaded() == False, "Camera is not threaded"

    def test_create_background(self):
        """Tests for create a background."""
        assert type(self.camera.createBackground()) == np.ndarray, "Camera is not creating a numpy background"

    def test_set_processing(self):
        """Tests for set processing function"""
        def callback():
            print("I'm a test callback")
            
        error = self.camera.setProcessing(callback)
        assert error == False, "Error should be false, because procesing it's callable"

        error = self.camera.setProcessing('not valid input')
        assert error == True, "Error should be True because procesing input param it's not valid"

    def test_set_speed(self):
        self.camera.setSpeed(10)

        with pytest.raises(ValueError):
            self.camera.setSpeed(0)

        with pytest.raises(ValueError):
            self.camera.setSpeed('a')


    def test_stop_camera(self):
        self.camera.stop()
