"""Settings file."""
from decouple import AutoConfig
from utils import processing
from routes import *

# ENV PATH
config = AutoConfig(search_path="./.env")
# ------------------------ SERVER SETTINGS ------------------------------------

serverSettings = {
    # "address": config("address", default="http://localhost:3000", cast=str),
    "address": "http://localhost:3000",
    "request_timeout": 10,
}
print("server: ", serverSettings)
# ------------------------- STREAM SETTINGS -----------------------------------

streamSettings = {
    "endpoint": STREAM_CLIENT_SERVER,
    "quality": 60,
    "fps": 15,
    "colorspace": "bgr",
    "colorsubsampling": "422",
    "fastdct": True,
    "enabled": True,
}

# ------------------------- CAMERA SETTINGS ------------------------------------

cameraSettings = {
    "webcam": {
        "src": 0,
        "fps": None,
        "size": [600, 400],
        "flipX": True,
        "flipY": False,
        "emitterIsEnabled": False,
        "backgroundIsEnabled": True,
        "processing": processing,
        "processingParams": {},
        "encoderIsEnable": False,
    },
}

# --------------------------- SERIAL SETTINGS ------------------------------

serialSettings = {
    "arduino": {
        "port": "/dev/cu.usbserial-1460",
        "baudrate": 9600,
        "timeout": 1.0,
        "reconnectDelay": 5,
        "portsRefreshTime": 5,
        "emitterIsEnabled": True,
        "emitAsDict": True,
    },
}
