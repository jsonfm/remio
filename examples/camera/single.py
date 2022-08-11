"""Single camera manage."""
import time
import cv2
from remio import Cameras


# Define devices
devices = {
    "webcam": {
        "src": 0,
        "size": [400, 300],
        "fps": None,
        "reconnectDelay": 5,
        "backgroundIsEnabled": True,
        "emitterIsEnabled": False,
    },
}

# Intialize Serial manager
camera = Cameras(devices=devices)

# Start device(s) connection on background
camera.startAll()

# Set a FPS speed to display image(s)
FPS = 20
T = 1 / FPS

while True:

    t0 = time.time()

    frame = camera["webcam"].read()
    camera.clearAllFrames()  # to avoid repeated frames

    if frame is not None:
        cv2.imshow("webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    t1 = time.time()

    readtime = t1 - t0 # reading and display time

    # Get a fixed delay value, where sampling period should be T = readtime + delay
    delay = abs(T - readtime)
    time.sleep(delay)


# Close all Windows
cv2.destroyAllWindows()

# Stop all Running devices
camera.stopAll()
