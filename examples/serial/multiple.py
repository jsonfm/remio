"""Multiple serial devices example."""
import time
from remio import Serials

# Define devices
devices = {
    "arduino1": {
        "src": 0,
        "port": "COM1",
        "baudrate": 9600,
        "emitterIsEnabled": True,
    },
    "arduino2": {
        "src": 1,
        "port": "COM2",
        "baudrate": 9600,
        "emitterIsEnabled": False,
    }
}


serial = Serials(devices=devices)
serial.startAll()

while True:
    print("Do some tasks...")
    time.sleep(1)