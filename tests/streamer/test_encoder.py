import time
import numpy as np
from remio import MJPEGEncoder


encoderParams = {
    "quality": 60,
    "colorspace": "bgr",
    "colorsubsampling": "422",
    "fastdct": True,
}


def read_frame():
    """Generates a random frame"""
    return np.random.randint(255, size=(1024, 720, 3), dtype=np.uint8)


def test_encoder():
    """Test socket encoder class."""
    max_encoding_time = 0.02  # seconds
    encoder = MJPEGEncoder(**encoderParams)
    encoding_time = []
    for i in range(10):
        frame = read_frame()
        t0 = time.time()
        encoded = encoder.encode(frame, base64=True)
        t1 = time.time()
        encoding_time.append(t1 - t0)
    encoding_time = np.array(encoding_time)
    assert encoding_time.mean() < max_encoding_time, "Improve the encoder..."
