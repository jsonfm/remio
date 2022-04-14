"""Pausable camera example."""
import time
import cv2
from remio import Camera


# Initialize Single Camera device
camera = Camera(name="webcam", src=0, size=[400, 400])

# Start device(s) connection on background
camera.start()

# Set a FPS speed to display image(s)
FPS = 10
T = 1 / FPS

# Auxiliar variables
i = 0

while True:

    t0 = time.time()

    image = camera.read()

    if image is not None:
        cv2.imshow("webcam1", image)
        camera.clearFrame()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    t1 = time.time()

    # Get a fixed delay value (t1 - t0) + delay = T
    delay = abs(T - (t1 - t0))
    time.sleep(delay)

    # Pauses camera when some event occurs
    i += 1

    if i == 50:
        # Here the CPU relaxes
        print("Pausing the camera read loop.")
        camera.pause()

    if i == 100:
        # Here the CPU returns to work
        print("Resuming the camera read loop.")
        camera.resume()
        i = 0

# Close all Windows
cv2.destroyAllWindows()

# Stop all Running devices
camera.stop()
