"""Camera callbacks example."""
import time
import cv2
from remio import Camera

image = None


def read_frame(frames: dict):
    global image
    image = frames["webcam"]


# Initialize Single Camera device
camera = Camera(name="webcam", src=0, size=[400, 400], emitterIsEnabled=True)

# Configure callbacks
camera.on("frame-ready", read_frame)

# Start device(s) connection on background
camera.start()


# Set a FPS speed to display image(s)
FPS = 10
T = 1 / FPS

while True:

    t0 = time.time()

    if image is not None:
        cv2.imshow("webcam1", image)
        image = None

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    t1 = time.time()

    # Get a fixed delay value (t1 - t0) + delay = T
    delay = abs(T - (t1 - t0))
    time.sleep(delay)

# Close all Windows
cv2.destroyAllWindows()

# Stop all Running devices
camera.stop()
