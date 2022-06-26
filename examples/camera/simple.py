"""Single simple camera example."""
import time
from remio import Camera

# Initialize Single Camera device
camera = Camera(name="webcam", src=0, size=[400, 400])
camera.start()


while True:
    print("Doing some tasks...")
    time.sleep(2)
