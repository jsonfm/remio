from socketio import Client


class CustomSocketIO(Client):
    """A custom socketio client."""

    def __init__(self, address: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.address = address

    def stop(self):
        try:
            self.disconnect()
        except Exception as e:
            print("Socket:: ", e)

    def start(self):
        """Starts socketio connection"""
        if self.address is not None:
            try:
                self.connect(self.address, wait=True)
            except Exception as e:
                print("socket:: ", e)

    def emit(self, *args, **kwargs):
        """custom emit method."""
        try:
            super().emit(*args, **kwargs)
        except Exception as e:
            print("socket:: ", e)

    def on(self, *args, **kwargs):
        """custom on method."""
        event = args[0]
        handler = args[1]
        if event == "connection":
            super().on("connect", handler)
            super().on("disconnect", handler)
        else:
            super().on(*args, **kwargs)

    def isConnected(self):
        """Checks if socket it's connected"""
        return not self.connected

    def toogle(self, value: bool = False):
        """switchs socketio. """
        if value:
            self.start()
        else:
            self.stop()
