"""A simple MJPEG"""
from remio import Camera, MJPEGServer


camera = Camera(src=0, fps=15, size=[800, 600], flipX=True)
server = MJPEGServer(camera, ip="0.0.0.0", port=8080)


try:
    server.run(display_url=True, start_camera=True)
except KeyboardInterrupt:
    server.stop(stop_camera=True)
