import unittest
import pytest
from remio import Serial, Serials


class TestSerials(unittest.TestCase):
    """Tests serials."""
    def setUp(self):
        devices = {
            "arduino1": {
                "port": "/dev/cu.usbserial-1440",
                "baudrate": 9600,
            },
            "arduino2": {
                "port": "COM7",
                "baudrate": 9600,
            }
        }
        self.serial = Serials(devices=devices)

    def test_get_device(self):
        """Test for get device method."""
        serial1 = self.serial.getDevice("arduino1")
        assert isinstance(serial1, Serial), "serial1 is not a instance of Camera"

        serial2 = self.serial.getDevice("arduino2")
        assert isinstance(serial2, Serial), "serial2 is not a instance of Camera"

        failserial = self.serial.getDevice("failserial")
        assert isinstance(failserial, type(None)), "failserial should be None"
    
    def test_get_device2(self):
        """Tests for get devices using key id"""
        serial1 = self.serial["arduino1"]
        assert isinstance(serial1, Serial), "serial1 is not a instance of Camera"

        serial2 = self.serial["arduino2"]
        assert isinstance(serial2, Serial), "serial2 is not a instance of Camera"

        with pytest.raises(KeyError):
            failserial = self.serial["failserial"]
            assert isinstance(failserial, type(None)), "failserial should be None"