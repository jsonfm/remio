"""Settings file."""
from utils import process_image

# ------------------------ SERVER SETTINGS ------------------------------------

serverSettings = {
    'host': 'http://localhost:5000',
    'key': 'Av2ff)_(@)323123-cxs51xB.p',
}

# ------------------------- STREAM SETTINGS -----------------------------------

streamSettings = {
    'endpoint': 'https://somehost/stream',
    'mode': 'auto',
    'quality': 'high',
}

# ------------------------- CAMERA SETTINGS ------------------------------------

encoderParams = {
    'quality': 70,
    'colorspace': 'bgr',
    'colorsubsampling': '422',
    'fastdct': True
}

cameraSettings = {
    'webcam': {
        'src': 0,
        'fps': None,
        'size': [1024, 768],
        'emitterIsEnabled': False,
        'backgroundIsEnabled': True,
        'processing': None,
        'processingParams': {},
        'encoderIsEnable': False,
        'encoderParams': encoderParams
    },
}

# --------------------------- SERIAL SETTINGS ------------------------------

serialSettings = {
    'arduino': {
        'port': '/dev/cu.usbserial-1460',
        'baudrate': 9600,
        'timeout': 20,
        'reconnectDelay': 5,
        'portsRefreshTime': 5,
        'emitterIsEnabled': True,
    },
}
