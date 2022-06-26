"""A MJPEG Server (Async) with Sanic."""
import asyncio
from sanic import Sanic, response
from remio import Camera


app = Sanic(name="server")


async def camera_read():
    """Camera read loop."""
    while True:
        yield camera.jpeg(quality=30, colorspace="bgr")
        await asyncio.sleep(1 / 20)


async def streaming(resp):
    """Streaming loop."""
    async for frame in camera_read():
        await resp.write(
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )


@app.get("/")
async def streaming_route(request):
    """Route for view the streaming."""
    return response.stream(
        streaming, content_type="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    # Start camera without the read loop
    camera = Camera(src=0, size=[800, 600], flipX=True).loadDevice()
    app.run(host="0.0.0.0", port=8888)
