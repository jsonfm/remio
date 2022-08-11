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


def read_frame_gray():
    """Generates a random frame with single color channel"""
    return np.random.randint(255, size=(1024, 720), dtype=np.uint8)


def test_encoder_rgb():
    """Test mjpeg encoder with rgb images."""
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


def test_encoder_gray():
    """Test mjpeg encoder with gray images."""
    max_encoding_time = 0.02  # seconds
    encoder = MJPEGEncoder(**encoderParams)
    encoding_time = []
    for i in range(10):
        frame = read_frame_gray()
        t0 = time.time()
        encoded = encoder.encode(frame, base64=True)
        t1 = time.time()
        encoding_time.append(t1 - t0)
    encoding_time = np.array(encoding_time)
    assert encoding_time.mean() < max_encoding_time, "Improve the encoder..."


def test_multiple_encode():
    """Test for multiple encoding"""
    encoder = MJPEGEncoder(**encoderParams)
    frame1 = read_frame()
    frame2 = read_frame_gray()
    frames_dict = {"cam1": frame1, "cam2": frame2}
    encoded_dict = encoder.multipleEncode(frames_dict)
    assert type(encoded_dict) == dict, "It's not a dict"

    frames_list = [frame1, frame2]
    encoded_list = encoder.multipleEncode(frames_list)
    assert type(encoded_list) == list, "It's not a list"


def test_set_params():
    """Test for set params"""
    encoder = MJPEGEncoder()
    encoder.setParams(**encoderParams)
