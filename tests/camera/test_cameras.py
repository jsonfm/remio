import unittest
import pytest
from remio.camio import Camera, Cameras


class TestCamera(unittest.TestCase):
    def setUp(self):
        devices = {
            "cam1": {
                "src": 0
            },
            "cam2": {
                "src": 1
            }
        }
        self.camera = Cameras(devices=devices)

    def test_get_device(self):
        """Test for get device method."""
        camera1 = self.camera.getDevice("cam1")
        assert isinstance(camera1, Camera), "camera1 is not a instance of Camera"

        camera2 = self.camera.getDevice("cam2")
        assert isinstance(camera2, Camera), "camera2 is not a instance of Camera"

        failcam = self.camera.getDevice("failcam")
        assert isinstance(failcam, type(None)), "failcam should be None"
    
    def test_get_device2(self):
        """Tests for get devices using key id"""
        camera1 = self.camera["cam1"]
        assert isinstance(camera1, Camera), "camera1 is not a instance of Camera"

        camera2 = self.camera["cam2"]
        assert isinstance(camera2, Camera), "camera2 is not a instance of Camera"

        with pytest.raises(KeyError):
            failcam = self.camera["failcam"]
            assert isinstance(failcam, type(None)), "failcam should be None"

    def test_read(self):
        """Tests for read method."""
        frames = self.camera.read(asDict=True)
        assert type(frames) == dict, "frames are not in dict format"

        frames = self.camera.read(asDict=False)
        assert type(frames) == list, "frames are not in list format"

    def test_get_all_frames(self):
        """Tests for getAllFrames64."""
        frames = self.camera.getAllFrames(asDict=True)
        assert type(frames) == dict, "frames are not in dict format"

        frames = self.camera.getAllFrames(asDict=False)
        assert type(frames) == list, "frames are not in list format"

    def test_get_all_frames64(self):
        """Tests for getAllFrames64."""
        frames = self.camera.getAllFrames64(asDict=True)
        assert type(frames) == dict, "frames are not in dict format"

        frames = self.camera.getAllFrames64(asDict=False)
        assert type(frames) == list, "frames are not in list format"

    def test_get_frame_of(self):
        """Tests for getFrameOf."""
        frame = self.camera.getFrameOf("cam1")
        assert type(frame) == type(None), "frame should be None"

    