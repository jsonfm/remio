"""Processing function API."""
import time
import cv2
from remio import Cameras


def processing(frame, *args, **kwargs):
    """Do some image processing.

    Args:
        frame: a numpy array
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame


# Intialize Serial manager
camera = Cameras(devices={"webcam": {"src": 0, "size": [400, 300]}})
camera["webcam"].setProcessing(processing)

# Start device(s) connection on background
camera.startAll()

# Set a FPS speed to display image(s)
FPS = 30
T = 1 / FPS

while True:

    t0 = time.time()
    
    frame = camera["webcam"].read()
    camera.clearAllFrames() # to avoid repeated frames

    if frame is not None:
        cv2.imshow("webcam1", frame)

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
