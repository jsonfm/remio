"""Settings file."""
from utils import process_image

# ------------------------ SERVER SETTINGS ------------------------------------

serverSettings = {
    'address': 'http://localhost:5000',
    # 'key': 'Av2ff)_(@)323123-cxs51xB.p',
}

# ------------------------- STREAM SETTINGS -----------------------------------

streamSettings = {
    'endpoint': 'stream',
    'mode': 'auto',
    'quality': 70,
    'fps': 12,
    'colorspace': 'bgr',
    'colorsubsampling': '444',
    'fastdct': True,
    'enabled': True,
}

# ------------------------- CAMERA SETTINGS ------------------------------------

encoderParams = {
    'quality': 80,
    'colorspace': 'bgr',
    'colorsubsampling': '422',
    'fastdct': True
}

cameraSettings = {
    'webcam': {
        'src': 0,
        'fps': None,
        'size': [600, 400],
        'flipX': True,
        'flipY': False,
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
        'timeout': 1.0,
        'reconnectDelay': 5,
        'portsRefreshTime': 5,
        'emitterIsEnabled': True,
    },
}
