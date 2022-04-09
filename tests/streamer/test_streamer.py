import numpy as np
from socketio import Client
from remio import SocketStreamer


def test_streamer():
    """Test socket streamer class."""
    streamer = SocketStreamer(socket=Client())
    assert streamer.hasSocket(), "Streamer has not socket."
    frame = np.random.randint(255, size=(900, 800, 3), dtype=np.uint8)
    streamer.stream(frame)
