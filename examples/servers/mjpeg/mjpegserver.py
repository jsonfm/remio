"""A simple MJPEG."""
from remio import Camera, MJPEGServer


encoderParams = {
    "quality": 90,
    "colorspace": "bgr",
    "colorsubsampling": "422",
    "fastdct": True,
}


# Initialize camera device
camera = Camera(src=0, fps=15, size=[800, 600], flipX=True, encoderParams=encoderParams)

# Configure MJPEG Server
server = MJPEGServer(
    camera=camera, ip="0.0.0.0", port=8080, endpoint="/video/mjpeg", fps=15
)

try:
    server.run(display_url=True, start_camera=True)
except KeyboardInterrupt:
    server.stop(stop_camera=True)
