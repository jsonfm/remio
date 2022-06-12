"""HTTP server functionalities."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import time
from .stream import MJPEGEncoder


class Handler(BaseHTTPRequestHandler):
    """Custom HTTP handler for streaming video on MJPEG format."""
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
        self.end_headers()

        if self.server.camera is not None and self.server.encoder is not None:
            fps = self.server.fps
            while True:
                try:
                    frame = self.server.camera.read()
                    jpeg = self.server.encoder.encode(frame, base64=False)
                    
                    self.wfile.write(bytes("--jpgboundary\n", "utf8"))
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', len(jpeg))
                    self.end_headers()

                    self.wfile.write(jpeg)
                    time.sleep(1 / fps) 

                except Exception as e:
                    print("error: ", e)
                    break


class CustomHTTPServer(HTTPServer):
    """HTTP server with custom params."""
    def __init__(self, camera = None, encoder = None, fps: int = 12, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera = camera
        self.encoder = encoder
        self.fps = fps


class ThreadedHTTPServer(ThreadingMixIn, CustomHTTPServer):
    """Handle requests in a separate thread."""


class MJPEGServer:
    """A MJPEG server class"""
    def __init__(self, 
        camera = None,
        fps: int = 10,
        ip: str = '0.0.0.0', 
        port: int = 8080, 
        encoderSettings: dict = {
            "quality": 60,
            "colorspace": "bgr",
            "colorsubsampling": "422",
            "fastdct": True,
            "enabled": True,
        },
        *args, 
        **kwargs
    ):
        self.camera = camera
        self.fps = fps
        self.encoder = MJPEGEncoder(**encoderSettings)
        self.server = ThreadedHTTPServer(
            camera=self.camera,
            encoder=self.encoder,
            fps = self.fps,
            server_address=(ip, port),
            RequestHandlerClass=Handler
        )

    def run(self):
        """Executes the streaming loop."""
        self.server.serve_forever()
