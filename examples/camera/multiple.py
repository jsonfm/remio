"""Multiple cameras manage."""
import time
import cv2
from remio import Cameras


# Define devices
devices = {
    "webcam1": {
        "src": 0,
        "size": [400, 300],
        "fps": None,
        "reconnectDelay": 5,
        "backgroundIsEnabled": True,
        "emitterIsEnabled": False,
    },
    "webcam2": {
        "src": "http://192.168.100.70:3000/video/mjpeg",
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
    
    webcam1, webcam2 = camera.read(asDict=False)
    camera.clearAllFrames() # to avoid repeated frames

    if webcam1 is not None:
        cv2.imshow("webcam1", webcam1)

    if webcam2 is not None:
        cv2.imshow("webcam2", webcam2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    t1 = time.time()

    # Get a fixed delay value (t1 - t0) + delay = T 
    delay = abs(T - (t1 - t0))
    time.sleep(delay)
    

# Close all Windows
cv2.destroyAllWindows() 

# Stop all Running devices
camera.stopAll()