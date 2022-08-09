import unittest
from remio import Serial


class TestCamera(unittest.TestCase):
    def setUp(self):
        self.serial = Serial()

    def test_ports(self):
        assert type(self.serial.ports()) == list, "It's not a list of ports"
    
    def test_dict_to_json(self):
        """Tests dict to json."""
        _dict = {"a": 1, "b": 2, "c": 3}
        _str = "wrong input"
        assert type(self.serial.dictToJson(_dict)) == str, "It's not returning a json string"
        assert self.serial.dictToJson(_str) == _str , "It's not returning the same input"