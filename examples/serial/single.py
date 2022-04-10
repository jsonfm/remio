"""Single serial device example."""
import time
from remio import Serials


# Define devices
devices = {
    "arduino": {
        "port": "/dev/cu.usbserial-1440",
        "baudrate": 9600,
        "emitterIsEnabled": True,  # Enable on/emit callbacks
        "reconnectDelay": 5,
    },
}

# Intialize Serial manager
serial = Serials(devices=devices)

# Configure callbacks
serial.on("connection", lambda status: print(f"serial connected: {status}"))

# Start device(s) connection on background
serial.startAll()


while True:
    print("Doing some tasks...")
    time.sleep(1)
