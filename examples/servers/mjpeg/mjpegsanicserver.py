"""A MJPEG async server based on sanic.

todo:
- Fix the bug with asyncio and threading
"""
import asyncio
from threading import Thread
from sanic import Sanic, response
from remio.camio import Camera


class MJPEGAsyncServer:
    """A MJPEG async server made with sanic."""

    def __init__(
        self,
        camera=None,
        fps: int = 12,
        ip: str = "0.0.0.0",
        port: int = 8080,
        endpoint: str = "",
        *args,
        **kwargs
    ):
        self.camera = camera
        self.ip = ip
        self.port = port
        self.fps = fps
        self.endpoint = endpoint
        self.server = Sanic(name="server")
        self.server.add_route(self.streaming_route, self.endpoint)
        self.thread = Thread(target=self.run, daemon=True)
        self.loop = None

    def start(self):
        """Starts server loop on a separated thread."""
        self.thread.start()

    async def camera_read(self):
        """Camera read loop."""
        while True:
            yield self.camera.jpeg(quality=30, colorspace="bgr")
            await asyncio.sleep(1 / self.fps)

    async def streaming(self, resp):
        """Streaming loop."""
        async for frame in self.camera_read():
            await resp.write(
                b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )

    async def streaming_route(self, request):
        """Route for view the streaming."""
        return response.stream(
            self.streaming, content_type="multipart/x-mixed-replace; boundary=frame"
        )

    def run(self):
        """Executes the server loop."""
        self.server.run(host=self.ip, port=self.port)


if __name__ == "__main__":
    camera = Camera(src=0, size=[800, 600], flipX=True).start()
    server = MJPEGAsyncServer(camera, fps=15)
    server.run()
