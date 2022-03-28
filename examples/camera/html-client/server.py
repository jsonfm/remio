import uvicorn
import socketio
import asyncio
import simplejpeg
import base64
import threading
import time
from remio import Machine


sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio, static_files={
    '/': './public/index.html',
    '/main.js': './public/main.js',
})

machine = Machine(cameraDevices={'webcam': 0}, cameraOptions={'fps': None, 'size':[320, 240]})
machine.start(camera=True)
time.sleep(1)
DELAY = 1 / 5

async def stream():
    while True:
        frame = machine.camera.getFrameOf('webcam')
        if frame is not None:
            jpeg = simplejpeg.encode_jpeg(frame, quality=80, colorspace='BGR', fastdct=True)
            b64 = base64.b64encode(jpeg).decode()
            await sio.emit('stream', b64)
        await asyncio.sleep(DELAY)

@sio.event
async def connect(sid, environ):
    print('connect: ', sid)
    await asyncio.sleep(.5)

@sio.event
async def disconnect(sid):
    print('disconnect: ', sid)
    await asyncio.sleep(.5)

@sio.on('web-to-server-update-state')
async def receive(sid, data):
    print()
    print('==== WEB CLIENT ====')
    print('sid: ', sid)
    print('data: ', data)
    print()
    await sio.emit('server-to-machine-update-state', data)

@sio.on('machine-to-server-update-state')
async def receive(sid, data):
    print()
    print('==== MACHINE CLIENT ====')
    print('sid: ', sid)
    print('data: ', data)
    print()   

async def run(scope, receive, send):
    await asyncio.gather(stream(), app(scope, receive, send))

if __name__ == '__main__':
    uvicorn.run("server:run", host='0.0.0.0', port=3000, reload=False, workers=1)
    
