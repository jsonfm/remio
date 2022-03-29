import uvicorn
import socketio


sio = socketio.AsyncServer(async_mode="asgi")
app = socketio.ASGIApp(
    sio,
    static_files={
        "/": "./public/index.html",
        "/main.js": "./public/main.js",
    },
)


@sio.event
async def connect(sid, environ):
    print("connect: ", sid)


@sio.on("web-to-server-update-state")
async def receive(sid, data):
    print()
    print("==== WEB CLIENT ====")
    print("sid: ", sid)
    print("data: ", data)
    print()
    await sio.emit("server-to-machine-update-state", data)


@sio.on("machine-to-server-update-state")
async def receive(sid, data):
    print()
    print("==== MACHINE CLIENT ====")
    print("sid: ", sid)
    print("data: ", data)
    print()


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=3000, reload=True)
