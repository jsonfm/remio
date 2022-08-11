import numpy as np
import unittest
import pytest
from remio import Camera


class TestCamera(unittest.TestCase):
    def setUp(self):
        self.camera = Camera(src=0)

    def test_get_name(self):
        """Test get name method."""
        name = self.camera.getName()
        assert name == "default", "default name is not being applied correctly"

    def test_read_camera(self):
        frame = self.camera.read()
        assert not self.camera.isConnected(), "Camera should not be open"
        assert frame is None, "camera should not read any frame when it's off"

    def test_jpeg(self):
        """Test jpeg encoder method."""
        jpeg = self.camera.jpeg()
        assert jpeg is None, "jpeg method not returning None when camera is off"

    def test_single_camera(self):
        """Test single camera"""
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
            
        self.camera.setProcessing(callback)

        with pytest.raises(ValueError):
            self.camera.setProcessing('not valid input')
        
    def test_set_speed(self):
        """Tests for set speed (set FPS) function."""
        self.camera.setSpeed(10)

        with pytest.raises(ValueError):
            self.camera.setSpeed(0)

        with pytest.raises(ValueError):
            self.camera.setSpeed('a')

    def test_get_frame64(self):
        """Tests for get frame on base64 format."""
        b64 = self.camera.getFrame64()
        assert isinstance(b64, type(None)), "b64 frame should be None"

    def test_stop_camera(self):
        """Stops camera"""
        self.camera.stop()
