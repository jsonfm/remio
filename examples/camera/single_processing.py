"""Processing function API."""
import time
import cv2
from remio import Camera


def processing(frame, *args, **kwargs):
    """Applies some image processing.

    Args:
        frame: a numpy array
    """

    if 'color' in kwargs: # if you pass a param named `color` it will print it
        print(kwargs['color'])

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame


# Intialize Camera manager
camera = Camera(src=0, size=[600, 400])

# set processing function passing to it some params
camera.setProcessing(processing, color='red')

# Also you could do
# camera.setProcessing(processing)

# Start device(s) read loop on background
camera.start()

# Set a FPS speed to display image(s)
FPS = 20
T = 1 / FPS # Sampling period


while True:

    t0 = time.time()

    frame = camera.read()
    camera.clearFrame()  # to avoid repeated frames, this line it's optional

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
