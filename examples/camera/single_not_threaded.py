"""Processing function API."""
import time
import cv2
from remio import Camera


# Intialize Camera manager
camera = Camera(src=0, size=[600, 400], flipX=True)

# Loads camera device but doesn't start background read loop
camera.loadDevice()


# Set a FPS speed to display image(s)
FPS = 10
T = 1 / FPS # Sampling period


while True:

    t0 = time.time()

    # Now the processing ocurrs on the main thread.
    frame = camera.read() 

    if frame is not None:
        cv2.imshow("webcam1", frame)

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
camera.stop()
