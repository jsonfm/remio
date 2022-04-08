"""Ports"""
from remio import Serials


serial = Serials()


for port in serial.getListOfPorts():
    print(f" - {port}")
