import unittest
from remio import Camera
from remio.httpservers import MJPEGServer


class TestCamera(unittest.TestCase):
    def setUp(self):
        self.camera = Camera(src=1, reconnectDelay=0.5)
        self.mjpegserver = MJPEGServer(camera=self.camera)
