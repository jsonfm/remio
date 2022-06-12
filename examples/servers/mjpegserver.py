"""A simple MJPEG"""
from remio import Camera, MJPEGServer


if __name__ == '__main__':
    try:
        IP = "0.0.0.0"
        PORT = 8080
        FPS = 10
        camera = Camera(src=0, fps=FPS, size=[800, 600], flipX=True).start()
        server = MJPEGServer(camera, ip=IP, port=PORT)
        print(f"MJPEG Server running on http://{IP}:{PORT}")
        server.run()
    except KeyboardInterrupt:
        camera.stop()