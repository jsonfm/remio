"""An example of remio Cameras API with an object color tracker."""
import time
import cv2
from remio import Cameras
from utils import Tracker

# Intialize tracker
robot = Tracker()

# Define devices
devices = {
    "webcam": {
        "src": 0,
        "size": [400, 300],
        "fps": None,
        "flipX": True,
        "reconnectDelay": 5,
        "backgroundIsEnabled": True,
        "emitterIsEnabled": False,
        "processing": robot.track,
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
        cv2.imshow("webcam1", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    t1 = time.time()

    print(f"position: {robot.get_position()}")

    # Get a fixed delay value (t1 - t0) + delay = T
    delay = abs(T - (t1 - t0))
    time.sleep(delay)


# Close all Windows
cv2.destroyAllWindows()

# Stop all Running devices
camera.stopAll()
