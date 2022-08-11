import unittest
import pytest
from remio.serialio import Serial


class TestCamera(unittest.TestCase):
    def setUp(self):
        """Configuring serial"""
        self.serial = Serial()

    def test_ports(self):
        """Test ports listing static method."""
        assert type(self.serial.ports()) == list, "It's not a list of ports"

    def test_dict_to_json(self):
        """Test dict to json function."""
        _dict = {"a": 1, "b": 2, "c": 3}
        _str = "wrong input"
        assert (
            type(self.serial.dictToJson(_dict)) == str
        ), "It's not returning a json string"
        assert self.serial.dictToJson(_str) == _str, "It's not returning the same input"

    def test_write(self):
        """Test write function."""
        message = "hello"
        self.serial.write(message)

    def test_check_serial_port(self):
        """Test for check serial port"""
        self.serial.checkSerialPorts(0.01)
        with pytest.raises(ValueError):
            self.serial.checkSerialPorts("a")

    def test_set_port(self):
        """Test set port method."""
        self.serial.setPort("COM7")

        with pytest.raises(ValueError):
            self.serial.setPort(22)

        with pytest.raises(ValueError):
            self.serial.setPort({})
