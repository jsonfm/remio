"""Write serial device example."""
import time
from remio import Serials


# Define devices
devices = {
    "arduino": {
        "port": "/dev/cu.usbserial-1460",
        "baudrate": 9600,
        "emitterIsEnabled": True,  # Enable on/emit callbacks
        "reconnectDelay": 5,
    },
}

# Intialize Serial manager
serial = Serials(devices=devices)

# Configure callbacks
serial.on("connection", lambda status: print(f"serial connected: {status}"))
serial.on("data", lambda response: print(f"serial says: {response}"))

# Start device(s) connection on background
serial.startAll()

i = 0
while True:
    # print("Doing some tasks...")
    i += 1
    if i == 10:
        print("-> Writting to the arduino...")
        serial["arduino"].write("Soy Python")
        i = 0
    time.sleep(1)
